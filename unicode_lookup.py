import sublime
import sublime_plugin
import re

from .unicode_completion import latex_symbols, emoji_symbols


RE_COMMAND = re.compile(r"(\\[a-zA-Z]*|\\:[_0-9a-zA-Z+-^]*:)")
RE_COMMAND_PREFIX = re.compile(r".*(\\[a-zA-Z]*|\\:[_0-9a-zA-Z+-^]*:)$")


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


class UnicodeCompletionLookup(sublime_plugin.TextCommand):
    def run(self, edit):
        cmds = [c for c in self.find_command_under_cursor()]
        cmds = list(set(cmds))
        self.show_list(cmds)

    def char_at(self, pt):
        return self.view.substr(sublime.Region(pt, pt+1))

    def look_forward(self, pt):
        view = self.view
        col = view.rowcol(pt)[1]
        line_content = view.substr(view.line(pt))
        m = RE_COMMAND.match(line_content[col:])
        if m:
            return m.group(1)

    def look_backward(self, pt):
        view = self.view
        line_content = view.substr(view.line(pt))
        col = view.rowcol(pt)[1]
        m = RE_COMMAND_PREFIX.match(line_content[:col])
        if m:
            return m.group(1)

    def look_arround(self, pt):
        view = self.view
        line_content = view.substr(view.line(pt))
        row, col = view.rowcol(pt)
        backslash_loc = line_content[:col].find("\\")
        if backslash_loc >= 0:
            return self.look_forward(view.text_point(row, backslash_loc))

    def find_command_under_cursor(self):
        view = self.view
        for s in view.sel():
            if s.empty():
                pt = s.end()
                if self.char_at(pt).isalpha():
                    ret = self.look_arround(pt)
                else:
                    ret = self.look_backward(pt)
                if ret:
                    yield ret
                ret = self.look_forward(pt)
                if ret:
                    yield ret
            else:
                for x in RE_COMMAND.findall(view.substr(s)):
                    yield x

    def show_list(self, cmds):
        if cmds:
            _latex_symbols = [s for s in latex_symbols if s[0] in cmds]
            _emoji_symbols = [s for s in emoji_symbols if s[0] in cmds]
        else:
            _latex_symbols = latex_symbols
            _emoji_symbols = emoji_symbols

        symbols = _latex_symbols + _emoji_symbols

        if len(symbols) == 0:
            sublime.status_message("No unicode matches were found.")

        def copycallback(action):
            if action >= 0:
                sublime.set_clipboard(symbols[action][1])

        l = [["%s: %s" % (s[1], s[0]), "Copy Unicode to Clipboard"] for s in _latex_symbols]
        l += [["%s: %s" % (s[1], s[0]), "Copy Unicode to Clipboard"] for s in _emoji_symbols]

        self.view.window().show_quick_panel(l, copycallback)


class UnicodeCompletionReverseLookup(sublime_plugin.TextCommand):
    def run(self, edit):
        unicodes = [c for c in self.find_unicode_under_cursor()]
        unicodes = list(set(unicodes))
        self.show_list(unicodes)

    def char_at(self, pt):
        return self.view.substr(sublime.Region(pt, pt+1))

    def look_forward(self, pt):
        char = self.char_at(pt)
        if not is_ascii(char):
            return char

    def look_backward(self, pt):
        if pt == 0:
            return
        char = self.char_at(pt - 1)
        if not is_ascii(char):
            return char

    def find_unicode_under_cursor(self):
        view = self.view
        for s in view.sel():
            if s.empty():
                pt = s.end()
                ret = self.look_backward(pt)
                if ret:
                    yield ret
                ret = self.look_forward(pt)
                if ret:
                    yield ret
            else:
                for x in view.substr(s):
                    if not is_ascii(x):
                        yield x

    def show_list(self, unicodes):

        if unicodes:
            _latex_symbols = [s for s in latex_symbols if s[1] in unicodes]
            _emoji_symbols = [s for s in emoji_symbols if s[1] in unicodes]
        else:
            _latex_symbols = latex_symbols
            _emoji_symbols = emoji_symbols

        symbols = _latex_symbols + _emoji_symbols

        if len(symbols) == 0:
            sublime.status_message("No matches were found.")

        def copycallback(action):
            if action >= 0:
                sublime.set_clipboard(symbols[action][0])

        l = [["%s: %s" % (s[1], s[0]), "Copy LaTeX to Clipboard"] for s in _latex_symbols]
        l += [["%s: %s" % (s[1], s[0]), "Copy Emoji to Clipboard"] for s in _emoji_symbols]

        self.view.window().show_quick_panel(l, copycallback)
