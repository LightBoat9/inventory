.. Item Class.

.. toctree::
   :maxdepth: 2
   :caption: Item:

Item Class
===========

Represents an inventory item instance for storing and retrieving item properties.

Class Methods
--------------

+------------+------------------------+
|`Item`_ |Item(self, **kwargs)        |
+------------+------------------------+

.. _Item: #item-item-str-kwargs

Item ``**Item(str, **kwargs)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Constructs a new inventory item with as many keyword arguments describing the item as needed

str get(self, keyword)
^^^^^^^^^^^^^^^^^^^^^^^^

Return the argument for the dictionary key ``keyword`` in ``kwargs``

Equivalent to ``Item().kwargs[keyword]`` however, it does not throw a ``KeyError`` if the key is missing.
Instead, it returns ``None``
