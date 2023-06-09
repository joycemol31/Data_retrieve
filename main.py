#Author: Joyce John
#This GUI loads COPDgene txt data and convert into a pandas dataframe for query
#The selected data is written out as a CSV

import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os
import subprocess

class DataSelector:
    def __init__(self, master):
        self.master = master
        master.title("Data Selector")

        # Create a label and an entry box for the file selection
        self.file_label = tk.Label(master, text="Select a data file:")
        self.file_label.grid(row=0, column=0, padx=5, pady=5)
        self.file_entry = tk.Entry(master)
        self.file_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_button = tk.Button(master, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        # Create a button to load the selected file and display its info
        self.load_button = tk.Button(master, text="Load File", command=self.load_file)
        self.load_button.grid(row=1, column=1, padx=5, pady=5)

        # Create labels and entry boxes for the conditions
        self.cond_label = tk.Label(master, text="Enter conditions:")
        self.cond_label.grid(row=2, column=0, padx=5, pady=5)

        self.cond_entries = []
        self.n_conds = 4  # number of conditions, can be changed as needed
        for i in range(self.n_conds):
            label = tk.Label(master, text=f"Column name for Condition {i+1}:")
            label.grid(row=i+3, column=0, padx=5, pady=5)
            entry = tk.Entry(master)
            entry.grid(row=i+3, column=1, padx=5, pady=5)
            self.cond_entries.append(entry)

            label = tk.Label(master, text=f"Condition {i+1} value:")
            label.grid(row=i+3, column=2, padx=5, pady=5)
            entry = tk.Entry(master)
            entry.grid(row=i+3, column=3, padx=5, pady=5)
            self.cond_entries.append(entry)

        # Create a button to apply the conditions and display the selected data
        self.select_button = tk.Button(master, text="Select Data", command=self.select_data)
        self.select_button.grid(row=self.n_conds+3, column=1, padx=5, pady=5)

        # Create a text widget to display the selected data
        self.data_text = tk.Text(master)
        self.data_text.grid(row=self.n_conds+4, column=0, columnspan=4, padx=5, pady=5)

        # Create a button to write the selected data to CSV
        self.write_button = tk.Button(master, text="Write CSV", command=self.write_csv)
        self.write_button.grid(row=self.n_conds + 3, column=2, padx=5, pady=5)

    def browse_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select a data file", filetypes=[("CSV files", "*.txt")])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, filename)

    def load_file(self):
        filename = self.file_entry.get()
        self.df = pd.read_csv(filename,sep='\t')

    # def select_data(self):
    #     conditions = []
    #     for i in range(self.n_conds):
    #         column_name = self.cond_entries[i*2].get()
    #         print(column_name)
    #         condition_value = self.cond_entries[i*2+1].get()
    #         print(condition_value)
    #         if column_name and condition_value:
    #             conditions.append((column_name, condition_value))
    #     if not conditions:
    #         return
    #     selected_data = self.df
    #     for column_name, condition_value in conditions:
    #         selected_data = selected_data[selected_data[column_name] == condition_value]
    #     self.show_data(selected_data)

    def select_data(self):
        conditions = []
        for i in range(self.n_conds):
            column_name = self.cond_entries[i * 2].get()
            condition_value = self.cond_entries[i * 2 + 1].get()
            if column_name and condition_value:
                # Check if condition_value is a number, and convert to int if it is
                try:
                    condition_value = int(condition_value)
                except ValueError:
                    pass
                conditions.append((column_name, condition_value))
        if not conditions:
            return
        self.selected_data = self.df
        for column_name, condition_value in conditions:
            # Check if condition_value is a number, and convert to int if it is
            if isinstance(condition_value, int):
                self.selected_data = self.selected_data[self.selected_data[column_name] == condition_value]
            else:
                self.selected_data = self.selected_data[self.selected_data[column_name] == condition_value]
        self.show_data(self.selected_data)

    # def show_data(self, data):
    #     top = tk.Toplevel(self.master)
    #     top.title("Selected Data")
    #     data_text = tk.Text(top)
    #     data_text.pack()
    #     data_text.insert(tk.END, data.to_string())

    def show_data(self, data):
        self.data_text.delete('1.0', tk.END)  # Clear previous data in the text box
        self.data_text.insert(tk.END, data.head())  # Insert the head of the selected data

    def write_csv(self):
        subset = ['sid','finalGold','cohort','gender','age_baseline']
        data_subset = self.selected_data[subset]
        data = data_subset.to_csv(index=False)
        if not data:
            return
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            with open(filename, "w") as f:
                f.write(data)
            subprocess.run(["xdg-open",filename])


root = tk.Tk()
selector = DataSelector(root)
root.mainloop()
