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
        self._path = path
        self._size = size
        if size is None: self.size = self._get_file_length()
        self.items_count = 0
        self.items_list = []
        self._update()
        self._iter_i = 0

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path
        self.items_list = []
        self._update()

    @path.getter
    def path(self):
        return self._path

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size
        self.items_list = []
        self._update()

    @size.getter
    def size(self):
        return self._size

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

    def add(self, item):
        """Adds an item to the inventory.

        Adds the passed in Item instance to the inventory at the next empty
        slot. If no slot is empty then it will throw an InventoryFullError.
        Use has_space before adding an item without slot specified to ensure
        that no error is thrown.

        Args:
            item (Item): instance of the item to add.

        Raises:
            OverflowError: if slot is negative or greater than or equal to
                        the inventory size.
        """
        if not self.has_space(): raise OverflowError("Inventory has no empty slots left")
        slot = self.find_first_empty()

        self.set(slot, item)

    def set(self, slot, item):
        """Adds the item to the specific inventory slot,

        The new item will replace the current item if one exists.

        Args:
            slot (int): optional integer inventory slot.
            item (Item): instance of the item to add.
        """
        if slot < 0: raise IndexError("slot can not be negative")
        if slot >= self.size:
            raise IndexError("slot can not be larger than inventory size")

        with open(self.path, "r") as file:
            data = file.readlines()
        data[slot] = str(item)
        with open(self.path, "w") as file:
            file.writelines(data)

        if self.items_list[slot].is_empty(): self.items_count += 1
        self.items_list[slot] = item

    def get(self, slot):
        """Returns the item instance at the inventory slot"""
        if slot < 0: raise ValueError("slot can not be negative")
        if slot >= self.size:
            raise ValueError("slot can not be larger than inventory size")
        if self.items_list[slot].is_empty():
            return None
        return self.items_list[slot]

    def remove(self, item):
        i = self.find(item)
        if i == -1: raise NoSuchItemError("can not remove item that does not exist")
        return self.remove_from(i)

    def remove_from(self, slot):
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
        if item.is_empty(): raise SlotEmptyError("can not remove item from empty inventory slot")

        # _update not used because only one line needs to be changed.
        with open(self.path, "r") as file:
            data = file.readlines()

        self.items_list[slot] = Item()
        data[slot] = str(self.items_list[slot])

        with open(self.path, "w") as file:
            file.writelines(data)

        self.items_count -= 1

        return item

    def remove_first(self):
        item = self.remove_from(self.find_first_item())
        if item == -1: raise NoSuchItemError
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

    def shift_down(self):
        """Sorts the inventory so that non-empty
           items come before empty items.

        Sorts the inventory using Insertion sort, pushing all existing items
        to the front of the inventory.

        Example:
            {}
            {'name': 'health potion'}

            After shift_down() becomes...

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

    def sort(self, keyword):
        """Sorts the inventory by keyword.

        Sorts the inventory using insertion sort,
        moving the items with the keyword to the top. Also sorts the items
        keyword values in alphabetical order.

        Args:
            keyword (str): The string keyword argument to sort the inventory by
        """
        self.shift_down()
        for a in range(1, self.items_count):
            b = 0
            while True:
                # If both of the items contain the keyword
                index = a - b
                first = self.items_list[index - 1].get(keyword)
                second = self.items_list[index].get(keyword)
                if first.isdigit() != second.isdigit():
                    raise TypeError("keyword argument values are of different types")

                if (self.items_list[index].has_keyword(keyword)
                    and self.items_list[index - 1].has_keyword(keyword)):
                    if len(first) > len(second): self._sort_swap(index)

                    if first.isdigit() and second.isdigit():
                        if int(second) < int(first):
                            self._sort_swap(index)
                    else:
                        for c in range(min(len(first), len(second))):
                            if ord(second[c]) < ord(first[c]):
                                self._sort_swap(index)
                            if second[c] != first[c]: break

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
           the inventory is an empty Item
        """
        return self.items_count != len(self.items_list)

    def is_empty(self):
        return self.items_count == 0

    def find(self, item):
        for a, b in enumerate(self.items_list):
            if b == item: return a
        return -1

    def find_first_item(self):
        for a, b in enumerate(self.items_list):
            if not b.is_empty(): return a
        return -1

    def find_first_empty(self):
        """Returns the first empty slot or -1 if the inventory is full"""
        if not self.has_space(): return -1
        for i in range(len(self.items_list)):
            if self.items_list[i].is_empty(): return i

    def get_empty_count(self):
        count = 0
        for i in self.items_list:
            if i.is_empty(): count += 1
        return count

    def get_first_item(self):
        for i in self.items_list:
            if i.is_empty(): return i

    def get_items(self):
        out = []
        for i in self.items_list:
            if not i.is_empty(): out.append(i)
        return out

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

    def _get_file_length(self):
        with open(self.path, "r") as file: data = file.readlines()
        return len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self._iter_i < self.size:
            self._iter_i += 1
            return self.items_list[self._iter_i - 1]
        self._iter_i = 0
        raise StopIteration

    def __contains__(self, item):
        return self.find(item) != -1

    def __getitem__(self, item):
        return self.get(item)

    def __len__(self):
        return self.items_count

    def __add__(self, other):
        inv = Inventory(self.path, self.size + other.size)
        count = 0
        for i in self:
            inv.set(count, i)
            count += 1
        for i in other:
            inv.set(count, i)
            count += 1
        return inv

    def __eq__(self, other):
        if len(self.items_list) != len(other.items_list): return False
        for i in range(len(self)):
            if self.items_list[i] != other.items_list[0]: return False
        return True

    def __lt__(self, other):
        return self.items_count < other.items_count

    def __le__(self, other):
        return self.items_count <= other.items_count

    def __str__(self):
        out = "[ "
        for i in self.items_list:
            out += str(i).strip() + ", "
        out += "]"
        return out


class SlotEmptyError(Exception): pass

class NoSuchItemError(Exception): pass