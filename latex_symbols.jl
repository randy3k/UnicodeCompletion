include(joinpath(JULIA_HOME, "..", "share", "julia", "base", "latex_symbols.jl"));

f = open("latex_symbols.py", "w")

println(f, "latex_symbols = [")
for (i, (α, β)) in enumerate(latex_symbols)
    print(f, "(\"", escape_string(α), "\", \"",  β, "\")")
    i < length(latex_symbols) && print(f, ",")
    println(f, "")
end
println(f, "]")

close(f)
