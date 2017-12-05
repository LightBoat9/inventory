.. Item Class.

Item Class
===========

Represents an inventory item instance for storing and retrieving item properties.

Class Methods
--------------

+------------------------+-------------------------------------------------------------------+
|:ref:`Item <Item>`      | :ref:`Item <Item>`:literal:`(self, **kwargs)`                     |
+------------------------+-------------------------------------------------------------------+
| None                   | :ref:`set <Item.set>`:literal:`(self, keyword, arg)`              |
+------------------------+-------------------------------------------------------------------+
| str                    | :ref:`get <Item.get>`:literal:`(self, keyword)`                   |
+------------------------+-------------------------------------------------------------------+
| bool                   | :ref:`has_keyword <Item.has_keyword>`:literal:`(self, keyword)`   |
+------------------------+-------------------------------------------------------------------+
| bool                   | :ref:`is_empty <Item.is_empty>`:literal:`(self)`                  |
+------------------------+-------------------------------------------------------------------+
| str                    | :ref:`__str__ <Item.str>`:literal:`(self)`                        |
+------------------------+-------------------------------------------------------------------+

.. _Item:

Item ``**Item(str, **kwargs)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Constructs a new inventory item with as many keyword arguments describing the item as needed

.. _Item.set:

None set(self, keyword, arg)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set the value for the keyword argument in `self.kwargs`

.. _Item.get:

str get(self, keyword)
^^^^^^^^^^^^^^^^^^^^^^^

Return the argument for the dictionary key ``keyword`` in ``kwargs``

Equivalent to ``Item().kwargs[keyword]`` however, it does not throw a ``KeyError`` if the key is missing.
Instead, it returns ``None``

.. _Item.has_keyword:

bool has_keyword(self, keyword)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Return True if the keyword exists in `kwargs`, Else return False

.. _Item.is_empty:

bool is_empty(self)
^^^^^^^^^^^^^^^^^^^

Return True if the item has no keyword arguments, Else return False

.. _Item.str:

str __str__(self)
^^^^^^^^^^^^^^^^^

Return `kwargs` as a string