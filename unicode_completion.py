import sublime
import sublime_plugin

from .unicode_mixin import UnicodeCompletionMixin
from .latex_symbols import latex_symbols
from .emoji_symbols import emoji_symbols

symbols = latex_symbols + emoji_symbols


class UnicodeCompletionListener(UnicodeCompletionMixin, sublime_plugin.EventListener):

    def should_complete(self, view):
        if view.settings().get("unicode_completion", False):
            return True
        elif view.settings().get('is_widget') and \
                view.window().active_view().settings().get("unicode_completion", False):
            return True
        else:
            return False

    def on_query_completions(self, view, prefix, locations):
        if not self.should_complete(view):
            return None

        prefix = self.look_command_backward(view, locations[0])
        if not prefix:
            return None
        ret = [(s[0] + "\t" + s[1], s[1]) for s in symbols if s[0].startswith(prefix)]
        return ret

    def on_query_context(self, view, key, operator, operand, match_all):

        sel = view.sel()
        if len(sel) == 0 or not sel[0].empty():
            return

        pt = view.sel()[0].end()

        if not self.should_complete(view):
            return None

        if key == 'unicode_completion_only_one_match':
            prefix = self.look_command_backward(view, pt)
            count = 0
            for s in symbols:
                if s[0].startswith(prefix):
                    count = count + 1
            return (count == 1) == operand
        elif key == 'unicode_completion_has_matches':
            prefix = self.look_command_backward(view, pt)
            return (prefix is not None) == operand

        return None


class UnicodeCompletionInsertBestCompletion(UnicodeCompletionMixin, sublime_plugin.TextCommand):
    def run(self, edit, next_completion=False):
        view = self.view
        if len(view.sel()) == 0 or not view.sel()[0].empty():
            return
        pt = view.sel()[0].end()

        if not next_completion:
            prefix = self.look_command_backward(view, pt)
            self.completions = [s[1] for s in symbols if s[0].startswith(prefix)]
            view.run_command("insert_best_completion",  {"default": "\t", "exact": False})
            self.fix_completion(view, edit)
        else:
            region = sublime.Region(view.sel()[0].begin()-1, view.sel()[0].begin())
            prev_char = view.substr(region)
            if prev_char in self.completions:
                prev_index = self.completions.index(prev_char)
                next_index = prev_index + 1 if prev_index < len(self.completions) - 1 else 0
                for sel in reversed(view.sel()):
                    pt = sel.begin()
                    if view.substr(sublime.Region(pt-1, pt)) == prev_char:
                        view.replace(edit, sublime.Region(pt-1, pt), self.completions[next_index])


class UnicodeCompletionAutoComplete(UnicodeCompletionMixin, sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        view.run_command("auto_complete")
        self.fix_completion(view, edit)


class UnicodeCompletionCommitComplete(UnicodeCompletionMixin, sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        view.run_command("commit_completion")
        self.fix_completion(view, edit)


class ToggleUnicodeCompletion(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        view.settings().set(
            "unicode_completion",
            not view.settings().get("unicode_completion", False))
        onoff = "on" if view.settings().get("unicode_completion") else "off"
        sublime.status_message("UnicodeCompletion %s" % onoff)
