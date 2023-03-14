import cvrplib
import threading
import tkinter as tk
from tkinter import filedialog

from controller import configure

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


def run():
    def validate_inputs(*args):
        # Check if input values are valid integers greater than or equal to 1
        if iteration_input.get().isdigit() \
                and population_input.get().isdigit() \
                and nruns_input.get().isdigit() \
                and int(iteration_input.get()) > 0 \
                and int(population_input.get()) > 0 \
                and int(nruns_input.get()) > 0 \
                and items_listbox.curselection() \
                and city_size_input.get().isdigit() \
                and int(city_size_input.get()) > 0 \
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
                [items_listbox.get(idx) for idx in items_listbox.curselection()],
                [i in export_listbox.curselection() for i in range(7)],
                path_input.get(),
                None,
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

    def select_directory():
        path_entry.config(state=tk.NORMAL)

        # get the directory path using the file dialog
        directory_path = filedialog.askdirectory()

        # update the path entry field with the selected directory path
        path_entry.delete(0, tk.END)
        path_entry.insert(0, directory_path)

        path_entry.config(state=tk.DISABLED)

    # Create main window
    root = tk.Tk()
    root.title("HHO-CVRP")
    root.configure(bg="white")

    # Left frame
    left_frame = tk.Frame(root, padx=5, pady=5, bg="white")
    left_frame.grid(row=0, column=0)

    # Create input fields
    nruns_label = tk.Label(left_frame, text="Num of run:", bg="white")
    nruns_input = IntegerInputField(left_frame)
    nruns_input.insert(0, "5")
    nruns_input.bind("<KeyRelease>", validate_inputs)

    population_label = tk.Label(left_frame, text="Population:", bg="white")
    population_input = IntegerInputField(left_frame)
    population_input.insert(0, "20")
    population_input.bind("<KeyRelease>", validate_inputs)

    iteration_label = tk.Label(left_frame, text="Iteration:", bg="white")
    iteration_input = IntegerInputField(left_frame)
    iteration_input.insert(0, "500")
    iteration_input.bind("<KeyRelease>", validate_inputs)

    # Create dropdown menu with checkboxes
    items = cvrplib.list_names(vrp_type="cvrp")
    items_label = tk.Label(left_frame, text="Instances:", bg="white")
    items_listbox = tk.Listbox(left_frame, selectmode=tk.MULTIPLE, height=8, exportselection=False)
    for item in items:
        items_listbox.insert(tk.END, item)
    items_listbox.bind("<<ListboxSelect>>", validate_inputs)

    # Create process label
    process_label = tk.Label(left_frame, text="", bg="white")

    # Create submit button
    submit_button = tk.Button(left_frame, text="Submit", command=submit_button_callback, state="disabled")

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

    # Right frame
    right_frame = tk.Frame(root, padx=5, pady=5, bg="white")
    right_frame.grid(row=0, column=1)

    path_button = tk.Button(right_frame, text="Path", command=select_directory)
    path_input = tk.StringVar(right_frame)
    path_input.set("")
    path_entry = tk.Entry(right_frame, textvariable=path_input, state=tk.DISABLED)
    path_input.trace("w", validate_inputs)

    city_size_label = tk.Label(right_frame, text="City Size:", bg="white")
    city_size_input = IntegerInputField(right_frame)
    city_size_input.insert(0, "10")
    city_size_input.bind("<KeyRelease>", validate_inputs)

    city_id_label = tk.Label(right_frame, text="Display City ID:", bg="white")
    city_id_listbox = tk.Listbox(right_frame, selectmode=tk.SINGLE, height=2, exportselection=False)
    for item in ["True", "False"]:
        city_id_listbox.insert(tk.END, item)
    city_id_listbox.bind("<<ListboxSelect>>", validate_inputs)
    city_id_listbox.select_set(1)

    export_label = tk.Label(right_frame, text="Export Flag:", bg="white")
    export_listbox = tk.Listbox(right_frame, selectmode=tk.MULTIPLE, height=5, exportselection=False)
    for item in ["Boxplot", "Configuration", "Convergence", "Route", "Scatter-plot"]:
        export_listbox.insert(tk.END, item)
    export_listbox.bind("<<ListboxSelect>>", validate_inputs)
    export_listbox.select_set(0, tk.END)

    # Arrange widgets in grid
    path_button.grid(row=0, column=0, padx=5, pady=5, sticky="E")
    path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="W")

    city_size_label.grid(row=1, column=0, padx=5, pady=5, sticky="E")
    city_size_input.grid(row=1, column=1, padx=5, pady=5, sticky="W")

    city_id_label.grid(row=2, column=0, padx=5, pady=5, sticky="E")
    city_id_listbox.grid(row=2, column=1, padx=5, pady=5, sticky="W")

    export_label.grid(row=3, column=0, padx=5, pady=5, sticky="E")
    export_listbox.grid(row=3, column=1, padx=5, pady=5, sticky="W")

    # Run main event loop
    root.mainloop()
