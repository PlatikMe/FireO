from fireo.fields import Field, errors
from google.cloud.firestore_v1.vector import Vector


class VectorField(Field):
    """Vector field for Models.

    Allowed attributes: ['max_length']

    Examples
    -------
    .. code-block:: python
        class Item(Model):
            embedding = Vector()

        i = Item()
        i.embedding = Vector([0.1, 0.2, 0.3, 0.4])
    """

    allowed_attributes = ['max_length']

    def attr_max_length(self, attr_val, field_val):
        """Method for attribute max_length."""
        if len(field_val.values) > attr_val:  # Use .values for Vector
            raise errors.VectorLengthError(f"Vector length cannot exceed {attr_val} elements.")
        return field_val

    def db_value(self, val):
        """Convert the vector value to a format suitable for Firestore storage."""
        if isinstance(val, Vector) or val is None:
            return val
        elif isinstance(val, list):
            try:
                return Vector(val)
            except ValueError as e:
                # Wrap the ValueError to provide more context.
                raise errors.InvalidFieldType(
                    f"Invalid data provided for Vector field '{self.name}': {e}"
                ) from e

        raise errors.InvalidFieldType(
            f"Invalid field type. Field '{self.name}' expected a Vector or a list of numbers, got {type(val)}."
        )
