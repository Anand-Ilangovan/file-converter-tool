import csv
import xml.sax.saxutils
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import xml.etree.ElementTree as ET


# Function to convert text (TXT) to HTML
def txt_to_html(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    with open(output_file, 'w') as f:
        f.write('<html>\n<body>\n')
        for line in lines:
            f.write(f'<p>{line.strip()}</p>\n')
        f.write('</body>\n</html>')
    return output_file


# Function to convert CSV to HTML
def csv_to_html(input_file, output_file):
    html_content = '<html>\n<body>\n<table border="1">\n'
    
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            html_content += '<tr>'
            for field in row:
                html_content += f'<td>{field}</td>'
            html_content += '</tr>\n'
    
    html_content += '</table>\n</body>\n</html>'

    # Write the HTML content to the output file
    with open(output_file, 'w') as f:
        f.write(html_content)

    return output_file


# Function to convert text (TXT) to XML
def txt_to_xml(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    root = ET.Element("text")
    for line in lines:
        paragraph = ET.SubElement(root, "paragraph")
        paragraph.text = line.strip()

    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    return output_file


# Function to convert CSV to XML
def csv_to_xml(input_file, output_file, encoding='utf-8'):
    with open(input_file, 'r', encoding=encoding, errors='replace') as f:
        lines = f.readlines()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<data>\n')
        
        for line in lines:
            try:
                fields = line.strip().split(',')
                f.write('  <row>\n')
                for field in fields:
                    escaped_field = xml.sax.saxutils.escape(field)
                    f.write(f'    <field>{escaped_field}</field>\n')
                f.write('  </row>\n')
            except Exception as e:
                print(f"Error processing line: {e}")
        
        f.write('</data>')
    
    return output_file

# Function to handle file selection and display content
def select_file():
    input_file_path = filedialog.askopenfilename(title="Select input file",
                                                 filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
    if input_file_path:
        # Display contents of source file
        with open(input_file_path, 'r') as f:
            source_contents = f.read()
        source_text.delete('1.0', tk.END)
        source_text.insert(tk.END, source_contents)

        # Enable conversion format dropdown
        format_dropdown.config(state="readonly")

        # Enable convert button
        convert_button.config(state="normal")

        # Store the selected input file path
        global input_file_path_global
        input_file_path_global = input_file_path


# Function to handle conversion
def convert_file():
    if not input_file_path_global:
        tk.messagebox.showerror("Error", "Please select a file first.")
        return

    # Get selected conversion format
    conversion_format = format_dropdown.get()
    if conversion_format == "HTML":
        if input_file_path_global.endswith('.txt'):
            conversion_function = txt_to_html
        else:
            conversion_function = csv_to_html
        file_extension = '.html'
    elif conversion_format == "XML":
        if input_file_path_global.endswith('.txt'):
            conversion_function = txt_to_xml
        else:
            conversion_function = csv_to_xml
        file_extension = '.xml'
    else:
        tk.messagebox.showerror("Error", "Invalid conversion format.")
        return

    # Perform the conversion
    output_file_path = os.path.splitext(input_file_path_global)[0] + file_extension
    output_file_path = conversion_function(input_file_path_global, output_file_path)

    # Display contents of target file
    with open(output_file_path, 'r') as f:
        target_contents = f.read()
    target_text.delete('1.0', tk.END)
    target_text.insert(tk.END, target_contents)

    # Enable save button
    save_button.config(state="normal")

    # Store the path of the converted file
    global converted_file_path
    converted_file_path = output_file_path


# Function to save the converted file
# Function to save the converted file
def save_file():
    if not converted_file_path:
        tk.messagebox.showerror("Error", "No converted file to save.")
        return

    # Get the contents of the converted file
    with open(converted_file_path, 'r') as f:
        converted_content = f.read()

    # Get the directory of the input file
    output_directory = os.path.dirname(input_file_path_global)
    
    # Construct the output file path based on the input file path and the conversion format
    conversion_format = format_dropdown.get()
    output_file_name = os.path.splitext(os.path.basename(input_file_path_global))[0]  # Extract filename without extension
    output_file_path = os.path.join(output_directory, f"{output_file_name}.{conversion_format.lower()}")

    # Save the converted content to the output file
    with open(output_file_path, 'w') as f:
        f.write(converted_content)

    tk.messagebox.showinfo("Success", f"File saved successfully as {output_file_path}.")
  #  tk.messagebox.showinfo("Success", f"File saved successfully as {output_file_path}.")

# GUI setup
root = tk.Tk()
root.title("File Converter")

# Button to select file
select_button = tk.Button(root, text="Select File", command=select_file)
select_button.pack(pady=10)

# Dropdown box for conversion format (initially disabled)
format_label = tk.Label(root, text="Conversion Format:")
format_label.pack()
format_dropdown = ttk.Combobox(root, values=["HTML", "XML"], state="disabled")
format_dropdown.pack()

# Button to trigger file conversion (initially disabled)
convert_button = tk.Button(root, text="Convert File", command=convert_file, state="disabled")
convert_button.pack(pady=10)

# Text widgets to display file contents
source_label = tk.Label(root, text="Source File Contents:")
source_label.pack()
source_text = tk.Text(root, height=13, width=80)
source_text.pack()

target_label = tk.Label(root, text="Converted File Contents:")
target_label.pack()
target_text = tk.Text(root, height=13, width=80)
target_text.pack()

# Button to save the converted file (initially disabled)
save_button = tk.Button(root, text="Save File", command=save_file, state="disabled")
save_button.pack(pady=10)

input_file_path_global = None  # Store the path of the selected input file
converted_file_path = None  # Store the path of the converted file

root.mainloop()
