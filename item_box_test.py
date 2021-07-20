import pytest
import sys
from item_box import ItemBox

def test_create_item_box():
    item_1 = ItemBox(name="Sauce Labs Bolt T-Shirt");

    print(item_1.name)
    assert(item_1.name == "Sauce Labs Bolt T-Shirt")
    print(item_1.price)
    assert(item_1.price == 15.99)
    print(item_1.description)
    assert(item_1.description == "Get your testing superhero on with the Sauce Labs bolt T-shirt. From American Apparel, 100% ringspun combed cotton, heather gray with red bolt.")

def test_create_item_box_negative():
    item_2 = ItemBox(name="Sauce Labs Bolt T-Shirt");

    print(item_2.name)
    assert(item_2.name == "Sauce Labs Bolt T-Shirt")
    print(item_2.price)
    assert(item_2.price == 15)
    print(item_2.description)
    assert(item_2.description == "Get your testing superhero on with the Sauce Labs bolt T-shirt. From American Apparel, 100% ringspun combed cotton, heather gray with red bolt.")
