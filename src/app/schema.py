from marshmallow import Schema, fields, validates, ValidationError
from marshmallow import Schema, fields, pre_load


class ReadingsSchema(Schema):
    class Meta:
        unknown = 'include'

    city = fields.Str(required=True)
    temperature = fields.Float(required=True)
    humidity = fields.Float(required=True)
    wind_speed = fields.Float(required=True)


    @validates('temperature')
    def validate_temperature(self, value):
        if not (40 <= value <= 90):
            raise ValidationError(
                'Temperature must be between 40 and 90 degrees.')

    @validates('humidity')
    def validate_humidity(self, value):
        if not (0 <= value <= 100):
            raise ValidationError(
                'Humidity must be between 0.0 and 100.0%.')
