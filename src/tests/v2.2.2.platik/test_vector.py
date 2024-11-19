from google.cloud.firestore_v1.vector import Vector

from fireo.fields import TextField, VectorField
from fireo.models import Model


class MyVectorModel(Model):
    name = TextField()
    embedding = VectorField()


def test_vector_operations():
    # Example 1: Creating and saving a vector
    item1 = MyVectorModel()
    item1.name = "Product A"
    values = (0.1, 0.2, 0.3, 0.4)
    item1.embedding = Vector(values)
    item1.save()

    # Example 2: Retrieving and using a vector
    retrieved_item = MyVectorModel.collection.get(item1.key)
    assert retrieved_item.name == "Product A"
    assert retrieved_item.embedding.count(0.2) == 1
    assert retrieved_item.embedding.to_map_value()['value'] == values

    # Example 3: Updating a vector (replace entirely)
    new_values = (0.5, 0.6, 0.7, 0.8)
    retrieved_item.embedding = Vector(new_values)  # Create a new vector.
    retrieved_item.update()
    retrieved_item.refresh()
    assert retrieved_item.embedding.to_map_value()['value'] == new_values

    MyVectorModel.collection.delete(item1.key)


def test_vector_operations_with_lists():
    # Example 5: Setting a vector from a list
    item2 = MyVectorModel()
    item2.name = "Product B"
    values = (1.1, 1.2, 1.3, 1.4)
    item2.embedding = list(values)  # Directly use a list - it will be converted.
    item2.save()

    retrieved_item = MyVectorModel.collection.get(item2.key)
    assert retrieved_item.embedding.to_map_value()['value'] == values

    MyVectorModel.collection.delete(item2.key)
