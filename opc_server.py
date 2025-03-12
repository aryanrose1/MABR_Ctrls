from opcua import Server
import time
import sqlite3
import json
import threading
import pandas as pd
import datetime
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Database file
DB_FILE = "sensor_data.db"
CONFIG_FILE = "config.json"
DROPBOX_PATH = "/home/cee/Dropbox/MABR_data/"

# Load configuration

def load_config():
    """Loads configuration settings from config.json."""
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

# Read sensor data from SQLite
def read_sensor_data():
    """Reads sensor data from SQLite."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT tag, value FROM sensor_data WHERE timestamp = (SELECT MAX(timestamp) FROM sensor_data)")
    data = {tag: value for tag, value in cursor.fetchall()}
    conn.close()
    return data if data else {"pH": 0.0, "ORP": 0.0, "NH4": 0.0, "NO3": 0.0, "ODO": 0.0, "Temperature": 0.0}

# Export daily CSV to Dropbox
def export_daily_csv():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Get yesterday's date
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    start_time = f"{yesterday} 00:00:00"
    end_time = f"{yesterday} 23:59:59"

    # Query last 24 hours of data
    query = f"""
    SELECT * FROM sensor_data
    WHERE timestamp BETWEEN '{start_time}' AND '{end_time}'
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Generate CSV filename
    csv_filename = f"{DROPBOX_PATH}sensor_data_{yesterday}.csv"
    df.to_csv(csv_filename, index=False)
    print(f"Exported daily CSV to {csv_filename}")

# Initialize OPC UA Server
server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/mabr_server/")  # Set the server URL
server.set_server_name("MABR_OPC_UA_Server")
uri = "http://mabr.system"
idx = server.register_namespace(uri)

# Create an object to store sensor data
mabr_object = server.nodes.objects.add_object(idx, "MABR_Sensors")

# Load existing tags
def load_tags():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT tag FROM tags")
    tags = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tags

sensor_data = {}
for tag in load_tags():
    opc_variable = mabr_object.add_variable(idx, tag, 0.0)
    opc_variable.set_writable()
    sensor_data[tag] = opc_variable

# GUI for adding tags
def add_tag(tag_name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO tags (tag) VALUES (?)", (tag_name,))
        conn.commit()
        opc_variable = mabr_object.add_variable(idx, tag_name, 0.0)
        opc_variable.set_writable()
        sensor_data[tag_name] = opc_variable
        print(f"Added new OPC UA tag: {tag_name}")
    except sqlite3.IntegrityError:
        print(f"Tag {tag_name} already exists.")
    conn.close()

def import_tags_from_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
    if not file_path:
        return
    df = pd.read_excel(file_path)
    for tag in df.iloc[:, 0].dropna():
        add_tag(tag.strip())
    messagebox.showinfo("Success", "Tags imported successfully.")

def tag_manager_gui():
    root = tk.Tk()
    root.title("Tag Manager")
    
    tk.Label(root, text="Enter New Tag Name:").pack()
    tag_entry = tk.Entry(root)
    tag_entry.pack()
    tk.Button(root, text="Add Tag", command=lambda: add_tag(tag_entry.get())).pack()
    tk.Button(root, text="Import Tags from Excel", command=import_tags_from_excel).pack()
    tk.Button(root, text="Close", command=root.destroy).pack()
    
    root.mainloop()

# Start OPC UA server
server.start()
print("OPC UA Server started at opc.tcp://0.0.0.0:4840/mabr_server/")

# Start GUI in a separate thread
threading.Thread(target=tag_manager_gui, daemon=True).start()

try:
    while True:
        updated_values = read_sensor_data()
        for key, value in updated_values.items():
            if key in sensor_data:
                sensor_data[key].set_value(value)
        
        # Run daily CSV export at midnight
        current_time = datetime.datetime.now()
        if current_time.hour == 0 and current_time.minute == 0:
            export_daily_csv()
        
        time.sleep(60)  # Check every minute

except KeyboardInterrupt:
    print("Shutting down OPC UA Server...")
    server.stop()
