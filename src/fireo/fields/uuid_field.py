import uuid
from fireo.fields import Field, errors
from fireo.utils.types import LoadOptions


class UuidField(Field):
    """UUID field for Models. Stores UUIDs as bytes.

    This field stores UUID values as bytes (16 bytes) in Firestore
    for efficiency, but interacts with the application using Python's
    `uuid.UUID` type.
    """

    def db_value(self, val):
        if isinstance(val, uuid.UUID) or val is None:
            return val.bytes if val else None  # Store as bytes
        elif isinstance(val, str):
            try:
                return uuid.UUID(val).bytes
            except ValueError as e:
                raise errors.InvalidUuidFormat(f"Invalid UUID string format for field '{self.name}': {e}")
        elif isinstance(val, bytes) and len(val) == 16:
            # Accept raw bytes if length 16
            return val
        raise errors.InvalidFieldType(
            f"Invalid field type. Field '{self.name}' expected uuid.UUID, string, or bytes[16], got {type(val)}."
        )

    def field_value(self, val, load_options=LoadOptions()):
        if val is None:
            return None
        elif isinstance(val, bytes) and len(val) == 16:
            return uuid.UUID(bytes=val)  # Convert from bytes to UUID
        elif isinstance(val, str):
            try:
                return uuid.UUID(val)  # If it's a valid UUID string, attempt conversion
            except ValueError as e:
                raise errors.InvalidUuidFormat(f"Invalid UUID string retrieved from Firestore for '{self.name}': {e}")
        raise errors.InvalidFieldType(
            f"Invalid field type received from Firestore for field '{self.name}'. Expected bytes[16], got {type(val)}."
        )
