import sublime
import sublime_plugin
import re
from .latex_symbols import latex_symbols
from .emoji_symbols import emoji_symbols


CONTAINS_COMPLETIONS = re.compile(r".*(\\[:_0-9a-zA-Z+-^]*)$")
symbols = latex_symbols + emoji_symbols


def get_command(view):
    sel = view.sel()[0]
    pt = sel.end()
    line = view.substr(sublime.Region(view.line(pt).begin(), pt))
    m = CONTAINS_COMPLETIONS.match(line)
    if m:
        return m.group(1)
    else:
        return None


def julia_unicode_can_complete(view, exact=True):
    c = get_command(view)
    if not c:
        return False
    if not exact:
        return True

    for s in symbols:
        if c == s[0]:
            return True

    return False


class JuliaUnicodeListener(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        if view.settings().get('is_widget'):
            return
        if not view.match_selector(locations[0], "source.julia"):
            return None

        ploc = locations[0]-len(prefix)
        if view.substr(sublime.Region(ploc-1, ploc)) == "\\":
            prefix = view.substr(sublime.Region(ploc-1, locations[0]))
        elif view.substr(sublime.Region(ploc-2, ploc)) == "\\^":
            prefix = view.substr(sublime.Region(ploc-1, locations[0]))
        elif view.substr(sublime.Region(ploc-2, ploc)) == "\\:":
            prefix = view.substr(sublime.Region(ploc-2, locations[0]))
        elif view.substr(sublime.Region(ploc-1, ploc)) == ":":
            pt = view.word(ploc-2).begin()
            prefix = view.substr(sublime.Region(pt-2, locations[0]))
        else:
            return None
        if not prefix:
            return None
        return [(s[0] + "\t" + s[1], prefix, s[1]) for s in symbols if prefix in s[0]]

    def on_query_context(self, view, key, operator, operand, match_all):
        if view.settings().get('is_widget'):
            return
        point = view.sel()[0].end() if view.sel() else 0
        if not view.match_selector(point, "source.julia"):
            return None

        if key == 'julia_unicode_is_completed':
            return julia_unicode_can_complete(view, True) == operand
        elif key == 'julia_unicode_can_complete':
            return julia_unicode_can_complete(view, False) == operand

        return None


class JuliaUnicodeInsertBestCompletion(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        view.run_command("insert_best_completion",  {"default": "\t", "exact": False})
        pt = view.sel()[0].begin()
        if view.substr(sublime.Region(pt-3, pt-1)) == "\\:":
            view.replace(edit, sublime.Region(pt-3, pt-1), "")


class JuliaUnicodeCommitComplete(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        view.run_command("commit_completion")
        pt = view.sel()[0].begin()
        if view.substr(sublime.Region(pt-3, pt-1)) == "\\:":
            view.replace(edit, sublime.Region(pt-3, pt-1), "")


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


class JuliaUnicodeReverseLookup(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        sel = view.sel()[0]
        if sel.empty():
            pt = sel.end()
            chars = view.substr(sublime.Region(pt, pt+1))
            if chars and is_ascii(chars):
                chars = view.substr(sublime.Region(pt-1, pt))
                if chars and is_ascii(chars):
                    chars = ""
        else:
            chars = view.substr(sel)
        view.window().show_input_panel("Unicode: ", chars, self.callback, None, None)

    def get_string(self, chars):
        for s in symbols:
            if chars == s[1]:
                return s[0]
        return None

    def callback(self, chars):
        results = []
        for char in chars:
            if not is_ascii(char):
                s = self.get_string(char)
                if s:
                    results = results + [(char, s)]

        def copycallback(action):
            if action == 0:
                sublime.set_clipboard(results[action][1])

        display = [["%s: %s" % r, "Copy to Clipboard"] for r in results]

        self.view.window().show_quick_panel(display, copycallback)
