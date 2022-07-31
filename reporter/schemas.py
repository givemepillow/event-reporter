from marshmallow import Schema, fields, validate


class EventSchema(Schema):
    token = fields.UUID(required=True)
    type = fields.Str(validate=validate.OneOf(["INFO", "WARNING", "ERROR"]), required=True)
    title = fields.Str(required=True)
    text = fields.Str(required=True)
    datetime = fields.DateTime(required=True)
