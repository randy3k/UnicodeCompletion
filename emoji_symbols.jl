include(joinpath(JULIA_HOME, "..", "share", "julia", "base", "emoji_symbols.jl"));

f = open("emoji_symbols.py", "w")

println(f, "emoji_symbols = [")
for (i, (α, β)) in enumerate(emoji_symbols)
    print(f, "(\"", escape_string(α), "\", \"",  β, "\")")
    i < length(emoji_symbols) && print(f, ",")
    println(f, "")
end
println(f, "]")

close(f)
