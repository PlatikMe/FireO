import unittest

from fireo.fields import ByteField, TextField
from fireo.models import Model
from fireo.models.errors import ModelSerializingWrappedError


class MyByteModel(Model):
    name = TextField()
    byte_data = ByteField()


class ByteFieldTest(unittest.TestCase):
    def test_byte_operations(self):

        item1 = MyByteModel()
        item1.name = "Test Bytes"
        byte_value = b'\x00\x01\x02\x03\x04'
        item1.byte_data = byte_value
        item1.save()

        retrieved_item = MyByteModel.collection.get(item1.key)
        self.assertEqual(retrieved_item.name, "Test Bytes")
        self.assertEqual(retrieved_item.byte_data, byte_value)

        # Example of Updating bytes
        new_byte_value = b'\x05\x06\x07\x08\x09'
        retrieved_item.byte_data = new_byte_value
        retrieved_item.update()

        retrieved_item2 = MyByteModel.collection.get(item1.key)
        self.assertEqual(retrieved_item2.byte_data, new_byte_value)

        MyByteModel.collection.delete(item1.key)


    def test_string_conversion(self):
        """Tests automatic string to bytes conversion."""
        item = MyByteModel()
        item.name = "String Test"
        item.byte_data = "hello" # Store as string
        item.save()

        retrieved_item = MyByteModel.collection.get(item.key)
        self.assertEqual(retrieved_item.byte_data, b"hello")  # Retrieved as bytes

        MyByteModel.collection.delete(item.key) # Cleanup

    def test_invalid_type(self):
        item = MyByteModel()
        item.name = "Invalid Type"
        with self.assertRaises(ModelSerializingWrappedError):
            item.byte_data = 123  # Try to set an invalid type
            item.save()

        # Cleanup in case it somehow saved.
        try:
            MyByteModel.collection.delete(item.key)
        except Exception: # We expect it to not exist, so ignore error.
            pass
