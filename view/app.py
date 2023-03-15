import cvrplib
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

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


class App:
    def __init__(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("HHO-CVRP")
        self.root.configure(bg="white")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Left frame
        self.left_frame = tk.Frame(self.root, padx=5, pady=5, bg="white")
        self.left_frame.grid(row=0, column=0)

        # Create input fields
        self.nruns_label = tk.Label(self.left_frame, text="Num of run:", bg="white")
        self.nruns_input = IntegerInputField(self.left_frame)
        self.nruns_input.insert(0, "5")
        self.nruns_input.bind("<KeyRelease>", self.validate_inputs)

        self.population_label = tk.Label(self.left_frame, text="Population:", bg="white")
        self.population_input = IntegerInputField(self.left_frame)
        self.population_input.insert(0, "20")
        self.population_input.bind("<KeyRelease>", self.validate_inputs)

        self.iteration_label = tk.Label(self.left_frame, text="Iteration:", bg="white")
        self.iteration_input = IntegerInputField(self.left_frame)
        self.iteration_input.insert(0, "500")
        self.iteration_input.bind("<KeyRelease>", self.validate_inputs)

        # Create dropdown menu with checkboxes
        self.items = cvrplib.list_names(vrp_type="cvrp")
        self.items_label = tk.Label(self.left_frame, text="Instances:", bg="white")
        self.items_listbox = tk.Listbox(self.left_frame, selectmode=tk.MULTIPLE, height=8, exportselection=False)
        for item in self.items:
            self.items_listbox.insert(tk.END, item)
        self.items_listbox.bind("<<ListboxSelect>>", self.validate_inputs)

        # Create process label
        self.process_label = tk.Label(self.left_frame, text="", bg="white")

        # Create submit button
        self.submit_button = tk.Button(self.left_frame, text="Submit", command=self.submit_button_callback, state="disabled")

        # Arrange widgets in grid
        self.nruns_label.grid(row=0, column=0, padx=5, pady=5, sticky="E")
        self.nruns_input.grid(row=0, column=1, padx=5, pady=5, sticky="W")

        self.population_label.grid(row=1, column=0, padx=5, pady=5, sticky="E")
        self.population_input.grid(row=1, column=1, padx=5, pady=5, sticky="W")

        self.iteration_label.grid(row=2, column=0, padx=5, pady=5, sticky="E")
        self.iteration_input.grid(row=2, column=1, padx=5, pady=5, sticky="W")

        self.items_label.grid(row=3, column=0, padx=5, pady=5, sticky="E")
        self.items_listbox.grid(row=3, column=1, padx=5, pady=5, sticky="W")

        self.process_label.grid(row=4, column=0, padx=5, pady=5, sticky="E")
        self.submit_button.grid(row=4, column=1, padx=5, pady=5, sticky="W")

        # Right frame
        self.right_frame = tk.Frame(self.root, padx=5, pady=5, bg="white")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.path_button = tk.Button(self.right_frame, text="Path", command=self.select_directory)
        self.path_input = tk.StringVar(self.right_frame)
        self.path_input.set("")
        self.path_entry = tk.Entry(self.right_frame, textvariable=self.path_input, state=tk.DISABLED)
        self.path_input.trace("w", self.validate_inputs)

        self.city_size_label = tk.Label(self.right_frame, text="City Size:", bg="white")
        self.city_size_input = IntegerInputField(self.right_frame)
        self.city_size_input.insert(0, "10")
        self.city_size_input.bind("<KeyRelease>", self.validate_inputs)

        self.city_id_label = tk.Label(self.right_frame, text="Display City ID:", bg="white")
        self.city_id_listbox = tk.Listbox(self.right_frame, selectmode=tk.SINGLE, height=2, exportselection=False)
        for item in ["False", "True"]:
            self.city_id_listbox.insert(tk.END, item)
        self.city_id_listbox.bind("<<ListboxSelect>>", self.validate_inputs)
        self.city_id_listbox.select_set(0)

        self.export_label = tk.Label(self.right_frame, text="Export Flag:", bg="white")
        self.export_listbox = tk.Listbox(self.right_frame, selectmode=tk.MULTIPLE, height=5, exportselection=False)
        for item in ["Boxplot", "Configuration", "Convergence", "Route", "Scatter-plot"]:
            self.export_listbox.insert(tk.END, item)
        self.export_listbox.bind("<<ListboxSelect>>", self.validate_inputs)
        self.export_listbox.select_set(0, tk.END)

        # Arrange widgets in grid
        self.path_button.grid(row=0, column=0, padx=5, pady=5, sticky="E")
        self.path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="W")

        self.city_size_label.grid(row=1, column=0, padx=5, pady=5, sticky="E")
        self.city_size_input.grid(row=1, column=1, padx=5, pady=5, sticky="W")

        self.city_id_label.grid(row=2, column=0, padx=5, pady=5, sticky="E")
        self.city_id_listbox.grid(row=2, column=1, padx=5, pady=5, sticky="W")

        self.export_label.grid(row=3, column=0, padx=5, pady=5, sticky="E")
        self.export_listbox.grid(row=3, column=1, padx=5, pady=5, sticky="W")

        # Progress Bar
        self.progress_label = tk.Label(self.right_frame, text="", bg="white")
        self.progress_bar = ttk.Progressbar(self.right_frame, orient=tk.HORIZONTAL,
                                            length=145, maximum=100, mode="determinate")
        self.progress_bar['value'] = 0

        self.progress_label.grid(row=4, column=0, padx=5, pady=5, sticky="E")
        self.progress_bar.grid(row=4, column=1, padx=5, pady=5, sticky="W")

        # Run main event loop
        self.root.mainloop()

    def validate_inputs(self, *args):
        # Check if input values are valid integers greater than or equal to 1
        if self.iteration_input.get().isdigit() \
                and self.population_input.get().isdigit() \
                and self.nruns_input.get().isdigit() \
                and int(self.iteration_input.get()) > 0 \
                and int(self.population_input.get()) > 0 \
                and int(self.nruns_input.get()) > 0 \
                and self.items_listbox.curselection() \
                and self.city_size_input.get().isdigit() \
                and int(self.city_size_input.get()) > 0 \
                and not running:
            self.submit_button.config(state=tk.NORMAL)
        else:
            self.submit_button.config(state=tk.DISABLED)

    def submit_button_callback(self):
        self.process_label.config(text="Running")
        self.progress_label.config(text="0%")
        self.progress_bar['value'] = 0

        # disable submit button
        global running
        running = True
        self.submit_button.config(state=tk.DISABLED)

        calculation_thread = threading.Thread(target=self.run_hho)
        calculation_thread.daemon = True
        calculation_thread.start()

    def run_hho(self):
        # Handle input values
        configure.conf(
            int(self.nruns_input.get()),
            int(self.population_input.get()),
            int(self.iteration_input.get()),
            [self.items_listbox.get(idx) for idx in self.items_listbox.curselection()],
            [i in self.export_listbox.curselection() for i in range(7)],
            int(self.city_size_input.get()),
            True if self.city_id_listbox.curselection()[0] else False,
            self.set_progress_bar_value,
            self.path_input.get()
        )

        self.root.after(0, lambda: self.update_ui())

    def update_ui(self):
        self.process_label.config(text="Completed")
        self.progress_label.config(text="100%")

        # enabling submit button
        global running
        running = False
        self.submit_button.config(state=tk.NORMAL)

    def select_directory(self):
        self.path_entry.config(state=tk.NORMAL)

        # get the directory path using the file dialog
        directory_path = filedialog.askdirectory()

        # update the path entry field with the selected directory path
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, directory_path)

        self.path_entry.config(state=tk.DISABLED)

    def set_progress_bar_value(self, value):
        self.progress_bar['value'] = round(value)
        self.progress_label.config(text=str(int(value))+"%")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
