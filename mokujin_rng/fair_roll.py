from mokujin_rng.rarity import Rarity

import hmac, hashlib

from typing import Tuple, Dict, List

def hmac_hex(key: str, message: str) -> str:
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()


def hmac_bytes(key: str, message: str) -> bytes:
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).digest()


def sha256_hex(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def seed_chain_advance(server_seed: str) -> str:
    return sha256_hex(server_seed)


def fair_roll(
    server_seed: str,
    client_seed: str,
    nonce: int,
    rarities: List[Rarity],
    advance_server_seed: bool = True,
) -> Tuple[Dict, str]:
    """
    Perform a provably-fair roll (rarity + item) using HMAC-SHA256 and advance the server seed.

    Args:
        server_seed: current secret server seed (hex or string)
        client_seed: public client seed
        nonce: counter for uniqueness
        rarities: list of Rarity objects
        advance_server_seed: if True, compute and return the next server seed (SHA256(current))

    Returns:
        (result_dict, next_server_seed)
        - result_dict contains 'rarity', 'item', and 'debug' info (including HMAC hexes).
        - next_server_seed is the advanced server seed (or same as current if advance_server_seed=False)
    """
    if not rarities:
        raise ValueError("rarities must be a non-empty list")

    total_weight = sum(r.weight for r in rarities)
    if total_weight <= 0:
        raise ValueError("Sum of weights must be positive")

    rarity_msg = f"{client_seed}:{nonce}:rarity"
    rarity_hmac_bytes = hmac_bytes(server_seed, rarity_msg)
    rarity_hmac_hex = rarity_hmac_bytes.hex()
    rarity_value = int.from_bytes(rarity_hmac_bytes[:4], "big")
    rarity_roll = rarity_value % total_weight

    cumulative = 0
    chosen_rarity = None
    for rarity in rarities:
        cumulative += rarity.weight
        if rarity_roll < cumulative:
            chosen_rarity = rarity
            break

    if chosen_rarity is None:
        # Defensive: should not happen
        raise RuntimeError("Failed to select a rarity from weights")

    # Item selection HMAC: use same server seed but different message to avoid correlation
    item_msg = f"{client_seed}:{nonce}:item"
    item_hmac_bytes = hmac_bytes(server_seed, item_msg)
    item_hmac_hex = item_hmac_bytes.hex()
    item_value = int.from_bytes(item_hmac_bytes[:4], "big")
    # handle case of empty item pool defensively
    if not chosen_rarity.items:
        chosen_item = None
    else:
        item_index = item_value % len(chosen_rarity.items)
        chosen_item = chosen_rarity.items[item_index]

    # Advance server seed for the next roll (optional based on flag)
    next_server_seed = seed_chain_advance(server_seed) if advance_server_seed else server_seed

    result = {
        "rarity": chosen_rarity.name,
        "item": chosen_item,
        "debug": {
            "server_seed_used": server_seed,
            "client_seed": client_seed,
            "nonce": nonce,
            "rarity_msg": rarity_msg,
            "rarity_hmac_hex": rarity_hmac_hex,
            "rarity_value": rarity_value,
            "rarity_roll": rarity_roll,
            "selected_rarity_weight": chosen_rarity.weight,
            "item_msg": item_msg,
            "item_hmac_hex": item_hmac_hex,
            "item_value": item_value,
            "item_index": (None if not chosen_rarity.items else item_index),
            "items_in_rarity": len(chosen_rarity.items),
            "total_weight": total_weight,
        },
    }

    return result, next_server_seed

def validate_hmac(secret_key: str, message: str, expected_hmac: str) -> bool:
    return hmac.compare_digest(
        expected_hmac,
        hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
    )

def build_message(client_seed: str, nonce: int, category: str) -> str:
    return f"{client_seed}:{nonce}:{category}"