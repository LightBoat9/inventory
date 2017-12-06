.. toctree::
   :maxdepth: 1

.. _Item:

Item
====

**Inherits:** object

**Module:** :ref:`inventory <Module_Inventory>`

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

.. _Item.init:

- **Item Item (** dict kwargs **)**

Construct a new inventory item with as many keyword arguments describing the item as needed.

.. _Item.set:

- **None set (** str keyword, str arg **)**

Set the value for the keyword argument in :ref:`kwargs <Item.kwargs>`.

.. _Item.get:

- **str get (** str keyword **)**

Return the argument for the dictionary key ``keyword`` in ``kwargs``. Returns ``None`` if the keyword is not in
kwargs

Supported Magic Methods
-----------------------

.. _Item.str:

- **str __str__ ( )**

Returns :ref:`kwargs <Item.kwargs>` as a string.

