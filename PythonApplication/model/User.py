from dataclasses import dataclass
import flask_login

@dataclass
class User(flask_login.UserMixin):
    id: str
    password: str