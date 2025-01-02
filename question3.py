import json
from decimal import Decimal

class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse_float(self, value):
        try:
            return Decimal(value)
        except Exception:
            return super().parse_float(value)

    def parse_int(self, value):
        return int(value)

def parse_json(json_string):
    return json.loads(json_string, cls=CustomJSONDecoder)


json_string = '{"integer": 1234567890123456789012345678901234567890, "float": 1234567890.123456789123456789, "list": [1, 2, 3], "nested_map": {"key": "value"}}'
parsed_object = parse_json(json_string)
print(parsed_object)