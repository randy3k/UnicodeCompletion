import re
import sublime


RE_COMMAND = re.compile(r"(\\[\^_]+[a-zA-Z0-9=+\-()]+|\\[a-zA-Z]+|\\:[_a-zA-Z0-9+\-]+:)")
RE_COMMAND_PREFIX = re.compile(
    r".*(\\[\^_]*[a-zA-Z0-9=+\-()]*|\\[a-zA-Z]*|\\:[_a-zA-Z0-9+\-]*:*)$")


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


class UnicodeCompletionMixin:
    def char_at(self, view, pt):
        return view.substr(sublime.Region(pt, pt+1))

    def find_command_forward(self, view, pt):
        col = view.rowcol(pt)[1]
        line_content = view.substr(view.line(pt))
        m = RE_COMMAND.match(line_content[col:])
        if m:
            return sublime.Region(pt, pt + len(m.group(1)))

    def look_command_forward(self, view, pt):
        ret = self.find_command_forward(view, pt)
        if ret:
            return view.substr(ret)

    def find_command_backward(self, view, pt):
        line_content = view.substr(view.line(pt))
        row, col = view.rowcol(pt)
        m = RE_COMMAND_PREFIX.match(line_content[:col])
        if m:
            return sublime.Region(pt - len(m.group(1)), pt)

    def look_command_backward(self, view, pt):
        ret = self.find_command_backward(view, pt)
        if ret:
            return view.substr(ret)

    def find_command_arround(self, view, pt):
        line_content = view.substr(view.line(pt))
        row, col = view.rowcol(pt)
        backslash_loc = line_content[:col].rfind("\\")
        if backslash_loc >= 0:
            cmd = self.find_command_forward(view, view.text_point(row, backslash_loc))
            if backslash_loc + len(cmd) >= col:
                return sublime.Region(view.text_point(row, backslash_loc),
                                      view.text_point(row, backslash_loc + len(cmd)))

    def look_command_arround(self, view, pt):
        ret = self.find_command_arround(view, pt)
        if ret:
            return view.substr(ret)

    def find_commands_in_selection(self, view, s):
        pt = s.begin()
        return [sublime.Region(sp.span()[0]+pt, sp.span()[1]+pt)
                for sp in RE_COMMAND.finditer(view.substr(s))]

    def look_commands_in_selection(self, view, s):
        return [view.substr(x) for x in self.find_commands_in_selection(view, s)]

    def iterate_commands_under_cursors(self, view):
        for s in view.sel():
            if s.empty():
                pt = s.end()
                if self.char_at(view, pt).isalpha():
                    ret = self.look_command_arround(view, pt)
                else:
                    ret = self.look_command_backward(view, pt)
                if ret:
                    yield ret
                ret = self.look_command_forward(view, pt)
                if ret:
                    yield ret
            else:
                for x in self.look_commands_in_selection(view, s):
                    yield x

    def look_unicode_forward(self, view, pt):
        char = self.char_at(view, pt)
        if not is_ascii(char):
            return char

    def look_unicode_backward(self, view, pt):
        if pt == 0:
            return
        char = self.char_at(view, pt - 1)
        if not is_ascii(char):
            return char

    def iterate_unicodes_under_cursors(self, view):
        for s in view.sel():
            if s.empty():
                pt = s.end()
                ret = self.look_unicode_backward(view, pt)
                if ret:
                    yield ret
                ret = self.look_unicode_forward(view, pt)
                if ret:
                    yield ret
            else:
                for x in view.substr(s):
                    if not is_ascii(x):
                        yield x

    def fix_completion(self, view, edit):
        for sel in view.sel():
            pt = sel.begin()
            if view.substr(sublime.Region(pt-3, pt-1)) == "\\:":
                view.replace(edit, sublime.Region(pt-3, pt-1), "")
            elif view.substr(sublime.Region(pt-4, pt-1)) == "\\:+":
                view.replace(edit, sublime.Region(pt-4, pt-1), "")
            elif view.substr(sublime.Region(pt-4, pt-1)) == "\\:-":
                view.replace(edit, sublime.Region(pt-4, pt-1), "")
