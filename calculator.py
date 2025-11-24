"""Simple command-line calculator supporting basic operations."""

import argparse
from typing import Callable, Dict

Operation = Callable[[float, float], float]


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b


OPERATIONS: Dict[str, Operation] = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Primitive calculator that performs basic arithmetic operations."
    )
    parser.add_argument(
        "operation",
        choices=OPERATIONS.keys(),
        help="Operation to perform (add, subtract, multiply, divide).",
    )
    parser.add_argument("a", type=float, help="First operand.")
    parser.add_argument("b", type=float, help="Second operand.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    operation = OPERATIONS[args.operation]

    try:
        result = operation(args.a, args.b)
    except ValueError as exc:
        raise SystemExit(str(exc))

    print(result)


if __name__ == "__main__":
    main()
