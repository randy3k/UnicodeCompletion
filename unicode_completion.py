import sublime
import sublime_plugin

from .unicode_mixin import UnicodeCompletionMixin
from .latex_symbols import latex_symbols
from .emoji_symbols import emoji_symbols

symbols = latex_symbols + emoji_symbols


def normalize_completion(symbols):
    return sublime.CompletionList(
            (sublime.CompletionItem(
                trigger=s[0],
                completion=s[1],
                annotation=s[1],
                kind=sublime.KIND_AMBIGUOUS)
                for s in symbols),
            flags=sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)


class UnicodeListener(UnicodeCompletionMixin, sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if not view.settings().get("unicode_completion", False):
            return None

        prefix = self.look_command_backward(view, locations[0])
        if not prefix:
            return None

        ret = [s for s in latex_symbols if s[0].startswith(prefix)]
        if not ret:
            ret = [s for s in emoji_symbols if s[0].startswith(prefix)]

        return normalize_completion(ret)

    def on_query_context(self, view, key, operator, operand, match_all):
        sel = view.sel()
        if len(sel) == 0 or not sel[0].empty():
            return

        pt = sel[0].end()

        if key == "active_view_setting.unicode_completion":
            if view.settings().get('is_widget'):
                return view.window().active_view().settings().get("unicode_completion", False)

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
            region = sublime.Region(view.sel()[0].begin()-len(prefix), view.sel()[0].begin())
            exact_match = [s[1] for s in symbols if s[0] == prefix]
            self.completions = exact_match + \
                    list(set([s[1] for s in symbols if s[0].startswith(prefix) and s[0] != prefix]))
            view.replace(edit, region, self.completions[0])
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


class ToggleUnicodeCompletion(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        view.settings().set(
            "unicode_completion",
            not view.settings().get("unicode_completion", False))
        onoff = "on" if view.settings().get("unicode_completion") else "off"
        sublime.status_message("UnicodeCompletion %s" % onoff)
