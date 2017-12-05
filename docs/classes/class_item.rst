.. toctree::
   :maxdepth: 1

Item
====

**Inherits:** object

**Module:** inventory

Brief Description
-----------------

Represents an inventory item instance for storing and retrieving item properties.

Instance Methods
----------------

+------------------------+-------------------------------------------------------------------+
|:ref:`Item <Item>`      | :ref:`Item <Item>` ( dict kwargs )                                |
+------------------------+-------------------------------------------------------------------+
| None                   | :ref:`set <Item.set>` ( str keyword, str arg )                    |
+------------------------+-------------------------------------------------------------------+
| str                    | :ref:`get <Item.get>` ( str keyword )                             |
+------------------------+-------------------------------------------------------------------+
| bool                   | :ref:`has_keyword <Item.has_keyword>` ( str keyword )             |
+------------------------+-------------------------------------------------------------------+
| bool                   | :ref:`is_empty <Item.is_empty>` ( )                               |
+------------------------+-------------------------------------------------------------------+

Description
-----------

Represents an item that can be stored in an inventory. The item takes in as many named arguments
as necessary that describe it.

Instance Variables
------------------

.. _Item.kwargs:

- **dict kwargs** - A list of keywords describing the item

Instance Method Descriptions
----------------------------

.. _Item:

- **Item Item (** dict kwargs **)**

Construct a new inventory item with as many keyword arguments describing the item as needed.

.. _Item.set:

- **None set (** str keyword, str arg **)**

Set the value for the keyword argument in `self.kwargs`.

.. _Item.get:

- **str get (** str keyword **)**

Return the argument for the dictionary key ``keyword`` in ``kwargs``.

Equivalent to ``Item().kwargs[keyword]`` however, it does not throw a ``KeyError`` if the key is missing.
Instead, it returns ``None``.

.. _Item.has_keyword:

- **bool has_keyword (** str keyword **)**

Return `True` if the `keyword` exists in :ref:`kwargs <Item.kwargs>`, Else return `False`.

.. _Item.is_empty:

- **bool is_empty ( )**

Returns `True` if no :ref:`kwargs <Item.kwargs>` were passed in, otherwise returns `False`.

Supported Magic Methods
-----------------------

.. _Item.str:

- **str __str__ ( )**

Returns :ref:`kwargs <Item.kwargs>` as a string.

