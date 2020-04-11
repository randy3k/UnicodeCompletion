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


class JuliaUnicodeListener(UnicodeCompletionMixin, sublime_plugin.EventListener):

    def should_complete(self, view, pt):
        if view.settings().get("unicode_completion", False):
            return True
        elif view.settings().get('is_widget') and \
                view.window().active_view().settings().get("unicode_completion", False):
            return True
        else:
            return False

    def on_query_completions(self, view, prefix, locations):
        if not self.should_complete(view, locations[0]):
            return None

        prefix = self.look_command_backward(view, locations[0])
        if not prefix:
            return None

        ret = [s for s in latex_symbols if s[0].startswith(prefix)]
        if not ret:
            ret = [s for s in emoji_symbols if s[0].startswith(prefix)]

        return normalize_completion(ret)


class ToggleUnicodeCompletion(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        view.settings().set(
            "unicode_completion",
            not view.settings().get("unicode_completion", False))
        onoff = "on" if view.settings().get("unicode_completion") else "off"
        sublime.status_message("UnicodeCompletion %s" % onoff)
