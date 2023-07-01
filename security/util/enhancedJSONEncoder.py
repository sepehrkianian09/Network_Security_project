import json

from pydantic import BaseModel
from base64 import b64encode


def convert_bytes_to_str(message: dict):
    for key, val in message.items():
        if isinstance(val, bytes):
            message[key] = b64encode(val).decode('utf-8')
        if isinstance(val, dict):
            message[key] = convert_bytes_to_str(val)
        if isinstance(val, list):
            decoded = []
            for i in val:
                if isinstance(i, bytes):
                    decoded.append(b64encode(i).decode('utf-8'))
                if isinstance(i, dict):
                    decoded.append(convert_bytes_to_str(i))
                else:
                    decoded.append(i)
            message[key] = decoded
    return message


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, BaseModel):
            x = convert_bytes_to_str(o.dict())
            return x
        return super(EnhancedJSONEncoder, self).default(o)
