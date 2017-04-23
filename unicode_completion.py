import sublime
import sublime_plugin
import re
from .latex_symbols import latex_symbols
from .emoji_symbols import emoji_symbols


RE_COMMAND_PREFIX = re.compile(r".*(\\[:_0-9a-zA-Z+-^]*)$")
symbols = latex_symbols + emoji_symbols


def get_prefix(view):
    sel = view.sel()[0]
    pt = sel.end()
    line = view.substr(sublime.Region(view.line(pt).begin(), pt))
    m = RE_COMMAND_PREFIX.match(line)
    if m:
        return m.group(1)
    else:
        return None


def fix_completion(view, edit):
    for sel in view.sel():
        pt = sel.begin()
        if view.substr(sublime.Region(pt-3, pt-1)) == "\\:":
            view.replace(edit, sublime.Region(pt-3, pt-1), "")
        elif view.substr(sublime.Region(pt-4, pt-1)) == "\\:+":
            view.replace(edit, sublime.Region(pt-4, pt-1), "")
        elif view.substr(sublime.Region(pt-4, pt-1)) == "\\:-":
            view.replace(edit, sublime.Region(pt-4, pt-1), "")


class UnicodeCompletionListener(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        if view.settings().get('is_widget'):
            return
        if not view.settings().get("unicode_completion", False):
            return None

        prefix = get_prefix(view)
        if not prefix:
            return None
        ret = [(s[0] + "\t" + s[1], s[1]) for s in symbols if s[0].startswith(prefix)]
        return ret

    def on_query_context(self, view, key, operator, operand, match_all):
        if view.settings().get('is_widget'):
            return
        if not view.settings().get("unicode_completion", False):
            return

        if key == 'unicode_completion_only_match':
            prefix = get_prefix(view)
            count = 0
            for s in symbols:
                if s[0].startswith(prefix):
                    count = count + 1
            return (count == 1) == operand
        elif key == 'unicode_completion_has_prefix':
            prefix = get_prefix(view)
            return (prefix is not None) == operand

        return None


class UnicodeCompletionInsertBestCompletion(sublime_plugin.TextCommand):
    def run(self, edit, next_completion=False):
        view = self.view
        if not next_completion:
            prefix = get_prefix(view)
            self.completions = [s[1] for s in symbols if s[0].startswith(prefix)]
            view.run_command("insert_best_completion",  {"default": "\t", "exact": False})
            fix_completion(view, edit)
        else:
            region = sublime.Region(view.sel()[0].begin()-1, view.sel()[0].begin())
            prev_char = view.substr(region)
            try:
                prev_index = self.completions.index(prev_char)
                next_index = prev_index + 1 if prev_index < len(self.completions) - 1 else 0
                for sel in view.sel():
                    pt = sel.begin()
                    if view.substr(sublime.Region(pt-1, pt)) == prev_char:
                        view.replace(edit, sublime.Region(pt-1, pt), self.completions[next_index])
            except:
                pass


class UnicodeCompletionAutoComplete(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        view.run_command("auto_complete")
        fix_completion(view, edit)


class UnicodeCompletionCommitComplete(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        view.run_command("commit_completion")
        fix_completion(view, edit)


class ToggleUnicodeCompletion(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        view.settings().set(
            "unicode_completion",
            not view.settings().get("unicode_completion", False))
        onoff = "on" if view.settings().get("unicode_completion") else "off"
        sublime.status_message("UnicodeCompletion %s" % onoff)
