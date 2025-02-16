from dataclasses import dataclass
from datetime import datetime


@dataclass
class Exchange:
    sender_id: int
    recipient_id: int
    coin: int
    date: datetime
