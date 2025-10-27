
# 🎲 Mokujin RNG

**Mokujin RNG** is a simple, *provably fair* random generation library in Python —

built for game loot tables, rarity draws, and any weighted selection system where fairness matters.

It uses **HMAC-SHA256** and a **server seed chain** to guarantee transparency and prevent tampering.

## 📦 Installation

Clone or download the project and install locally:

```bash

git  clone  https://github.com/yourusername/mokujin_rng.git

cd  mokujin_rng

pip  install  -e  .

````

This  installs  it  in  “editable”  mode  so  you  can  import  it  locally.

## 📘 Example Usage

A  complete,  ready-to-run  example  is  included  in [`example_usage.py`](./example_usage.py).

Run  it  directly  to  see  the  system  in  action:
```bash

python example_usage.py

```
The example demonstrates how to:

* Define a list of rarities (each with weights and item pools)
* Perform multiple provably fair rolls
* Verify each roll’s HMAC for fairness
* Advance the server seed after every roll

Expected output:

```bash

🎲 Roll 1: Uncommon → uncommon_amulet
   message:     user123:0:rarity
   rarity HMAC: aa05ec5f10490382991517b5017348d13b970fdcb11090ef59cbc0b4cc2e32d3
   ✅ Verified:  True

🎲 Roll 2: Uncommon → uncommon_necklace
   message:     user123:1:rarity
   rarity HMAC: becab0df897c7d1a6347a16d22ef0d3f7520a021524eb45ec0069fc03bacc940
   ✅ Verified:  True

🎲 Roll 3: Rare → rare_staff
   message:     user123:2:rarity
   rarity HMAC: 3f75cbf762310a1c3073d6e39f8bc112464602ad1334e90ead5dfa6d91d60725
   ✅ Verified:  True

🎲 Roll 4: Rare → rare_bow
   message:     user123:3:rarity
   rarity HMAC: 6b0970651791c0cc67e586f273b355ffa68c8fec6d734c40fe38ec02cc886664
   ✅ Verified:  True

🎲 Roll 5: Legendary → legendary_dragon_slayer
   message:     user123:4:rarity
   rarity HMAC: d52a2609787f0d02c5945f32b45531f9132855cb0024af74f8099b56f723083f
   ✅ Verified:  True

```

## 🔎 Independent Verification Example

When a roll is made, you can later **reveal the server seed** so anyone can verify fairness.

Here’s how a player or third party can confirm a result:

```python

from mokujin_rng import validate_hmac

# Publicly shared data after the roll

revealed_server_seed =  "9f8a3bd7c72b2a...f2a1c8"
client_seed =  "user123"
nonce =  0
expected_rarity_hmac =  "8b5d0d...b13f4e"

# Rebuild the original message used during the roll

message =  f"{client_seed}:{nonce}:rarity"

# Verify integrity

is_valid =  validate_hmac(revealed_server_seed, message, expected_rarity_hmac)

print("Fair result:", is_valid)

```

If this prints `True`, it proves the roll was generated with the exact same inputs and algorithm,

ensuring **no tampering** — pure math-backed fairness. 🧮

## ⚙️ How It Works

Each roll uses a cryptographic HMAC to select rarity and item:

```

HMAC_SHA256(server_seed, f"{client_seed}:{nonce}:rarity")

```
### Components

| Parameter       | Description                                                           |
|-----------------|------------------------------------------------------------------------|
| **Server Seed** | Secret seed known only to the server; revealed later for verification. |
| **Client Seed** | Public seed chosen by the user or session.                             |
| **Nonce**       | Counter that increments for each roll.                                 |
| **HMAC**        | One-way hash ensuring deterministic, tamper-proof fairness.            |


After each roll, the server can **advance its seed** to prevent reverse-engineering past results:
```

next_server_seed = SHA256(current_server_seed)

```

This maintains verifiability without compromising future randomness.

## 📁 Project Structure
A minimal example structure:
```
mokujin/
	└── mokujin_rng/
			├── __init__.py
			├── rarity.py
			├── fair_roll.py
			├── example_usage.py
			├── LICENSE
			└── README.md
	└── tests/
			├── fair_roll_tests.py

```

  

You can import it in your Python code like:

  

```python

from mokujin_rng import Rarity, fair_roll, validate_hmac

```
---

## 🧩 License

Licensed under the **LGPL-3.0** license.

You’re free to use, modify, and share improvements —

as long as derivative works remain under the same license.

See [LICENSE](./LICENSE) for full terms.

## 💡 Notes
* Requires **Python ≥ 3.8**
* Works entirely **offline**
* Deterministic and reproducible results
* Ideal for:
	* 🎮 Game loot systems
	* 🎲 Weighted random draws
	* 🧠 Simulations or controlled randomness
	* 🔐 Provably fair gambling mechanics

  

---

  

**Mokujin RNG** — *fair randomness, verified by math.*