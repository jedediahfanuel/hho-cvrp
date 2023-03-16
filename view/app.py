import cvrplib
import threading
import customtkinter as ctk

from tkinter import filedialog
from tkinter import messagebox
from controller import configure
from view.custom_widget import IntegerInputField
from view.custom_widget import ScrollableCheckBoxFrame

ctk.set_appearance_mode("Dark")
running = False
count = 0

class App:
    city_id = ""

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("HHO-CVRP")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Left frame
        self.left_frame = ctk.CTkFrame(self.root)
        self.left_frame.grid(row=0, column=0)

        # Create input fields
        self.nruns_label = ctk.CTkLabel(self.left_frame, text="Num of run:")
        self.nruns_label.configure(padx=5, pady=5)
        self.nruns_input = IntegerInputField(self.left_frame)
        self.nruns_input.insert(0, "5")
        self.nruns_input.bind("<KeyRelease>", self.validate_inputs)

        self.population_label = ctk.CTkLabel(self.left_frame, text="Population:")
        self.population_label.configure(padx=5, pady=5)
        self.population_input = IntegerInputField(self.left_frame)
        self.population_input.insert(0, "20")
        self.population_input.bind("<KeyRelease>", self.validate_inputs)

        self.iteration_label = ctk.CTkLabel(self.left_frame, text="Iteration:")
        self.iteration_label.configure(padx=5, pady=5)
        self.iteration_input = IntegerInputField(self.left_frame)
        self.iteration_input.insert(0, "500")
        self.iteration_input.bind("<KeyRelease>", self.validate_inputs)

        # Create dropdown menu with checkboxes
        self.items = cvrplib.list_names(vrp_type="cvrp")
        self.items_label = ctk.CTkLabel(self.left_frame, text="Instances:")
        self.items_label.configure(padx=5, pady=5)
        self.items_checkbox = ScrollableCheckBoxFrame(self.left_frame,
                                                      width=120,
                                                      command=self.validate_inputs,
                                                      item_list=self.items)

        # Create process label
        self.process_label = ctk.CTkLabel(self.left_frame, text="")
        self.process_label.configure(padx=5, pady=5)

        # Create submit button
        self.submit_button = ctk.CTkButton(self.left_frame, text="Submit", state="disabled", width=140,
                                           command=self.submit_button_callback)

        # Arrange left frame widgets in grid
        self.nruns_label.grid(row=0, column=0, sticky="E", padx=5, pady=5)
        self.nruns_input.grid(row=0, column=1, sticky="W", padx=5, pady=5)

        self.population_label.grid(row=1, column=0, sticky="E", padx=5, pady=5)
        self.population_input.grid(row=1, column=1, sticky="W", padx=5, pady=5)

        self.iteration_label.grid(row=2, column=0, sticky="E", padx=5, pady=5)
        self.iteration_input.grid(row=2, column=1, sticky="W", padx=5, pady=5)

        self.items_label.grid(row=3, column=0, sticky="E", padx=5, pady=5)
        self.items_checkbox.grid(row=3, column=1, sticky="W", padx=5, pady=5)

        self.process_label.grid(row=4, column=0, sticky="E", padx=5, pady=5)
        self.submit_button.grid(row=4, column=1, sticky="W", padx=5, pady=5)

        # Right frame
        self.right_frame = ctk.CTkFrame(self.root)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.path_button = ctk.CTkButton(self.right_frame, text="Path", width=50, command=self.select_directory)
        self.path_input = ctk.StringVar(self.right_frame)
        self.path_input.set("")
        self.path_entry = ctk.CTkEntry(self.right_frame, border_width=1, textvariable=self.path_input,
                                       state=ctk.DISABLED)
        self.path_input.trace("w", self.validate_inputs)

        self.city_size_label = ctk.CTkLabel(self.right_frame, text="City Size:")
        self.city_size_label.configure(padx=5, pady=5)
        self.city_size_input = IntegerInputField(self.right_frame, border_width=1)
        self.city_size_input.insert(0, "10")
        self.city_size_input.bind("<KeyRelease>", self.validate_inputs)

        self.city_id_label = ctk.CTkLabel(self.right_frame, text="Display City ID:")
        self.city_id_label.configure(padx=5, pady=5)
        self.city_id_dropdown = ctk.CTkOptionMenu(self.right_frame,
                                                  values=["True", "False"],
                                                  command=self.get_city_id)
        self.city_id_dropdown.set("False")

        self.export_label = ctk.CTkLabel(self.right_frame, text="Export Flag:")
        self.export_label.configure(padx=5, pady=5)
        self.export_checkbox = ScrollableCheckBoxFrame(self.right_frame,
                                                       width=118,
                                                       item_list=[
                                                           "Boxplot",
                                                           "Configuration",
                                                           "Convergence",
                                                           "Route",
                                                           "Scatter-plot"])

        # Arrange right frame widgets in grid
        self.path_button.grid(row=0, column=0, sticky="E", padx=5, pady=5)
        self.path_entry.grid(row=0, column=1, sticky="W", padx=5, pady=5)

        self.city_size_label.grid(row=1, column=0, sticky="E", padx=5, pady=5)
        self.city_size_input.grid(row=1, column=1, sticky="W", padx=5, pady=5)

        self.city_id_label.grid(row=2, column=0, sticky="E", padx=5, pady=5)
        self.city_id_dropdown.grid(row=2, column=1, sticky="W", padx=5, pady=5)

        self.export_label.grid(row=3, column=0, sticky="E", padx=5, pady=5)
        self.export_checkbox.grid(row=3, column=1, sticky="W", padx=5, pady=5)

        # Progress Bar
        self.progress_label = ctk.CTkLabel(self.right_frame, text="")
        self.progress_label.configure(padx=5, pady=5)
        self.progress_bar = ctk.CTkProgressBar(self.right_frame, orientation=ctk.HORIZONTAL,
                                               width=140, progress_color="green", mode="determinate")
        self.progress_bar.set(0)

        self.progress_label.grid(row=4, column=0, sticky="E", padx=5, pady=5)
        self.progress_bar.grid(row=4, column=1, sticky="W", padx=5, pady=5)

    def validate_inputs(self, *args):
        # Check if input values are valid integers greater than or equal to 1
        # and at least one instance is selected
        if self.iteration_input.get().isdigit() \
                and self.population_input.get().isdigit() \
                and self.nruns_input.get().isdigit() \
                and int(self.iteration_input.get()) > 0 \
                and int(self.population_input.get()) > 0 \
                and int(self.nruns_input.get()) > 0 \
                and self.items_checkbox.get_checked_items() \
                and self.city_size_input.get().isdigit() \
                and int(self.city_size_input.get()) > 0 \
                and not running:
            self.submit_button.configure(state=ctk.NORMAL)
        else:
            self.submit_button.configure(state=ctk.DISABLED)

    def submit_button_callback(self):
        self.process_label.configure(text="Running")
        self.progress_label.configure(text="0%")
        self.progress_bar.set(0)

        # disable submit button
        global running
        running = True
        self.submit_button.configure(state=ctk.DISABLED)

        calculation_thread = threading.Thread(target=self.run_hho)
        calculation_thread.daemon = True
        calculation_thread.start()

    def run_hho(self):
        # Handle input values
        configure.conf(
            int(self.nruns_input.get()),
            int(self.population_input.get()),
            int(self.iteration_input.get()),
            self.items_checkbox.get_checked_items(),
            self.export_checkbox.get_boolean(),
            int(self.city_size_input.get()),
            self.city_id,
            self.set_progress_bar_value,
            self.path_input.get()
        )

        self.root.after(0, lambda: self.update_ui())

    def update_ui(self):
        self.process_label.configure(text="Completed")
        self.progress_label.configure(text="100%")

        # enabling submit button
        global running
        running = False
        self.submit_button.configure(state=ctk.NORMAL)

    def select_directory(self):
        self.path_entry.configure(state=ctk.NORMAL)

        # get the directory path using the file dialog
        directory_path = filedialog.askdirectory()

        # update the path entry field with the selected directory path
        self.path_entry.delete(0, ctk.END)
        self.path_entry.insert(0, directory_path)

        self.path_entry.configure(state=ctk.DISABLED)

    def get_city_id(self, choice):
        if choice == "True":
            self.city_id = True
        else:
            self.city_id = False

    def set_progress_bar_value(self, value):
        self.progress_bar.set(value)
        self.progress_label.configure(text=str(int(value * 100)) + "%")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
