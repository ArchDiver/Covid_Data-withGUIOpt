import pandas as pd
import tkinter as tk
import sys
from datetime import date
from tkinter import messagebox as tkmb
from tkinter import filedialog as tkfd
from tkinter import ttk
from pathvalidate import ValidationError, validate_filename, sanitize_filename
import covid_gui_funcs
from pandastable import Table, TableModel
from pathlib import Path
import logging as log
import os

CWD = os.getcwd()



log.basicConfig(
    filename="covid_gui.log",
    level=log.DEBUG,
    format="%(asctime)s:%(levelname)s:%(funcName)s:%(message)s",
)

############ All of the GUI setup ############################

root = tk.Tk()

root.title("Covid Data From John Hopkins")
# root.geometry("800x600") # Used with table
root.geometry("800x200")

root.columnconfigure(0, weight=1)
root.rowconfigure(3, weight=1)

# Input Excel file
excel_file_frame = tk.Frame(root)
excel_file_frame.columnconfigure(1, weight=1)
excel_file_var = tk.StringVar()
tk.Label(excel_file_frame, text="Choose the excel file: ").grid(
    sticky="we", padx=5, pady=5
)
excel_file_inp = tk.Entry(excel_file_frame, textvariable=excel_file_var)
excel_file_inp.insert(0, CWD + '\\covid_base.xlsx')
excel_file_inp.grid(row=0, column=1, sticky=tk.E + tk.W, padx=5, pady=5)
excel_file_frame.grid(sticky=tk.E + tk.W)
select_file_btn = tk.Button(excel_file_frame, text="Select file")
select_file_btn.grid(row=0, column=2, sticky=tk.E, ipadx=5, ipady=5)

# Output excel name
output_name_frame = tk.Frame(root)
output_name_frame.columnconfigure(1, weight=1)
output_name_var = tk.StringVar()
tk.Label(output_name_frame, text="What do you want to call the output file? : ").grid(
    sticky=tk.E + tk.W)
output_name_inp = tk.Entry(output_name_frame, textvariable=output_name_var)
output_name_inp.insert(0, ("Covid_Data_" + str(date.today())))
output_name_inp.grid(row=0, column=1, sticky=tk.E + tk.W)
output_name_frame.grid(sticky=tk.E + tk.W)

# # Table to show the data
# table_frame = tk.LabelFrame(root, text="Covid Data")
# table_frame.columnconfigure(0, weight=1)
# table_frame.grid(sticky=tk.N + tk.E + tk.S + tk.W)

# # # ## Treeview Widget
# tree = tk.ttk.Treeview(table_frame)
# hsb = tk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
# vsb = tk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
# tree.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
# tree.grid(column=0, row=0, sticky=tk.NSEW)
# vsb.grid(column=1, row=0, sticky=tk.NS)
# hsb.grid(column=0, row=1, sticky=tk.EW)
# table_frame.grid_columnconfigure(0, weight=1)
# table_frame.grid_rowconfigure(0, weight=1)


# Run Button
run_btn = tk.Button(root, text="Send Request")
run_btn.grid(row=0, column=1, sticky=tk.W, ipadx=5, ipady=5, padx=5, pady=5)

# #Table Button
# table_btn = tk.Button(root, text="Show Table")
# table_btn.grid(row=99, column=2, sticky=tk.W, ipadx=5, ipady=5, padx=5, pady=5)

# Save button
save_btn = tk.Button(root, text="Save")
save_btn.grid(row=1, column=1, sticky=tk.E, ipadx=5, ipady=5, padx=5, pady=5)

# Area for displaying messages
status_var = tk.StringVar()
status_bar = tk.Label(root, textvariable=status_var)
status_bar.grid(row=3, ipadx=5, ipady=5)


##################### Below is the Prog Functions ####################################


df_covid = pd.DataFrame([])


def select_file():
    """select the base_excel"""
    file_path = tkfd.askopenfilename(
        title="Select the excel file as a base: ", filetypes=[("excel", "*.xlsx")]
    )
    fp = Path(file_path)
    excel_file_var.set(fp)


select_file_btn.configure(command=select_file)


def run():
    """This runs the request """
    api_url = "https://covid-api.com/api/"
    global df_covid
    fp = excel_file_var.get()
    try:
      excel_filename = r"{}".format(fp)
      df_run = pd.read_excel(excel_filename)

    except ValueError:
        tkmb.showerror("Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
      tkmb.showerror("Information", f"No such file as {fp}")
      return None


    input_items = covid_gui_funcs.get_input_items(df_run)

    df_covid = covid_gui_funcs.build_excel_dataframe(api_url, input_items)
    status_var.set("Finished request")

run_btn.configure(command=run)


# def clear_data():
#   """Clears the Treeview of any data if you want to run again"""
#   tree.delete(*tree.get_children())
#   return None


# def show_table():
#   status_var.set("Creating Table")
#   global df_covid
#   clear_data()
#   # # table1["column"] = list(df_covid.columns)
#   # # table1["show"] = "headings"
#   # # for column in table1["columns"]:
#   # #   table1.heading(column, text=column) # let the column heading = column name
#   # #   status_var.set("Creating Table-Columns")

#   # # df_covid_rows = df_covid.to_numpy().tolist() # turns the dataframe into a list of lists
#   # # for row in df_covid_rows:
#   # #   table1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
#   # #   status_var.set("Creating Table-Rows")
#   # # status_var.set("Finished Creating Table")
#   # pt = Table(table_frame, dataframe=df_covid)
#   # pt.show()
#   # Create a Treeview with dual Scrollbars
#   tree = tk.ttk.Treeview(table_frame, show="headings", columns=df_covid.columns)
#   hsb = tk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
#   vsb = tk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
#   tree.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
#   tree.grid(column=0, row=0, sticky=tk.NSEW)
#   vsb.grid(column=1, row=0, sticky=tk.NS)
#   hsb.grid(column=0, row=1, sticky=tk.EW)
#   table_frame.grid_columnconfigure(0, weight=1)
#   table_frame.grid_rowconfigure(0, weight=1)

#   for i, header in enumerate(df_covid.columns):
#       tree.column(i, width=100, anchor='center')
#       tree.heading(i, text=header)
#   for row in range(df_covid.shape[0]):
#       tree.insert('', 'end', values=list(df_covid.iloc[row]))
#   return None


# table_btn.configure(command=show_table())


def filename_check(filename):
    run = True
    while run:
      try:
        validate_filename(filename)
        return filename
      except ValidationError as e:
        status_var.set("{}\n".format(e), file=sys.stderr)
        # print("{}\n".format(e), file=sys.stderr)
        filename = input(
            f"If you hit enter your new filename will be {sanitize_filename(filename)}, else enter a new filename: "
        ) or sanitize_filename(filename)


def get_save_name( excel_name=("Covid_Data_" + str(date.today()))):  # Sets default Name for the output file
    excel_name = filename_check( excel_name )  # Allows user to name the output file OR uses default
    return excel_name


def file_check(output_name):
    """Checks if the filename already exists"""
    run = True
    while run:
        if Path(output_name).exists():
            status_var.set(f"WARNING: {output_name} already exists")
        else:
            status_var.set("")
            output_name = get_save_name(output_name)
            return output_name


def save():
    """
    This takes in the dataframe and the save file name and creates the xslx file
    """
    global df_covid
    if df_covid.empty:
        status_var.set("There is nothing to save.")

    output_name = output_name_var.get()
    output_name = file_check(output_name)

    covid_gui_funcs.save_excel(df_covid, output_name)
    status_var.set(f"{output_name}.xlsx \n was saved to \n{CWD}")


save_btn.configure(command=save)

root.mainloop()
