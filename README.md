# ChatGPT Calculator

This repository contains a simple command-line calculator written in Python. It supports basic arithmetic operations: addition, subtraction, multiplication, and division.

## Requirements

- Python 3.8 or newer

## Usage

Run the calculator by specifying the operation followed by two numbers:

```bash
python calculator.py add 2 3
# Output: 5.0

python calculator.py subtract 10 4
# Output: 6.0

python calculator.py multiply 1.5 4
# Output: 6.0

python calculator.py divide 8 2
# Output: 4.0
```

If division by zero is attempted, the calculator will exit with an error message.

## Development

The calculator logic lives in `calculator.py` and exposes simple functions (`add`, `subtract`, `multiply`, `divide`) along with a small CLI entry point. Feel free to extend it with more operations or integrate it into other projects.
