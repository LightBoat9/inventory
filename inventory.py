import ast
"""Game inventory save system"""

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
        """Returns the argument for the items keyword attribute, or None if it does not exist"""
        try:
            return self.kwargs[keyword]
        except KeyError:
            return None

    def set(self, keyword, arg):
        """Sets the value for the keyword in kwargs."""
        self.kwargs[keyword] = arg

    def _is_empty(self):
        return len(self.kwargs) == 0

    def __str__(self):
        return str(self.kwargs) + "\n"


class Inventory(object):
    """Represents a basic inventory for item management

    The inventory holds up to the passed in size amount of items
    """
    def __init__(self, size):
        self._size = size
        self._items_count = 0
        self._items_list = []
        for i in range(self._size):
            self._items_list.append(Item())
        self._iter_i = 0

    def load(self, path):
        """Loads the inventory from the passed in file"""
        with open(path, "r") as file:
            data = file.readlines()

        _slot_count = 0
        self._size = self._get_file_length(path)
        for i in range(min(len(data), self._size)):
            keys = data[i].rstrip()
            if keys:  # Ignores empty lines
                if i >= len(self._items_list):
                    self._items_list.append(Item(**ast.literal_eval(keys)))
                if not self._items_list[i]._is_empty(): self._items_count += 1
                _slot_count += 1

        for i in range(self._size):
            if i >= _slot_count: self._items_list.append(Item())

    def _get_file_length(self, path):
        with open(path, "r") as file: data = file.readlines()
        return len(data)

    def save(self, path):
        """Saves the inventory to the passed in file path"""
        open(path, "a").close()  # Create a blank file if it does not exist
        self._items_count = 0

        with open(path, "r") as file:
            data = file.readlines()

        with open(path, "w") as file:
            for i in range(self._size):
                file.write(str(self._items_list[i]))

    def sort(self, keyword=None):
        """Sorts the inventory by keyword."""
        for a in range(1, len(self._items_list)):  # Shits items down
            b = 0
            while (not self._items_list[a - b]._is_empty()
                   and self._items_list[a - b - 1]._is_empty()):
                self._sort_swap(a - b)
                if a - b - 1 == 0: break
                b += 1
        for a in range(1, self._items_count):
            b = 0
            while True:
                # If both of the items contain the keyword
                index = a - b
                first = self._items_list[index - 1].get(keyword)
                second = self._items_list[index].get(keyword)
                if first is None or second is None: break
                if first.isdigit() != second.isdigit():
                    raise TypeError("keyword argument values are of different types")

                if (self._items_list[index].get(keyword) is not None and
                        self._items_list[index - 1].get(keyword) is not None):
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
                    if self._items_list[index].get(keyword) is not None and (
                            not self._items_list[index - 1].get(keyword) is not None):
                        self._sort_swap(index)
                if index - 1 == 0: break
                b += 1

    def _sort_swap(self, index):
        (self._items_list[index],
         self._items_list[index - 1]) = (self._items_list[index - 1],
                                         self._items_list[index])

    def add(self, item):
        """Adds an item to the inventory at the first empty slot"""
        if self.is_full(): raise OverflowError("Inventory has no empty slots left")
        slot = self.find_first_empty()

        self.set(slot, item)

    def set(self, slot, item):
        """Adds the item to the specific inventory slot"""
        if slot < 0: raise IndexError("slot can not be negative")
        if slot >= self._size:
            raise IndexError("slot can not be larger than inventory size")

        if self._items_list[slot]._is_empty(): self._items_count += 1
        self._items_list[slot] = item

    def set_size(self, size):
        """Sets the number of items the inventory can hold"""
        self._size = size
        self._items_count = 0
        for i in range(size):
            if i < len(self._items_list):
                if not self._items_list[i]._is_empty(): self._items_count += 1
            else:
                self._items_list.append(Item())
        self._items_list = self._items_list[:size]

    def find(self, item):
        """Finds the index of the passed in item"""
        for a, b in enumerate(self._items_list):
            if b == item: return a
        return -1

    def find_first_item(self):
        """Finds the index of the first item in the inventory or -1 if the inventory is empty"""
        if self.is_empty(): return -1
        for a, b in enumerate(self._items_list):
            if not b._is_empty(): return a

    def find_first_empty(self):
        """Returns the first empty slot or -1 if the inventory is full"""
        if self.is_full(): return -1
        for i in range(len(self._items_list)):
            if self._items_list[i]._is_empty(): return i

    def get(self, slot):
        """Returns the item instance at the inventory slot"""
        if slot < 0: raise ValueError("slot can not be negative")
        if slot >= self._size: raise ValueError("slot can not be larger than inventory size")
        if self._items_list[slot]._is_empty():
            return None
        return self._items_list[slot]

    def get_empty_count(self):
        """Returns the number of inventory slots that are empty"""
        count = 0
        for i in self._items_list:
            if i._is_empty(): count += 1
        return count

    def get_items_count(self, item=None):
        """Returns the number of items or the number of instances of the passed in item"""
        if item is None: return self._items_count
        count = 0
        for i in self:
            if i == item: count += 1
        return count

    def get_items(self):
        out = []
        for i in self._items_list:
            if not i._is_empty(): out.append(i)
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
        for i in self._items_list:
            if keyword in i.kwargs:
                if arg is None:
                    out.append(i)
                elif i.kwargs[keyword] == arg:
                    out.append(i)
        return out

    def get_size(self):
        """Returns the size of the inventory i.e. the amount of items the inventory can hold"""
        return self._size

    def is_full(self):
        """Returns true if the inventory has no empty slots"""
        return self._items_count == len(self._items_list)

    def is_empty(self):
        return self._items_count == 0

    def remove(self, item):
        i = self.find(item)
        if i == -1: raise SlotEmptyError("can not remove item from empty inventory slot")
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
        if slot >= self._size:
            raise ValueError("slot can not be larger than inventory size")

        item = self._items_list[slot]
        if item._is_empty(): raise SlotEmptyError("can not remove item from empty inventory slot")

        self._items_list[slot] = Item()
        self._items_count -= 1

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
        for i, item in enumerate(self._items_list):
            if not item._is_empty():
                items.append(self._items_list[i])
                self._items_list[i] = Item()
        self._items_count = 0

        return items

    def __iter__(self):
        return self

    def __next__(self):
        if self._iter_i < self._size:
            self._iter_i += 1
            return self._items_list[self._iter_i - 1]
        self._iter_i = 0
        raise StopIteration

    def __contains__(self, item):
        return self.find(item) != -1

    def __getitem__(self, item):
        return self.get(item)

    def __len__(self):
        return self._items_count

    def __add__(self, other):
        inv = Inventory(self._size + other.get_size())
        count = 0
        for i in self:
            inv.set(count, i)
            count += 1
        for i in other:
            inv.set(count, i)
            count += 1
        return inv

    def __eq__(self, other):
        if len(self._items_list) != len(other._items_list): return False
        for i in range(len(self)):
            if self._items_list[i] != other._items_list[0]: return False
        return True

    def __lt__(self, other):
        return self._items_count < other._items_count

    def __le__(self, other):
        return self._items_count <= other._items_count

    def __str__(self):
        out = "[ "
        for i in self._items_list:
            out += str(i).strip() + ", "
        out += "]"
        return out


class SlotEmptyError(Exception): pass