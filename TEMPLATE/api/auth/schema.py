from marshmallow import fields as f, Schema


class UserSchema(Schema):
    extid = f.Str(dump_only=True)
    name = f.Str()
