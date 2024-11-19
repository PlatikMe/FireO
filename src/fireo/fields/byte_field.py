from fireo.fields import Field, errors
from fireo.utils.types import LoadOptions


class ByteField(Field):
    """Byte field for Models.  Stores bytes data.

    Allowed attributes: ['max_length']
    """

    allowed_attributes = ['max_length']

    def attr_max_length(self, attr_val, field_val):
        """Method for attribute max_length."""
        if len(field_val) > attr_val:
            raise errors.ByteLengthError(f"Byte data length cannot exceed {attr_val} bytes.")
        return field_val

    def db_value(self, val):
        """Convert to bytes for storage."""
        if isinstance(val, bytes) or val is None:
            return val
        elif isinstance(val, str):  # Added for convenience
            return val.encode('utf-8')  # Encode strings to bytes using UTF-8
        raise errors.InvalidFieldType(
            f"Invalid field type. Field '{self.name}' expected bytes or string, got {type(val)}."
        )

    def field_value(self, val, load_options=LoadOptions()):
        """Return bytes from Firestore."""
        if isinstance(val, bytes) or val is None:
            return val
        elif isinstance(val, str): # For backwards compatibility
            return val.encode('utf-8')
        raise errors.InvalidFieldType(
            f"Invalid field type received from Firestore for field '{self.name}'. Expected bytes, got {type(val)}."
        )
