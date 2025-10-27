# __init__.py
"""
mokujin_rng — a lightweight, provably fair RNG rarity system.
"""

__version__ = "1.0.0"
__author__ = "laasilva"
__email__ = "laasilva@proton.me"
__license__ = "LGPL v3"

from .rarity import Rarity
from .fair_roll import fair_roll, validate_hmac, build_message

__all__ = ["Rarity", "fair_roll", "validate_hmac", "build_message"]

