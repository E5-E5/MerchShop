from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class InventoryItem:
    type: str
    quantity: int


@dataclass
class ReceivedCoinTransaction:
    fromUser: str
    amount: int


@dataclass
class SentCoinTransaction:
    toUser: str
    amount: int


# @dataclass
# class CoinHistory:
#     received: list[ReceivedCoinTransaction]
#     sent: list[SentCoinTransaction]
class CoinHistory(BaseModel):
    received: list[dict]
    sent: list[dict]

@dataclass
class InfoResponse:
    coins: int
    inventory: list[InventoryItem]
    coinHistory: CoinHistory


@dataclass
class ErrorResponse:
    errors: str


@dataclass
class AuthRequest:
    username: str
    password: str


@dataclass
class AuthResponse:
    token: str


@dataclass
class SendCoinRequest:
    toUser: str
    amount: int
