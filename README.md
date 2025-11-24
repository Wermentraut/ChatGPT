# ChatGPT

## inverse_finder.py

Symbolically inverts elementary functions with SymPy.

### Usage

```bash
python inverse_finder.py "x**2 + 3" --input-var x --output-var y
```

Example output:

```
Function f(x) = x**2 + 3
Inverse candidate(s) reported as y(x):
  1. y = -sqrt(x - 3)
  2. y = sqrt(x - 3)
Verify each branch under your domain assumptions; inverse input variable is x.
```

Options (script will prompt for the expression if omitted):

- `--input-var`: variable used in the original expression.
- `--output-var`: symbol that will represent the input of the inverse function.
- `--inverse-input-var`: which symbol to use for the inverse function's input (default: `x`).
- `--domain`: `real` (default) or `complex` for the fallback solver.
