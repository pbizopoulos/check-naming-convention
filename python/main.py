import unittest
from pathlib import Path

from python.main import naming_convention


class Tests(unittest.TestCase):
    def test_naming_convention(self: "Tests") -> None:
        with Path("prm/sample.py").open(encoding="utf-8") as file:
            naming_convention(file)


if __name__ == "__main__":
    unittest.main()
