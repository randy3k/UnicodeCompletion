### Julia-Unicode

This is a simple package to insert Unicode characters (both latex and emoji symbols) to Julia as in Julia REPL.
For some reasons, [Julia Completions](https://github.com/jakeconnor/JuliaCompletions) doesn't quite
work for me and [UnicodeMath](https://github.com/mvoidex/UnicodeMath)
keymapping is different from Julia (e.g., `\epsilon` and `\varepsilon`), so I
created this package.
The list of unicodes is copied from
[Julia](https://github.com/JuliaLang/julia/), check [latex_symbols.jl](latex_symbols.jl) and [emoji_symbols.jl](emoji_symbols.jl). 

#### Usage:

Type `\alpha` and hit enter/tab to insert the corresponding unicode `α` to Sublime Text. Similar to other unicodes.

<img width="400px", src="shot.png"/>


#### Known issues for emoji:

It is known that there is a bug in handling emoji. For example, when you hit
enter while trying to insert `🍰` via `\:cake:`, the text `\:` is not replaced.
It could probably be fixed by defining custom tab completion keybind. A
workaround for now is to type the full text `\:cake:` and then trigger
`auto_complete` (<kbd>ctrl+space</kbd> for Mac and Windows, <kbd>alt+/</kbd>
for Linux).
