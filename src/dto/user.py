from dataclasses import dataclass
from src.model.user import Gender


@dataclass
class UserRegistrationDTO:
    first_name: str
    last_name: str
    gender: Gender
    login: str
    password: str
