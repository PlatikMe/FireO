import unittest
import uuid

from fireo.fields import UuidField, TextField
from fireo.models import Model
from fireo.models.errors import ModelSerializingWrappedError


class UuidModel(Model):
    name = TextField()
    uuid_field = UuidField()


class UuidFieldTest(unittest.TestCase):
    def test_uuid_operations(self):
        u = uuid.uuid4()

        # Test with UUID object
        item1 = UuidModel()
        item1.name = "UUID Test"
        item1.uuid_field = u
        item1.save()

        retrieved_item = UuidModel.collection.get(item1.key)
        self.assertEqual(retrieved_item.uuid_field, u)

        # Test updating with a new UUID
        u2 = uuid.uuid4()
        retrieved_item.uuid_field = u2
        retrieved_item.update()

        retrieved_item2 = UuidModel.collection.get(item1.key)
        self.assertEqual(retrieved_item2.uuid_field, u2)

        UuidModel.collection.delete(item1.key)

    def test_uuid_string_storage(self):
        uuid_str = str(uuid.uuid4())
        item = UuidModel.collection.create(name="UUID String Test", uuid_field=uuid_str)

        retrieved_item = UuidModel.collection.get(item.key)
        self.assertEqual(retrieved_item.uuid_field, uuid.UUID(uuid_str))

        UuidModel.collection.delete(item.key)

    def test_invalid_uuid_string(self):
        item = UuidModel()
        item.name = "Invalid UUID"
        with self.assertRaises(ModelSerializingWrappedError):
            item.uuid_field = "not-a-valid-uuid"
            item.save()
        # Cleanup in case the invalid model was saved.
        if hasattr(item, 'key'):
             UuidModel.collection.delete(item.key)

    def test_invalid_type(self):
        item = UuidModel()
        item.name = "Invalid Type"
        with self.assertRaises(ModelSerializingWrappedError):
            item.uuid_field = 123
            item.save()
        # Cleanup in case the invalid model was saved.
        if hasattr(item, 'key'):
             UuidModel.collection.delete(item.key)

    def test_bytes_input(self):
        """Test setting the field with bytes."""
        u = uuid.uuid4()
        item = UuidModel()
        item.name = "Bytes Input Test"
        item.uuid_field = u.bytes # Provide bytes directly.
        item.save()
        retrieved_item = UuidModel.collection.get(item.key)
        self.assertEqual(retrieved_item.uuid_field, u)

        UuidModel.collection.delete(item.key)
