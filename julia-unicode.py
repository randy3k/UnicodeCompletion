import sublime
import sublime_plugin
import re
from .latex_symbols import latex_symbols
from .emoji_symbols import emoji_symbols

class LatexPlusAutoCompletions(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        if not view.match_selector(locations[0], "source.julia"):
            return None
        if not prefix:
            return
        ploc = locations[0]-len(prefix)
        if view.substr(sublime.Region(ploc-1, ploc)) == "\\":
            prefix = view.substr(sublime.Region(ploc-1, locations[0]))
        elif view.substr(sublime.Region(ploc-2, ploc)) == "\\^":
            prefix = view.substr(sublime.Region(ploc-1, locations[0]))
        elif view.substr(sublime.Region(ploc-2, ploc)) == "\\:":
            prefix = view.substr(sublime.Region(ploc-1, locations[0]))

        r = latex_symbols + emoji_symbols
        return [(s[0] + "\t" + s[1], s[1], s[1] ) for s in r if prefix in s[0]]
