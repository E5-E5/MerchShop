from dataclasses import dataclass


@dataclass
class Merch:
    merch_id: int
    name: str
    coin: int
    count: int