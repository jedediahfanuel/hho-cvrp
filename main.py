import tkinter as tk
import cvrplib
import configure
import threading

running = False


class IntegerInputField(tk.Entry):
    """Custom Entry widget that only accepts integer input."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(validate="key")
        self.configure(validatecommand=(self.register(self.validate_input), "%P"))

    @staticmethod
    def validate_input(value):
        if value.isdigit():
            return True
        elif value == "" or value == "-":
            return True
        else:
            return False


def validate_inputs(*args):
    # Check if input values are valid integers greater than or equal to 1
    if iteration_input.get().isdigit() \
            and population_input.get().isdigit() \
            and nruns_input.get().isdigit() \
            and int(iteration_input.get()) >= 1 \
            and int(population_input.get()) >= 1 \
            and int(nruns_input.get()) >= 1 \
            and items_listbox.curselection() \
            and not running:
        submit_button.config(state="normal")
    else:
        submit_button.config(state="disabled")


def submit_button_callback():
    process_label.config(text="Running")

    # disable submit button
    global running
    running = True
    submit_button.config(state="disabled")

    def run_hho():
        # Handle input values
        configure.conf(
            int(nruns_input.get()),
            int(population_input.get()),
            int(iteration_input.get()),
            [items_listbox.get(idx) for idx in items_listbox.curselection()]
        )

        root.after(0, lambda: update_ui())

    def update_ui():
        process_label.config(text="Completed")

        # enabling submit button
        global running
        running = False
        submit_button.config(state="normal")

    calculation_thread = threading.Thread(target=run_hho)
    calculation_thread.start()


# Create main window
root = tk.Tk()
root.title("HHO-CVRP")
root.configure(bg="white")

# Create input fields
nruns_label = tk.Label(root, text="Num of run:", bg="white")
nruns_input = IntegerInputField(root)
nruns_input.insert(0, "5")
nruns_input.bind("<KeyRelease>", validate_inputs)

population_label = tk.Label(root, text="Population:", bg="white")
population_input = IntegerInputField(root)
population_input.insert(0, "20")
population_input.bind("<KeyRelease>", validate_inputs)

iteration_label = tk.Label(root, text="Iteration:", bg="white")
iteration_input = IntegerInputField(root)
iteration_input.insert(0, "500")
iteration_input.bind("<KeyRelease>", validate_inputs)

# Create dropdown menu with checkboxes
items = cvrplib.list_names(vrp_type="cvrp")
items_label = tk.Label(root, text="Instances:", bg="white")
items_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, exportselection=False)
for item in items:
    items_listbox.insert(tk.END, item)
items_listbox.bind("<<ListboxSelect>>", validate_inputs)

# Create process label
process_label = tk.Label(root, text="", bg="white")

# Create submit button
submit_button = tk.Button(root, text="Submit", command=submit_button_callback, state="disabled")

# Arrange widgets in grid
nruns_label.grid(row=0, column=0, padx=5, pady=5, sticky="E")
nruns_input.grid(row=0, column=1, padx=5, pady=5, sticky="W")

population_label.grid(row=1, column=0, padx=5, pady=5, sticky="E")
population_input.grid(row=1, column=1, padx=5, pady=5, sticky="W")

iteration_label.grid(row=2, column=0, padx=5, pady=5, sticky="E")
iteration_input.grid(row=2, column=1, padx=5, pady=5, sticky="W")

items_label.grid(row=3, column=0, padx=5, pady=5, sticky="E")
items_listbox.grid(row=3, column=1, padx=5, pady=5, sticky="W")

process_label.grid(row=4, column=0, padx=5, pady=5, sticky="E")
submit_button.grid(row=4, column=1, padx=5, pady=5, sticky="W")

# Run main event loop
root.mainloop()
