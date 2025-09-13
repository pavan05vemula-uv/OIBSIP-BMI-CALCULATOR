import tkinter as tk
from tkinter import messagebox
from bmi import calculate_bmi, get_bmi_category
from database import create_tables, get_or_create_user, save_bmi_record, get_bmi_history
from plotter import plot_bmi_history

class BMIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator")
        self.root.configure(bg="#f0f8ff")  # Set background color

        self.username_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.height_var = tk.StringVar()

        self.build_ui()
        create_tables()

    def build_ui(self):
        label_font = ("Arial", 12)
        entry_font = ("Arial", 12)
        button_font = ("Arial", 11, "bold")

        # Styles
        label_style = {'bg': '#f0f8ff', 'font': label_font}
        entry_style = {'font': entry_font}

        # Username
        tk.Label(self.root, text="Username:", **label_style).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(self.root, textvariable=self.username_var, **entry_style).grid(row=0, column=1, padx=10, pady=5)

        # Weight
        tk.Label(self.root, text="Weight (kg):", **label_style).grid(row=1, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(self.root, textvariable=self.weight_var, **entry_style).grid(row=1, column=1, padx=10, pady=5)

        # Height
        tk.Label(self.root, text="Height (m):", **label_style).grid(row=2, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(self.root, textvariable=self.height_var, **entry_style).grid(row=2, column=1, padx=10, pady=5)

        # Calculate Button
        calc_button = tk.Button(
            self.root,
            text="Calculate BMI",
            command=self.calculate_bmi,
            bg="#4CAF50", fg="white",
            font=button_font,
            width=20,
            padx=5, pady=5
        )
        calc_button.grid(row=3, column=0, columnspan=2, pady=10)

        # View Trend Button
        trend_button = tk.Button(
            self.root,
            text="View BMI Trend",
            command=self.show_bmi_trend,
            bg="#2196F3", fg="white",
            font=button_font,
            width=20,
            padx=5, pady=5
        )
        trend_button.grid(row=4, column=0, columnspan=2, pady=5)

        # Output Label
        self.output_label = tk.Label(self.root, text="", fg="blue", bg="#f0f8ff", font=("Arial", 12, "bold"))
        self.output_label.grid(row=5, column=0, columnspan=2, pady=10)

    def calculate_bmi(self):
        try:
            username = self.username_var.get().strip()
            weight = float(self.weight_var.get())
            height = float(self.height_var.get())

            if weight <= 0 or height <= 0:
                raise ValueError("Height and weight must be positive numbers.")

            user_id = get_or_create_user(username)
            bmi = calculate_bmi(weight, height)
            category = get_bmi_category(bmi)
            save_bmi_record(user_id, bmi, category)

            self.output_label.config(text=f"BMI: {bmi:.2f} ({category})")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def show_bmi_trend(self):
        username = self.username_var.get().strip()
        if not username:
            messagebox.showerror("Error", "Enter a username first.")
            return
        user_id = get_or_create_user(username)
        records = get_bmi_history(user_id)
        if records:
            plot_bmi_history(records)
        else:
            messagebox.showinfo("No Data", "No BMI records found for this user.")
