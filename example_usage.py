# example_usage.py
from mokujin_rng import Rarity, fair_roll, validate_hmac

rarities = [
    Rarity("Common", 8, ["common_sword", "common_shield", "common_helm", "common_boots", "common_gloves", "common_cloak"]),
    Rarity("Uncommon", 7, ["uncommon_ring", "uncommon_dagger", "uncommon_amulet", "uncommon_robe", "uncommon_necklace"]),
    Rarity("Rare", 6, ["rare_staff", "rare_bow"]),
    Rarity("Mythical", 5, ["mythical_blade"]),
    Rarity("Legendary", 4, ["legendary_dragon_slayer"]),
    Rarity("Immortal", 3, ["immortal_scepter"]),
    Rarity("Arcana", 2, ["arcana_void_wings"]),
    Rarity("Ancient", 1, ["ancient_eternal_flame"]),
]

server_seed = "9f8a3bd7c72b2a...f2a1c8"  # secret server seed
client_seed = "user123"                  # public client seed
nonce = 0

for i in range(5):
    result, next_server_seed = fair_roll(server_seed, client_seed, nonce, rarities)
    print(f"🎲 Roll {i + 1}: {result['rarity']} → {result['item']}")

    # Extract debug data for verification
    debug = result["debug"]
    message = f"{client_seed}:{nonce}:rarity"
    expected_hmac = debug["rarity_hmac_hex"]

    # Verify the result's fairness
    is_valid = validate_hmac(server_seed, message, expected_hmac)

    print(f"   message:     {message}")
    print(f"   rarity HMAC: {expected_hmac}")
    print(f"   ✅ Verified:  {is_valid}\n")

    # Advance for next roll
    server_seed = next_server_seed
    nonce += 1
