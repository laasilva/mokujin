import unittest
from mokujin_rng.fair_roll import (
    hmac_hex,
    hmac_bytes,
    sha256_hex,
    seed_chain_advance,
    fair_roll,
)
from mokujin_rng.rarity import Rarity

class TestFairRoll(unittest.TestCase):
    def setUp(self):
        # Set up common test data
        self.server_seed = "mysecretserverseed123"
        self.client_seed = "publicclientseed456"
        self.nonce = 1
        
        # Create some test rarities
        self.common = Rarity("Common", 70, ["Item1", "Item2", "Item3"])
        self.rare = Rarity("Rare", 25, ["RareItem1", "RareItem2"])
        self.legendary = Rarity("Legendary", 5, ["LegendaryItem"])
        self.rarities = [self.common, self.rare, self.legendary]

    def test_hmac_hex(self):
        result = hmac_hex("key", "message")
        # HMAC should be consistent and match expected length
        self.assertEqual(len(result), 64)  # SHA256 produces 32 bytes = 64 hex chars
        # Test consistency
        self.assertEqual(result, hmac_hex("key", "message"))

    def test_hmac_bytes(self):
        result = hmac_bytes("key", "message")
        # Should return bytes of correct length
        self.assertEqual(len(result), 32)  # SHA256 produces 32 bytes
        # Test consistency
        self.assertEqual(result, hmac_bytes("key", "message"))

    def test_sha256_hex(self):
        result = sha256_hex("test")
        # SHA256 should be consistent and match expected length
        self.assertEqual(len(result), 64)
        # Test consistency
        self.assertEqual(result, sha256_hex("test"))

    def test_seed_chain_advance(self):
        seed = "initial_seed"
        next_seed = seed_chain_advance(seed)
        # Should return different value
        self.assertNotEqual(seed, next_seed)
        # Should be consistent
        self.assertEqual(next_seed, seed_chain_advance(seed))
        # Should be hex string of correct length
        self.assertEqual(len(next_seed), 64)

    def test_fair_roll_basic(self):
        result, next_seed = fair_roll(
            self.server_seed,
            self.client_seed,
            self.nonce,
            self.rarities
        )
        
        # Check structure of result
        self.assertIsInstance(result, dict)
        self.assertIn("rarity", result)
        self.assertIn("item", result)
        self.assertIn("debug", result)
        
        # Verify debug info
        debug = result["debug"]
        self.assertEqual(debug["server_seed_used"], self.server_seed)
        self.assertEqual(debug["client_seed"], self.client_seed)
        self.assertEqual(debug["nonce"], self.nonce)

        # Check next seed
        self.assertEqual(next_seed, seed_chain_advance(self.server_seed))

    def test_fair_roll_empty_rarities(self):
        with self.assertRaises(ValueError):
            fair_roll(self.server_seed, self.client_seed, self.nonce, [])

    def test_fair_roll_zero_weights(self):
        zero_rarities = [Rarity("Zero", 0, ["Item"])]
        with self.assertRaises(ValueError):
            fair_roll(self.server_seed, self.client_seed, self.nonce, zero_rarities)

    def test_fair_roll_empty_items(self):
        empty_rarity = Rarity("Empty", 1, [])
        result, _ = fair_roll(
            self.server_seed,
            self.client_seed,
            self.nonce,
            [empty_rarity]
        )
        self.assertIsNone(result["item"])

    def test_fair_roll_no_advance(self):
        result, next_seed = fair_roll(
            self.server_seed,
            self.client_seed,
            self.nonce,
            self.rarities,
            advance_server_seed=False
        )
        # Server seed should not change
        self.assertEqual(next_seed, self.server_seed)

    def test_fair_roll_distribution(self):
        # Basic distribution test with many rolls
        rolls = 1000
        counts = {"Common": 0, "Rare": 0, "Legendary": 0}
        
        for i in range(rolls):
            result, seed = fair_roll(
                self.server_seed,
                self.client_seed,
                i,  # use i as nonce
                self.rarities
            )
            counts[result["rarity"]] += 1
        
        # Check if distribution roughly matches weights
        # Allow for some variance due to randomness
        total_weight = sum(r.weight for r in self.rarities)
        for rarity in self.rarities:
            expected = (rarity.weight / total_weight) * rolls
            actual = counts[rarity.name]
            # Allow for 20% deviation
            self.assertTrue(
                abs(actual - expected) < (expected * 0.2),
                f"Distribution test failed for {rarity.name}. "
                f"Expected ~{expected:.0f}, got {actual}"
            )

if __name__ == '__main__':
    unittest.main()