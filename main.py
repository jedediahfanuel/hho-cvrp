import tkinter as tk


class IntegerInputField(tk.Entry):
    """Custom Entry widget that only accepts integer input."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(validate='key')
        self.configure(validatecommand=(self.register(self.validate_input), '%P'))

    @staticmethod
    def validate_input(value):
        if value.isdigit():
            return True
        elif value == '' or value == '-':
            return True
        else:
            return False


def validate_button(*args):
    # Check if input values are valid integers greater than or equal to 1
    if iteration_input.get().isdigit() \
            and population_input.get().isdigit() \
            and int(iteration_input.get()) >= 1 \
            and int(population_input.get()) >= 1:
        submit_button.config(state='normal')
    else:
        submit_button.config(state='disabled')


def submit_button_callback():
    # Handle input values
    print(f"Iteration: {iteration_input.get()}")
    print(f"Population: {population_input.get()}")
    selected_items = [items_listbox.get(idx) for idx in items_listbox.curselection()]
    print(f"Selected Items: {selected_items}")


# Create main window
root = tk.Tk()
root.title("Integer Input Fields")
root.configure(bg="white")

# Create input fields
iteration_label = tk.Label(root, text="Iteration:", bg="white")
iteration_input = IntegerInputField(root)
iteration_input.bind('<KeyRelease>', validate_button)

population_label = tk.Label(root, text="Population:", bg="white")
population_input = IntegerInputField(root)
population_input.bind('<KeyRelease>', validate_button)

# Create dropdown menu with checkboxes
items = ['Item 1', 'Item 2', 'Item 3']
items_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, exportselection=False)
for item in items:
    items_listbox.insert(tk.END, item)
items_label = tk.Label(root, text="Instances:", bg="white")

# Create submit button
submit_button = tk.Button(root, text="Submit", command=submit_button_callback, state='disabled')

# Arrange widgets in grid
iteration_label.grid(row=0, column=0, padx=5, pady=5, sticky='E')
iteration_input.grid(row=0, column=1, padx=5, pady=5, sticky='W')
population_label.grid(row=1, column=0, padx=5, pady=5, sticky='E')
population_input.grid(row=1, column=1, padx=5, pady=5, sticky='W')
items_label.grid(row=2, column=0, padx=5, pady=5, sticky='E')
items_listbox.grid(row=2, column=1, padx=5, pady=5, sticky='W')
submit_button.grid(row=3, column=1, padx=5, pady=5, sticky='E')

# Run main event loop
root.mainloop()
