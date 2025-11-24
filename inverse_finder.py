#!/usr/bin/env python3
"""
Command-line helper that attempts to compute symbolic inverse functions.

The tool accepts an expression in terms of one variable (default: x) and
solves y = f(x) for x. Multiple solutions are reported whenever the
inverse is multivalued.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Sequence

import sympy as sp
from sympy.core.sympify import SympifyError


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Solve y = f(x) for x using SymPy to obtain symbolic inverse "
            "expressions."
        )
    )
    parser.add_argument(
        "function",
        nargs="?",
        help=(
            "Expression for f(x). Provide a SymPy-compatible expression using "
            "the chosen input variable."
        ),
    )
    parser.add_argument(
        "--input-var",
        default="x",
        help="Symbol used for the original function's input (default: x).",
    )
    parser.add_argument(
        "--output-var",
        default="y",
        help="Symbol name for the function output / inverse input (default: y).",
    )
    parser.add_argument(
        "--inverse-input-var",
        default="x",
        help=(
            "Symbol used as the independent variable when expressing inverse "
            "functions (default: x)."
        ),
    )
    parser.add_argument(
        "--domain",
        choices=("real", "complex"),
        default="real",
        help=(
            "Domain to consider when falling back to solveset. "
            "Use 'complex' for a wider search space (default: real)."
        ),
    )
    return parser


def _sympify_expression(expr_str: str, input_symbol: sp.Symbol, output_symbol: sp.Symbol) -> sp.Expr:
    """Convert the raw string into a SymPy expression."""
    local_symbols = {str(input_symbol): input_symbol, str(output_symbol): output_symbol}
    return sp.sympify(expr_str, locals=local_symbols)


def _solve_for_inverse(expr: sp.Expr, input_symbol: sp.Symbol, output_symbol: sp.Symbol) -> Sequence[sp.Expr]:
    """Try solving y = f(x) for x and return all isolated solutions."""
    equation = sp.Eq(expr, output_symbol)
    solutions = sp.solve(equation, input_symbol)
    if solutions:
        return [sp.simplify(sol) for sol in solutions]
    return []


def _fallback_solveset(expr: sp.Expr, input_symbol: sp.Symbol, output_symbol: sp.Symbol, domain: str) -> sp.Set:
    """Use solveset to return an implicit solution set if solve() fails."""
    domain_set = sp.S.Reals if domain == "real" else sp.S.Complexes
    residual = sp.simplify(expr - output_symbol)
    return sp.solveset(residual, input_symbol, domain=domain_set)


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    function_expr = args.function
    if function_expr is None:
        try:
            function_expr = input("Enter f(x): ").strip()
        except EOFError:
            parser.error("A function expression is required.")
        if not function_expr:
            parser.error("A function expression is required.")

    input_symbol = sp.Symbol(args.input_var)
    output_symbol = sp.Symbol(args.output_var)
    inverse_input_symbol = sp.Symbol(args.inverse_input_var)

    try:
        expr = _sympify_expression(function_expr, input_symbol, output_symbol)
    except SympifyError as exc:
        parser.error(f"Could not parse expression: {exc}")

    solutions = _solve_for_inverse(expr, input_symbol, output_symbol)
    fallback_set = None
    if not solutions:
        fallback_set = _fallback_solveset(expr, input_symbol, output_symbol, args.domain)

    lines: List[str] = []
    lines.append(f"Function f({input_symbol}) = {sp.simplify(expr)}")
    if solutions:
        lines.append("Inverse candidate(s) reported as y(x):")
        for idx, sol in enumerate(solutions, start=1):
            formatted = sp.simplify(sol.subs(output_symbol, inverse_input_symbol))
            lines.append(f"  {idx}. {output_symbol} = {formatted}")
        lines.append(
            "Verify each branch under your domain assumptions; inverse input "
            f"variable is {inverse_input_symbol}."
        )
    else:
        lines.append(
            "SymPy could not isolate the input variable explicitly. "
            "Implicit solution set:"
        )
        lines.append(f"  {fallback_set}")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
