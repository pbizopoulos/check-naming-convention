import unittest
from pathlib import Path

from python.main import check_naming_convention


class Tests(unittest.TestCase):
    def test_function(self: "Tests") -> None:
        with Path("prm/test_function.py").open(encoding="utf-8") as file:
            check_naming_convention(file)

    def test_variable(self: "Tests") -> None:
        with Path("prm/test_variable.py").open(encoding="utf-8") as file:
            check_naming_convention(file)


if __name__ == "__main__":
    unittest.main()
