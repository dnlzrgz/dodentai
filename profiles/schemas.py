from ninja import Schema


class ProfileIn(Schema):
    biography: str


class ProfileOut(Schema):
    biography: str
