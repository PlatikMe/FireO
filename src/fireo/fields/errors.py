"""Field related errors"""


class NumberRangeError(Exception):
    pass


class UnSupportedAttribute(Exception):
    pass


class InvalidFieldType(Exception):
    pass


class AttributeTypeError(Exception):
    pass


class NestedModelTypeError(Exception):
    pass


class ReferenceTypeError(Exception):
    pass


class MissingFieldOptionError(Exception):
    pass


class FieldNotFound(Exception):
    pass


class RequiredField(Exception):
    pass


class FieldValidationFailed(Exception):
    pass


class ValidatorNotCallable(Exception):
    pass


class AttributeMethodNotDefined(Exception):
    pass

class VectorLengthError(Exception):
    pass

class InvalidUpdateModifierError(Exception):
    pass

class ByteLengthError(Exception):
    pass
