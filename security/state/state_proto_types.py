from pydantic import BaseModel, Field
from typing import List, Union


class SessionStructureChainChainKey(BaseModel):
    index: Union[int, None] = None
    key: Union[bytes, None] = None

    def __init__(self, *args, **kwargs):
        from base64 import b64decode
        for key, val in kwargs.items():
            if key in ['key'] and val:
                kwargs[key] = b64decode(val)
        super().__init__(*args, **kwargs)


class SessionStructureChainMessageKey(BaseModel):
    index: Union[int, None] = None
    cipher_key: Union[bytes, None] = None
    mac_key: Union[bytes, None] = None
    iv: Union[bytes, None] = None

    def __init__(self, *args, **kwargs):
        from base64 import b64decode
        for key, val in kwargs.items():
            if key in ['cipher_key', 'mac_key', 'iv'] and val:
                kwargs[key] = b64decode(val)
        super().__init__(*args, **kwargs)


class SessionStructureChain(BaseModel):
    sender_ratchet_key: Union[bytes, None] = None
    sender_ratchet_key_private: Union[bytes, None] = None
    chain_key: Union["SessionStructureChainChainKey", None] = None
    message_keys: List["SessionStructureChainMessageKey"] = Field(default_factory=list)

    def __init__(self, *args, **kwargs):
        from base64 import b64decode
        for key, val in kwargs.items():
            if key in ['sender_ratchet_key', 'sender_ratchet_key_private'] and val:
                kwargs[key] = b64decode(val)
        super().__init__(*args, **kwargs)


class SessionStructurePendingKeyExchange(BaseModel):
    sequence: Union[int, None] = None
    local_base_key: Union[bytes, None] = None
    local_base_key_private: Union[bytes, None] = None
    local_ratchet_key: Union[bytes, None] = None
    local_ratchet_key_private: Union[bytes, None] = None
    local_identity_key: Union[bytes, None] = None
    local_identity_key_private: Union[bytes, None] = None

    def __init__(self, *args, **kwargs):
        from base64 import b64decode
        for key, val in kwargs.items():
            if key in ['local_base_key', 'local_base_key_private', 'local_ratchet_key', 'local_ratchet_key_private', 'local_identity_key', 'local_identity_key_private'] and val:
                kwargs[key] = b64decode(val)
        super().__init__(*args, **kwargs)


class SessionStructurePendingPreKey(BaseModel):
    pre_key_id: Union[int, None] = None
    signed_pre_key_id: Union[int, None] = None
    base_key: Union[bytes, None] = None

    def __init__(self, *args, **kwargs):
        from base64 import b64decode
        for key, val in kwargs.items():
            if key in ['base_key'] and val:
                kwargs[key] = b64decode(val)
        super().__init__(*args, **kwargs)


class SessionStructure(BaseModel):
    session_version: Union[int, None] = None
    local_identity_public: Union[bytes, None] = None
    remote_identity_public: Union[bytes, None] = None
    root_key: Union[bytes, None] = None
    previous_counter: Union[int, None] = None
    sender_chain: Union["SessionStructureChain", None] = None
    receiver_chains: List["SessionStructureChain"] = Field(default_factory=list)
    pending_key_exchange: Union["SessionStructurePendingKeyExchange", None] = None
    pending_pre_key: Union["SessionStructurePendingPreKey", None] = None
    remote_registration_id: Union[int, None] = None
    local_registration_id: Union[int, None] = None
    needs_refresh: Union[bool, None] = None
    alice_base_key: Union[bytes, None] = None

    def __init__(self, *args, **kwargs):
        from base64 import b64decode
        for key, val in kwargs.items():
            if key in ['local_identity_public', 'remote_identity_public', 'root_key', 'alice_base_key'] and val:
                kwargs[key] = b64decode(val)
        super().__init__(*args, **kwargs)


class RecordStructure(BaseModel):
    current_session: Union["SessionStructure", None] = None
    previous_sessions: List["SessionStructure"] = Field(default_factory=list)


class PreKeyRecordStructure(BaseModel):
    id: Union[int, None] = None
    public_key: Union[bytes, None] = None
    private_key: Union[bytes, None] = None

    def __init__(self, *args, **kwargs):
        from base64 import b64decode
        for key, val in kwargs.items():
            if key in ['public_key', 'private_key'] and val:
                kwargs[key] = b64decode(val)
        super().__init__(*args, **kwargs)


class SignedPreKeyRecordStructure(BaseModel):
    id: Union[int, None] = None
    public_key: Union[bytes, None] = None
    private_key: Union[bytes, None] = None
    signature: Union[bytes, None] = None
    timestamp: Union[float] = None

    def __init__(self, *args, **kwargs):
        from base64 import b64decode
        for key, val in kwargs.items():
            if key in ['public_key', 'private_key', 'signature'] and val:
                kwargs[key] = b64decode(val)
        super().__init__(*args, **kwargs)


class IdentityKeyPairStructure(BaseModel):
    public_key: Union[bytes, None] = None
    private_key: Union[bytes, None] = None

    def __init__(self, *args, **kwargs):
        from base64 import b64decode
        for key, val in kwargs.items():
            if key in ['public_key', 'private_key'] and val:
                kwargs[key] = b64decode(val)
        super().__init__(*args, **kwargs)


class SenderKeyStateStructureSenderChainKey(BaseModel):
    iteration: Union[int, None] = None
    seed: Union[bytes, None] = None

    def __init__(self, *args, **kwargs):
        from base64 import b64decode
        for key, val in kwargs.items():
            if key in ['seed'] and val:
                kwargs[key] = b64decode(val)
        super().__init__(*args, **kwargs)


class SenderKeyStateStructureSenderMessageKey(BaseModel):
    iteration: Union[int, None] = None
    seed: Union[bytes, None] = None

    def __init__(self, *args, **kwargs):
        from base64 import b64decode
        for key, val in kwargs.items():
            if key in ['seed'] and val:
                kwargs[key] = b64decode(val)
        super().__init__(*args, **kwargs)


class SenderKeyStateStructureSenderSigningKey(BaseModel):
    public: Union[bytes, None] = None
    private: Union[bytes, None] = None

    def __init__(self, *args, **kwargs):
        from base64 import b64decode
        for key, val in kwargs.items():
            if key in ['public', 'private'] and val:
                kwargs[key] = b64decode(val)
        super().__init__(*args, **kwargs)


class SenderKeyStateStructure(BaseModel):
    sender_key_id: Union[int, None] = None
    sender_chain_key: Union["SenderKeyStateStructureSenderChainKey", None] = None
    sender_signing_key: Union["SenderKeyStateStructureSenderSigningKey", None] = None
    sender_message_keys: List["SenderKeyStateStructureSenderMessageKey"] = Field(default_factory=list)


class SenderKeyRecordStructure(BaseModel):
    sender_key_states: List["SenderKeyStateStructure"] = Field(default_factory=list)
