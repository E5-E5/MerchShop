from dataclasses import dataclass
from enum import Enum


class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"


@dataclass
class User:
    user_id: int
    first_name: str
    last_name: str
    gender: Gender
    login: str
    password: str
    coin: int = 0


