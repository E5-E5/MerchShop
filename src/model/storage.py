from dataclasses import dataclass


@dataclass
class Storage:
    user_id: int
    merch_id: int
    count: int
