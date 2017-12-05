.. toctree::
   :maxdepth: 1

Inventory
=========

**Inherits:** object

**Module:** inventory

Brief Description
-----------------

Represents a basic inventory for item management

Instance Methods
----------------

+-----------------------------------+-----------------------------------------------------------------------------------------------+
| :ref:`Inventory <Inventory>`      | :ref:`Inventory <Inventory>` ( path, size=None )                                              |
+-----------------------------------+-----------------------------------------------------------------------------------------------+
| None                              | :ref:`add <Inventory.add>` ( item )                                                           |
+-----------------------------------+-----------------------------------------------------------------------------------------------+
| :ref:`Item <Item>`                | :ref:`get <Inventory.get>` ( slot )                                                           |
+-----------------------------------+-----------------------------------------------------------------------------------------------+
| :ref:`Item <Item>`                | :ref:`remove <Inventory.remove>` ( item )                                                     |
+-----------------------------------+-----------------------------------------------------------------------------------------------+
| :ref:`Item <Item>`                | :ref:`remove_from <Inventory.remove_from>` ( slot )                                           |
+-----------------------------------+-----------------------------------------------------------------------------------------------+
| :ref:`Item <Item>`                | :ref:`remove_first <Inventory.remove_first>` ( )                                              |
+-----------------------------------+-----------------------------------------------------------------------------------------------+
| List                              | :ref:`remove_all <Inventory.remove_all>` ( )                                                  |
+-----------------------------------+-----------------------------------------------------------------------------------------------+
| None                              | :ref:`shift_down <Inventory.shift_down>` ( )                                                  |
+-----------------------------------+-----------------------------------------------------------------------------------------------+
| None                              | :ref:`sort <Inventory.sort>` ( )                                                              |
+-----------------------------------+-----------------------------------------------------------------------------------------------+
| bool                              | :ref:`has_space <Inventory.has_space>` ( )                                                    |
+-----------------------------------+-----------------------------------------------------------------------------------------------+
| bool                              | :ref:`has_space <Inventory.has_space>` ( )                                                    |
+-----------------------------------+-----------------------------------------------------------------------------------------------+
| int                               | :ref:`find <Inventory.find>` ( :ref:`Item <Item>` item )                                      |
+-----------------------------------+-----------------------------------------------------------------------------------------------+
| int                               | :ref:`find_first_item <Inventory.find_first_item>` ( )                                        |
+-----------------------------------+-----------------------------------------------------------------------------------------------+
| int                               | :ref:`find_first_empty <Inventory.find_first_empty>` ( )                                      |
+-----------------------------------+-----------------------------------------------------------------------------------------------+
| int                               | :ref:`get_empty_count <Inventory.get_empty_count>` ( )                                        |
+-----------------------------------+-----------------------------------------------------------------------------------------------+
| :ref:`Item <Item>`                | :ref:`get_first_item <Inventory.get_first_item>` ( )                                          |
+-----------------------------------+-----------------------------------------------------------------------------------------------+
| List                              | :ref:`get_items <Inventory.get_items>` ( )                                                    |
+-----------------------------------+-----------------------------------------------------------------------------------------------+
| List                              | :ref:`get_items_with_kwargs <Inventory.get_items_with_kwargs>` ( str keyword, str args=None ) |
+-----------------------------------+-----------------------------------------------------------------------------------------------+

Instance Variables
------------------

- path - Filepath to a text file to save or load inventory data
- size - The amount of items the inventory can hold
- items_count - The amount of items in the inventory
- items_list - A list of references to item instances in the inventory, includes empty items

Instance Method Descriptions
----------------------------

.. _Inventory:

- Inventory Inventory ( str path, int size=None )

Construct a new inventory using the passed in filepath `path`. `size` must be passed in if the file does not
exist. If the file does exist and size is `None`. Then the size is set to the size of the inventory created from
the file.

.. _Inventory.add:

- None add ( :ref:`Item <Item>` item )

Add the passed in item instance to the inventory at the next empty slot.
If no slot is empty then it will raise an `InventoryFullError`. Use :ref:`has_space <Inventory.has_space>`
before adding an item without slot specified to ensure that no error is thrown.

.. _Inventory.set:

- None set ( int slot, :ref:`Item <Item>` item )

Add the `item` to the specific inventory slot, The new `item`
will replace the current `item` if one exists.

.. _Inventory.get:

- :ref:`Item <Item>` get ( int slot )

Return the item instance at the inventory `slot`.

.. _Inventory.remove:

- :ref:`Item <Item>` remove ( :ref:`Item <Item>` item )

Remove and return the first instance of the `item`. If the item is not found it will raise a `NoSuchItemError`.

.. _Inventory.remove_from:

- :ref:`Item <Item>` remove_from ( int slot )

Remove and return the `item` from the inventory slot. If the slot is empty it raises a `SlotEmptyError`.

.. _Inventory.remove_first:

- :ref:`Item <Item>` remove_first ( )

Remove and return the first `item` found. If the item is not found it will raise a `NoSuchItemError`.

.. _Inventory.remove_all:

- List remove_all ( )

Removes all items and returns them as a `List`.

.. _Inventory.shift_down:

- None shift_down ( )

Removes any empty slots at the start of the inventory shifting the items down.

.. _Inventory.sort:

- None sort ( str keyword )

Moves the items with the keyword to the start of the inventory sorting them by keyword in either alphabetical order,
numerical order (If only contains numbers).

.. _Inventory.has_space:

- bool has_space ( )

Returns `True` if the inventory has at least one slot empty. Else returns `False`.

.. _Inventory.is_empty:

- bool is_empty ( )

Returns true if the inventory does not contain any items.

.. _Inventory.find:

- int find ( str item )

Returns the first slot index of the item if it exists in the inventory. If no item is found returns `-1`.

.. _Inventory.find_first_item:

- int find_first_item ( )

Returns the slot index of the first item in the inventory if the inventory is not empty. If the inventory is empty
returns `-1`.

.. _Inventory.find_first_empty:

- int find_first_empty ( )

Returns the slot index of the first empty slot in the inventory. If the inventory is full returns `-1`.

.. _Inventory.get_empty_count:

- int get_empty_count ( )

Returns the number of empty slots in the inventory.

.. _Inventory.get_first_item:

- :ref:`Item <Item>` get_first_item ( )

Returns the first `item` in the inventory.

.. _Inventory.get_items:

- List get_items ( )

Returns a `List` of items in the inventory. Alternative to `Item().items_list` that will also return empty `items`.

.. _Inventory.get_items_with_kwargs:

- List get_items_with_kwargs ( str keyword, str arg=None )

Returns a list of inventory items with the specific `keyword` argument. If `arg` is not `None` then it will return only
the items that have the keyword argument and the arguments value is `args`

Instance Magic Methods
----------------------

.. _Inventory.iter:

- None __iter__ ( )

Iterates through the inventory items.

.. _Inventory.contains:

- bool __contains__ ( )

Returns true if the item is in the inventory.

.. _Inventory.getitem:

- Item __getitem__ ( )

Calls :ref:`get <Inventory.get>` on the item.

.. _Inventory.len:

- int __len__ ( )

Returns items_count

.. _Inventory._add:

- :ref:`Inventory <Inventory>` __add__()

Returns this inventory with the second inventory added to the end.

.. _Inventory.eq:

- bool __eq__ ( )

Returns true if this inventory has the same items and length as other inventory

.. _Inventory.lt:

- bool __lt__ ( )

Returns true if this inventory has less items than the other inventory

.. _Inventory.le:

- bool __le__ ( )

Returns true if this inventory has less or equal number of items than the other inventory

.. _Inventory.str:

- str __str__ ( )

Returns this inventory as a string


