import sublime
import sublime_plugin

from .unicode_mixin import UnicodeCompletionMixin
from .latex_symbols import latex_symbols
from .emoji_symbols import emoji_symbols


class UnicodeCompletionConvertToUnicodes(UnicodeCompletionMixin, sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        for s in reversed(view.sel()):
            if s.empty():
                pt = s.begin()
                r = self.find_command_arround(view, pt)
                if r:
                    self.convert_region(edit, r)
            else:
                rs = reversed(self.find_commands_in_selection(view, s))
                for r in rs:
                    self.convert_region(edit, r)

    def convert_region(self, edit, r):
        view = self.view
        m = self.find_match(view.substr(r))
        if m:
            self.view.replace(edit, r, "")
            self.view.insert(edit, r.begin(), m)

    def find_match(self, text):
        for l in [latex_symbols, emoji_symbols]:
            for s in l:
                if text == s[0]:
                    return s[1]


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


class UnicodeCompletionConvertFromUnicodes(UnicodeCompletionMixin, sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        for s in reversed(view.sel()):
            if s.empty():
                pt = s.begin()
                self.convert_region(edit, sublime.region(pt-1, pt))
            else:
                b = s.begin()
                pts = reversed([i for i, c in enumerate(view.substr(s)) if not is_ascii(c)])
                for pt in pts:
                    self.convert_region(edit, sublime.Region(b+pt, b+pt+1))

    def convert_region(self, edit, r):
        view = self.view
        m = self.find_match(view.substr(r))
        if m:
            self.view.replace(edit, r, "")
            self.view.insert(edit, r.begin(), m)

    def find_match(self, text):
        for l in [latex_symbols, emoji_symbols]:
            for s in l:
                if text == s[1]:
                    return s[0]
