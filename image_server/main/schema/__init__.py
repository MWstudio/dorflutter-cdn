from marshmallow import fields, Schema


# Requests
class RequestFileSchema(Schema):
  file = fields.Raw(required=True, type="file")