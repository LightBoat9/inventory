import ast


class Item(object):
    """Represents an item that can be stored in the inventory

    The item takes in as many named arguments as necessary that describe the item

    Example:
        Item(name="health pot", category="pots")
    """
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def get(self, keyword):
        """Returns the argument for the items keyword attribute.

        This can also be accessed by directly accessing the items kwargs dictionary. However this function will return
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
            The argument for the keyword or None if the keyword does not exist.
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

    def is_empty(self):
        """Returns true if the item was created with no keyword arguments"""
        return len(self.kwargs) == 0

    def __str__(self):
        return str(self.kwargs) + "\n"


class Inventory(object):
    """Represents a basic inventory for item management

    The inventory will take in a filepath to the inventory text file and a size. The filepath should point to either
    an empty text file or a previously created inventory file. If the file exists and holds item data, then the item
    data is used to create the inventory. If the new inventory size differs from the file then the new inventory will
    be cut or extended. Otherwise a blank inventory will be instanced with the number of slots added.
    """
    def __init__(self, path, size):
        self.path = path
        self.size = size
        self.items_count = 0
        self.items_list = []
        self._update()

    def _update(self):
        """Reads the inventory file and cuts or extends it to fit the passed in size

        Iterates through the inventory file lines and parses the information into Item instances. This can cut and
        extend the current file if the size differs from the original inventory size, otherwise it loads the
        information into the new inventory instance.
        """
        _slot_count = 0

        with open(self.path, "r") as file:
            data = file.readlines()

        for i in range(min(len(data), self.size)):
            keys = data[i].rstrip()
            if keys:  # Ignores empty lines
                self.items_list.append(Item(**ast.literal_eval(keys)))
                if not self.items_list[i].is_empty(): self.items_count += 1
                _slot_count += 1

        with open(self.path, "w") as file:
            for i in range(self.size):
                if i >= _slot_count: self.items_list.append(Item())
                file.write(str(self.items_list[i]))

    def add(self, item, slot):
        """Adds an item to the inventory.

        Adds the passed in Item instance to the inventory at the passed in slot number.

        Args:
            item (Item): instance of the item to add.
            slot (int): integer inventory slot.

        Raises:
            ValueError: if slot is negative or greater than or equal to the inventory size
        """
        if slot < 0: raise ValueError("slot can not be negative")
        if slot >= self.size: raise ValueError("slot can not be larger than inventory size")

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
            ValueError: if slot is negative or greater than or equal to the inventory size
        """
        if slot < 0: raise ValueError("slot can not be negative")
        if slot >= self.size: raise ValueError("slot can not be larger than inventory size")

        item = self.items_list[slot]

        with open(self.path, "r") as file:
            data = file.readlines()

        self.items_list[slot] = Item()
        data[slot] = str(self.items_list[slot])

        with open(self.path, "w") as file:
            file.writelines(data)

        return item

    def has_space(self):
        """Returns true if at least one slot in the inventory is empty"""
        return self.items_count != len(self.items_list)

    def get_first_empty(self):
        """Returns the first empty slot or -1 if the inventory is full"""
        if not self.has_space(): return -1
        for i in range(len(self.items_list)):
            if self.items_list[i].is_empty(): return i

    def get_items_with_kwargs(self, arg, arg_value=None):
        """Returns a list of the inventory items that contain the keyword argument, and optionally limit the list to
        only the items that contain a specific value for the keyword argument"""
        out = []
        for i in self.items_list:
            if arg in i.kwargs:
                if arg_value is None:
                    out.append(i)
                elif i.kwargs[arg] == arg_value:
                    out.append(i)
        return out

    def __str__(self):
        out = "[ "
        for i in self.items_list:
            out += str(i).strip() + ", "
        out += "]"
        return out
