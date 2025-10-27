class Rarity:
    def __init__(self, name: str, weight: int, items: List[str]):
        self.name = name
        self.weight = weight
        self.items = items

    def __repr__(self):
        return f"Rarity(name='{self.name}', weight={self.weight}, items={len(self.items)} items)"
