from typing import Union

from pydantic import BaseModel


class WhisperMessage(BaseModel):
    ratchet_key: Union[bytes, None] = None
    counter: Union[int, None] = None
    previous_counter: Union[int, None] = None
    ciphertext: Union[bytes, None] = None

    def __init__(self, *args, **kwargs):
        from base64 import b64decode
        for key, val in kwargs.items():
            if key in ['ratchet_key', 'ciphertext'] and val:
                kwargs[key] = b64decode(val)
        super().__init__(*args, **kwargs)


class PreKeyWhisperMessage(BaseModel):
    registration_id: Union[int, None] = None
    pre_key_id: Union[int, None] = None
    signed_pre_key_id: Union[int, None] = None
    base_key: Union[bytes, None] = None
    identity_key: Union[bytes, None] = None
    message: Union[bytes, None] = None

    def __init__(self, *args, **kwargs):
        from base64 import b64decode
        for key, val in kwargs.items():
            if key in ['base_key', 'identity_key', 'message'] and val:
                kwargs[key] = b64decode(val)
        super().__init__(*args, **kwargs)


class KeyExchangeMessage(BaseModel):
    id: Union[int, None] = None
    base_key: Union[bytes, None] = None
    ratchet_key: Union[bytes, None] = None
    identity_key: Union[bytes, None] = None
    base_key_signature: Union[bytes, None] = None

    def __init__(self, *args, **kwargs):
        from base64 import b64decode
        for key, val in kwargs.items():
            if key in ['base_key', 'ratchet_key', 'identity_key', 'base_key_signature'] and val:
                kwargs[key] = b64decode(val)
        super().__init__(*args, **kwargs)


class SenderKeyMessage(BaseModel):
    id: Union[int, None] = None
    iteration: Union[int, None] = None
    ciphertext: Union[bytes, None] = None

    def __init__(self, *args, **kwargs):
        from base64 import b64decode
        for key, val in kwargs.items():
            if key in ['ciphertext'] and val:
                kwargs[key] = b64decode(val)
        super().__init__(*args, **kwargs)


class SenderKeyDistributionMessage(BaseModel):
    id: Union[int, None] = None
    iteration: Union[int, None] = None
    chain_key: Union[bytes, None] = None
    signing_key: Union[bytes, None] = None

    def __init__(self, *args, **kwargs):
        from base64 import b64decode
        for key, val in kwargs.items():
            if key in ['chain_key', 'signing_key'] and val:
                kwargs[key] = b64decode(val)
        super().__init__(*args, **kwargs)
