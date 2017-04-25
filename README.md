# UnicodeCompletion

UnicodeCompletion allows users to insert unicodes and perform the unicode lookups and conversions.

To enable UnicodeCompletion check the item `Unicode Completion Enabled` in the
Edit menu. Alternatively, it can be toggled via Command Palette: `Unicode Completion: Toggle`.

If you want to enable it for a specific syntax, edit the specific syntax settings file and
add `"unicode_completion" : true`. 

UnicodeCompletion's tab completion feature was [ported](https://github.com/JuliaEditorSupport/Julia-sublime/pull/20) to [Julia](https://github.com/JuliaEditorSupport/Julia-sublime), so Julia users should be able to use it without enabling UnicodeCompletion.

The list of unicodes is generated from
[Julia](https://github.com/JuliaLang/julia/), see [latex_symbols.jl](latex_symbols.jl) and [emoji_symbols.jl](emoji_symbols.jl). Check [Julia Docs](https://docs.julialang.org/en/latest/manual/unicode-input.html) for the complete list of supported Unicodes.

### δ Insert a LaTeX symbol:

Type `\alpha` and hit enter/tab to insert the corresponding unicode `α` to Sublime Text. Similar procedure applies to other latex symbols.

<img width="400px" src="https://cloud.githubusercontent.com/assets/1690993/25364118/e4468f9c-292d-11e7-8f32-3e55cb75edeb.png"/>

### 🍺 Insert an emoji:

Type `\:beer:` and hit enter/tab to insert the corresponding unicode 🍺 to Sublime Text. 
It is known that Sublime Text autocompletion pop up window does not show 👍 (`\:+1:`) and superscriptions (e.g., `\^2`) correctly, to insert them, they have to be typed and followed by a <kbd>tab</kbd>.

<img width="400px" src="https://cloud.githubusercontent.com/assets/1690993/25364117/e432b828-292d-11e7-914a-9c0f32d7489f.png"/>

### Unicode conversion

There are two conversion commands `Convert Selection to Unicodes` and `Convert Selection from Unicodes`. To use the conversion, just select the text which you would like to convert, and run the command.

### Lookup and Reverse lookup

It also provides commands `Unicode Lookup` and `Unicode Reverse Lookup` (can be found in Command Palette) to lookup the unicodes or the corresponding input of the unicodes under the cursor or the selection. If no unicode is detected, a full list of unicodes will be shown.

<img width="600px" src="https://cloud.githubusercontent.com/assets/1690993/25364120/e63afac2-292d-11e7-90b8-81a0c75477ae.png"/>
