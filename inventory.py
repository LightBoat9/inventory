import ast


class Item(object):
    """Represents an item that can be stored in the inventory.

    The item takes in as many named arguments
    as necessary that describe the item.

    Example:
        Item(name="health pot", category="pots")
    """
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def get(self, keyword):
        """Returns the argument for the items keyword attribute.

        This can also be accessed by directly accessing the items
        kwargs dictionary. However this function will return
        None if the keyword does not exist.

        Example:
            item = Item(name="potion")
            item.kwargs["name"]  # returns "potion"
            item.kwargs["type"]  # raises KeyError
            item.get("name")  # returns "potion"
            item.get("type")  # returns None

        Args:
            keyword (str): The string keyword name.

        Returns:
            The argument for the keyword or None if
            the keyword does not exist.
        """
        try:
            return self.kwargs[keyword]
        except KeyError:
            return None

    def set(self, keyword, arg):
        """Sets the value for the keyword in kwargs.

        Args:
            keyword (str): The string keyword name
            arg: The value to set the keyword to, will be stored as a string
        """
        self.kwargs[keyword] = arg

    def has_keyword(self, keyword):
        """Returns true if the string keyword is
        in the keyword arguments dictionary."""
        return keyword in self.kwargs

    def is_empty(self):
        """Returns true if the item was created with no keyword arguments"""
        return len(self.kwargs) == 0

    def __str__(self):
        return str(self.kwargs) + "\n"


class Inventory(object):
    """Represents a basic inventory for item management

    The inventory will take in a filepath to the inventory text file
    and a size. The filepath should point to either an empty text file
    or a previously created inventory file. If the file exists and holds
    item data, then the item data is used to create the inventory.
    If the new inventory size differs from the file then the new inventory
    will be cut or extended. Otherwise a blank inventory will be instanced
    with the number of slots added. If the file inventory size is unknown
    size can be omitted and the size of the inventory file will be used
    """
    def __init__(self, path, size=None):
        open(path, "a").close()  # Create a blank file if it does not exist
        self.path = path
        self.size = size
        if size is None: self.size = self._inv_file_length()
        self.items_count = 0
        self.items_list = []
        self._update()

    def _update(self):
        """Reads the inventory file and cuts or
        extends it to fit the passed in size

        Iterates through the inventory file lines and parses the
        information into Item instances. This can cut and extend
        the current file if the size differs from the original
        inventory size, otherwise it loads the information into
        the new inventory instance.
        """
        _slot_count = 0
        self.items_count = 0

        with open(self.path, "r") as file:
            data = file.readlines()

        for i in range(min(len(data), self.size)):
            keys = data[i].rstrip()
            if keys:  # Ignores empty lines
                if i >= len(self.items_list):
                    self.items_list.append(Item(**ast.literal_eval(keys)))
                if not self.items_list[i].is_empty(): self.items_count += 1
                _slot_count += 1

        with open(self.path, "w") as file:
            for i in range(self.size):
                if i >= _slot_count: self.items_list.append(Item())
                file.write(str(self.items_list[i]))

    def _inv_file_length(self):
        with open(self.path, "r") as file: data = file.readlines()
        return len(data)

    def add(self, item, slot=None):
        """Adds an item to the inventory.

        Adds the passed in Item instance to the inventory at the optional
        passed in slot number. If not slot number is passed in the next
        free empty slot is used. If no slot is specified and there is no
        empty slot available then it will throw a IndexError. Use has_space
        before adding an item without slot specified to ensure that no
        error is thrown.

        Args:
            item (Item): instance of the item to add.
            slot (int): optional integer inventory slot.

        Raises:
            IndexError: if slot is negative or greater than or equal to
                        the inventory size.
        """
        if slot is None: slot = self.get_first_empty()
        if slot < 0: raise IndexError("slot can not be negative")
        if slot >= self.size:
            raise IndexError("slot can not be larger than inventory size")

        # _update not used because only one line needs to be changed
        with open(self.path, "r") as file:
            data = file.readlines()

        data[slot] = str(item)

        with open(self.path, "w") as file:
            file.writelines(data)

        self.items_list[slot] = item
        self.items_count += 1

    def remove(self, slot):
        """Removes an item from the inventory.

        Removes the item from the passed in inventory slot number.

        Args:
            slot (int): integer inventory slot to remove an item from.

        Raises:
            ValueError: if slot is negative or greater than
                        or equal to the inventory size.
        """
        if slot < 0: raise ValueError("slot can not be negative")
        if slot >= self.size:
            raise ValueError("slot can not be larger than inventory size")

        item = self.items_list[slot]

        # _update not used because only one line needs to be changed.
        with open(self.path, "r") as file:
            data = file.readlines()

        self.items_list[slot] = Item()
        data[slot] = str(self.items_list[slot])

        with open(self.path, "w") as file:
            file.writelines(data)

        self.items_count -= 1

        return item

    def remove_all(self):
        """Removes and returns all of the inventory items.

        Sets all of the inventory slots to empty items and returns
        a list of items removed. The list will not contain existing
        inventory slots.

        Returns:
            A list of the inventory items that were removed.
        """
        items = []
        for i, item in enumerate(self.items_list):
            if not item.is_empty():
                items.append(self.items_list[i])
                self.items_list[i] = Item()

        self._update()

        return items

    def sort(self):
        """Sorts the inventory so that non-empty
           items come before empty items.

        Sorts the inventory using Insertion sort, pushing all existing items
        to the front of the inventory.

        Example:
            {}
            {'name': 'health potion'}

            After sort() becomes...

            {'name': 'health potion'}
            {}
        """
        for a in range(1, len(self.items_list)):
            b = 0
            while (not self.items_list[a - b].is_empty()
                   and self.items_list[a - b - 1].is_empty()):
                self._sort_swap(a - b)
                if a - b - 1 == 0: break
                b += 1
        self._update()

    def sort_by_keyword(self, keyword):
        """Sorts the inventory by keyword.

        Sorts the inventory using insertion sort,
        moving the items with the keyword to the top. Also sorts the items
        keyword values in alphabetical order.

        Example:
            {}
            {'name': 'milk', 'type': 'food'}
            {'name': 'meat', 'type': 'food'}

            after sort_by_keyword("name")

            {'name': 'meat', 'type': 'food'}
            {'name': 'milk', 'type': 'food'}
            {}

        Args:
            keyword (str): The string keyword argument to sort the inventory by
        """
        self.sort()
        for a in range(1, self.items_count):
            b = 0
            while True:
                # If both of the items contain the keyword
                index = a - b
                if (self.items_list[index].has_keyword(keyword)
                    and self.items_list[index - 1].has_keyword(keyword)):
                    first = self.items_list[index - 1].get(keyword)
                    second = self.items_list[index].get(keyword)
                    if (len(first) > len(second)): self._sort_swap(index)
                    for c in range(min(len(first), len(second))):
                        if ord(second[c]) < ord(first[c]):
                            self._sort_swap(index)
                            break
                else:
                    # If the first item does not contains the keyword and
                    # the second item does swap
                    if self.items_list[index].has_keyword(keyword) and (
                       not self.items_list[index - 1].has_keyword(keyword)):
                        self._sort_swap(index)
                if index - 1 == 0: break
                b += 1
        self._update()

    def _sort_swap(self, index):
        (self.items_list[index],
         self.items_list[index - 1]) = (self.items_list[index - 1],
                                        self.items_list[index])

    def has_space(self):
        """Returns true if at least one slot in
           the inventory is an empty Item"""
        return self.items_count != len(self.items_list)

    def get_first_empty(self):
        """Returns the first empty slot or -1 if the inventory is full"""
        if not self.has_space(): return -1
        for i in range(len(self.items_list)):
            if self.items_list[i].is_empty(): return i

    def get_items_with_kwargs(self, keyword, arg=None):
        """Returns a list of inventory items with the
           specific keyword argument.

        Args:
            keyword (str): The string keyword in the items kwargs
            arg: The optional argument that the keyword must equal
        Returns:
            A list of the inventory items that contain the keyword argument,
            and optionally limit the list to only the items that contain a
            specific value for the keyword argument.
        """
        out = []
        for i in self.items_list:
            if keyword in i.kwargs:
                if arg is None:
                    out.append(i)
                elif i.kwargs[keyword] == arg:
                    out.append(i)
        return out

    def __str__(self):
        out = "[ "
        for i in self.items_list:
            out += str(i).strip() + ", "
        out += "]"
        return out
