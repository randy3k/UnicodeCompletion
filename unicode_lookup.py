import sublime
import sublime_plugin

from .unicode_mixin import UnicodeCompletionMixin
from .latex_symbols import latex_symbols
from .emoji_symbols import emoji_symbols


def unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


class UnicodeCompletionLookup(UnicodeCompletionMixin, sublime_plugin.TextCommand):
    def run(self, edit):
        cmds = unique(self.iterate_commands_under_cursors(self.view))
        if cmds:
            _latex_symbols = [s for c in cmds for s in latex_symbols if c == s[0]]
            _emoji_symbols = [s for c in cmds for s in emoji_symbols if c == s[0]]
        else:
            _latex_symbols = latex_symbols
            _emoji_symbols = emoji_symbols

        symbols = _latex_symbols + _emoji_symbols
        if len(symbols) == 0 or not cmds:
            sublime.status_message("No unicode matches were found.")

        def copycallback(action):
            if action >= 0:
                sublime.set_clipboard(symbols[action][1])

        l = [["%s: %s" % (s[1], s[0]), "Copy Unicode to Clipboard"] for s in _latex_symbols]
        l += [["%s: %s" % (s[1], s[0]), "Copy Unicode to Clipboard"] for s in _emoji_symbols]

        self.view.window().show_quick_panel(l, copycallback)


class UnicodeCompletionReverseLookup(UnicodeCompletionMixin, sublime_plugin.TextCommand):
    def run(self, edit):
        unicodes = unique(self.iterate_unicodes_under_cursors(self.view))

        if unicodes:
            _latex_symbols = [s for u in unicodes for s in latex_symbols if u == s[1]]
            _emoji_symbols = [s for u in unicodes for s in emoji_symbols if u == s[1]]
        else:
            _latex_symbols = latex_symbols
            _emoji_symbols = emoji_symbols

        symbols = _latex_symbols + _emoji_symbols

        if len(symbols) == 0 or not unicodes:
            sublime.status_message("No matches were found.")

        def copycallback(action):
            if action >= 0:
                sublime.set_clipboard(symbols[action][0])

        l = [["%s: %s" % (s[1], s[0]), "Copy LaTeX to Clipboard"] for s in _latex_symbols]
        l += [["%s: %s" % (s[1], s[0]), "Copy Emoji to Clipboard"] for s in _emoji_symbols]

        self.view.window().show_quick_panel(l, copycallback)
