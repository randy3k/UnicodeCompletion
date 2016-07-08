import sublime
import sublime_plugin
import re
from .latex_symbols import latex_symbols

class LatexPlusAutoCompletions(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        if not view.match_selector(locations[0], "source.julia"):
            return None
        if not prefix:
            return
        ploc = locations[0]-len(prefix)
        if view.substr(sublime.Region(ploc-1, ploc)) != "\\" and \
                view.substr(sublime.Region(ploc-2, ploc)) != "\\^":
            return None
        return [(s[0] + "\t" + s[1], "", s[1] ) for s in latex_symbols if prefix in s[0]]
