# UnicodeCompletion

Previously known as JuliaUnicode, UnicodeCompletion allows users to insert
unicodes and perform the unicode lookup and reverse lookup.

Julia REPL has a very nice way to insert Unicode characters (both latex and emoji symbols). This package brings the same feature to Sublime Text. 

To enable UnicodeCompletion check the item `Unicode Completion Enabled` in the
Edit menu. Alternatively, it can be toggled via Command Palette. If you want
to enable it for a specific syntax, edit the specific syntax settings file and
add `"unicode_completion" : true`. 

UnicodeCompletion is [ported](https://github.com/JuliaEditorSupport/Julia-sublime/pull/20)
to [Julia](https://github.com/JuliaEditorSupport/Julia-sublime), so Julia users
should be able to use it without installing UnicodeCompletion.

The list of unicodes is generated from
[Julia](https://github.com/JuliaLang/julia/), see [latex_symbols.jl](latex_symbols.jl) and [emoji_symbols.jl](emoji_symbols.jl). 

Check [Julia Docs](http://docs.julialang.org/en/latest/manual/unicode-input/) for the complete list of supported Unicodes.

### Insert LaTeX symbol δ:

Type `\alpha` and hit enter/tab to insert the corresponding unicode `α` to Sublime Text. Similar to other latex symbols.

<img width="400px", src="latex.png"/>

### Insert Emoji 🍺:

Type `\:beer:` and hit enter/tab to insert the corresponding unicode 🍺 to Sublime Text. 
It is known that Sublime Text autocompletion pop up window does not show 👍 (`\:+1:`) and superscriptions (e.g., `\^2`) correctly, to insert them, they have to be exactly typed and followed by a <kbd>tab</kbd>.

<img width="400px", src="beers.png"/>

### Lookup and Reverse lookup

It also provides commands `Unicode Lookup` and `Unicode Reverse Lookup` (can be found in Command Palette) to lookup the unicodes or the corresponding input of the unicodes under the cursor or the selection. If no unicode is detected, a input prompt will be shown to ask for a unicode.

<img width="600px", src="reverse.png"/>
