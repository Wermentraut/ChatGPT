"""
Riemann zeta approximation for real and complex inputs.
- Uses the Dirichlet eta series for Re(s) > 0 (and s != 1).
- Provides exact values for non-positive integers via Bernoulli numbers.
- For negative non-integers, falls back to the eta series (limited accuracy).
"""

import argparse
import math
from typing import Iterable, List, Union

Number = Union[float, complex]

# Bernoulli numbers B_n for n up to 20 (odd n > 1 are zero).
BERNOULLI = {
    0: 1.0,
    1: -0.5,
    2: 1.0 / 6.0,
    4: -1.0 / 30.0,
    6: 1.0 / 42.0,
    8: -1.0 / 30.0,
    10: 5.0 / 66.0,
    12: -691.0 / 2730.0,
    14: 7.0 / 6.0,
    16: -3617.0 / 510.0,
    18: 43867.0 / 798.0,
    20: -174611.0 / 330.0,
}


def riemann_zeta(
    s: Number, max_terms: int = 200_000, tolerance: float = 1e-12
) -> complex:
    """
    Compute zeta(s) for real or complex s using the Dirichlet eta series.

    Args:
        s: Real or complex input.
        max_terms: Hard cap on series terms to avoid infinite loops.
        tolerance: Stop early when the current term is smaller than this.

    Returns:
        Complex value approximating zeta(s). Returns math.inf for s == 1.
    """
    if s == 1:
        return math.inf

    s_c = complex(s)

    # Exact values for negative integers (and s=0) via Bernoulli numbers.
    if abs(s_c.imag) < 1e-12:
        r = s_c.real
        if r <= 0 and abs(r - round(r)) < 1e-12:
            n = int(round(r))
            if n == 0:
                return complex(-0.5)
            if n < 0:
                m = -n
                b_index = m + 1
                if b_index in BERNOULLI:
                    return complex(-BERNOULLI[b_index] / (m + 1))
                # Odd Bernoulli numbers above 1 are zero, giving zeta(-even) = 0.
                if b_index % 2 == 1:
                    return complex(0.0)

    s = s_c
    eta = 0.0j

    for k in range(1, max_terms + 1):
        term = ((-1) ** (k - 1)) / (k**s)
        eta += term
        if abs(term) < tolerance:
            break

    denom = 1 - (2 ** (1 - s))
    if abs(denom) < 1e-16:
        return math.inf

    return eta / denom


def demo_samples(values: Iterable[Number]) -> None:
    """Print zeta(s) for a list of sample values."""
    for s in values:
        val = riemann_zeta(s)
        print(f"zeta({s}) ~ {val}")


def parse_values(args: List[str]) -> List[Number]:
    """Parse CLI inputs into complex numbers (real accepted too)."""
    parsed: List[Number] = []
    for raw in args:
        if raw == "&":
            # Ignore stray ampersands that can appear when pasting a shell line.
            continue
        try:
            parsed.append(complex(raw))
        except ValueError as exc:
            raise SystemExit(f"Cannot parse '{raw}' as a number/complex: {exc}")
    return parsed


def main(argv: List[str]) -> None:
    parser = argparse.ArgumentParser(
        description="Compute Riemann zeta(s) for given values (real or complex). "
        "Complex numbers use Python's syntax, e.g. 0.5+14j"
    )
    parser.add_argument(
        "values",
        nargs="*",
        help="Values of s (real like 2.0 or complex like 0.5+14j). "
        "If omitted, prints a built-in demo set.",
    )
    parser.add_argument(
        "--max-terms",
        type=int,
        default=200_000,
        help="Maximum series terms to sum (default: 200000)",
    )
    parser.add_argument(
        "--tol",
        type=float,
        default=1e-12,
        help="Early-stop tolerance for series term magnitude (default: 1e-12)",
    )

    opts = parser.parse_args(argv)

    if opts.values:
        values = parse_values(opts.values)
    else:
        raw = input(
            "Enter s values separated by space (real or complex like 0.5+14j). "
            "Leave empty for demo set: "
        ).strip()
        if raw:
            values = parse_values(raw.split())
        else:
            values = [
                2,  # zeta(2) = pi^2 / 6
                4,  # zeta(4) = pi^4 / 90
                0,  # analytic continuation gives -1/2
                -1,  # analytic continuation gives -1/12
                0.5,
                2 + 3j,
                0.5 + 14j,
            ]
            print("Riemann zeta values (Dirichlet eta approximation):")

    for s in values:
        val = riemann_zeta(s, max_terms=opts.max_terms, tolerance=opts.tol)
        print(f"zeta({s}) ~ {val}")

    if not opts.values:
        print("\nReference checks:")
        print(f"pi^2 / 6 ~ {math.pi ** 2 / 6}")
        print(f"pi^4 / 90 ~ {math.pi ** 4 / 90}")


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
