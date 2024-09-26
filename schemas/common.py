from ninja import Schema


class Message(Schema):
    details: str


class Token(Schema):
    token: str
