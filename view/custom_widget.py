import customtkinter as ctk


class IntegerInputField(ctk.CTkEntry):
    """Custom Entry widget that only accepts integer input."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(validate="key", border_width=1)
        self.configure(validatecommand=(self.register(self.validate_input), "%P"))

    @staticmethod
    def validate_input(value):
        if value.isdigit():
            return True
        elif value == "" or value == "-":
            return True
        else:
            return False


class ScrollableCheckBoxFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        checkbox = ctk.CTkCheckBox(self, text=item)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.configure(checkbox_width=16, checkbox_height=16)
        checkbox.grid(row=len(self.checkbox_list), column=0)
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]

    def get_boolean(self):
        return [True if checkbox.get() == 1 else False for checkbox in self.checkbox_list]
