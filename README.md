# MABR Control System - Automated Wastewater Monitoring

## Overview
This project involves automating and monitoring a **wastewater treatment system** by integrating **sensors, a data logger, and an industrial communication protocol (Modbus RTU)**. The system is designed to monitor and control a **Membrane Aerated Biofilm Reactor (MABR)** by handling **sensor data acquisition, logging, and communication** using serial and Modbus protocols.

## Project Structure
### **Python Scripts**
- `logger.py` - Sensor Monitoring & Data Logging to JSON
- `opc_server.py` - OPC UA Server & Data Sharing to inCTRL opsCTRL Edge
- `sonde.py` - Sonde Sensor Communication
- `modbus.py` - Modbus Sensor Data Retrieval & Calibration

### **Shell Scripts**
- `run2.sh` - Logger Script Automation
- `get_port.sh` - USB Device Identification

### **Configuration and Documentation Files**
- `config.json` - System configuration
- `README.md` - Project documentation
- `debug.log` - Log file for debugging
- `.python-version` - Python version specification

### **Data Storage Files**
- `sensor_data.json` - JSON file storing real-time sensor data

### **Hardware Design Files**
- `backplane_rev_2.brd` - Circuit board design
- `backplane_rev_2.sch` - Schematic design

---

## **Script Descriptions**
### **1. `logger.py` - Sensor Monitoring & Data Logging**
- Continuously **retrieves real-time sensor data** from connected devices.
- Writes sensor readings to **`sensor_data.json`** for external use.
- Acts as the primary data source for **OPC UA and opsCTRL Edge integration**.

#### **Relevance:**
Ensures accurate logging of wastewater parameters and provides data for external systems.

---

### **2. `opc_server.py` - OPC UA Server & Data Sharing to inCTRL opsCTRL Edge**
- Reads sensor data from **`sensor_data.json`**.
- Updates the **OPC UA Server** to allow real-time data access.
- Sends sensor readings to **inCTRL’s opsCTRL Edge** for remote monitoring and analysis.
- Handles **error logging** for connectivity issues.

#### **Relevance:**
Provides a standardized data-sharing mechanism for industrial automation and process control.

---

### **3. `sensor_data.json` - Real-time Sensor Data Storage**
- A **lightweight JSON file** that stores real-time wastewater treatment data.
- Continuously updated by **`logger.py`**.
- Read by **`opc_server.py`** to share data via **OPC UA and opsCTRL Edge**.

#### **Relevance:**
Acts as a data bridge between sensor monitoring and external integration systems.

---

### **4. `sonde.py` - Sonde Sensor Communication**
- Establishes a **serial connection** with a **sonde sensor** (water quality monitoring device).
- Retrieves **real-time water quality parameters** (e.g., pH, ammonia, nitrate levels).

#### **Relevance:**
Ensures continuous monitoring of water quality in the treatment process.

---

### **5. `modbus.py` - Modbus Sensor Data Retrieval & Calibration**
- Handles **Modbus RTU communication** for sensors using a serial port.
- Reads raw sensor data from **Modbus registers** and applies calibration to obtain meaningful values.

#### **Relevance:**
Ensures precise data collection from Modbus-based sensors used in wastewater treatment.

---

### **6. `run2.sh` - Logger Script Automation**
- Detects and assigns **correct serial ports** for sensors.
- Runs the **logger script** (`logger.py`) with detected ports.
- Prints the **assigned ports for debugging**.

#### **Relevance:**
Automates the startup process for continuous monitoring.

---

### **7. `get_port.sh` - USB Device Identification**
- Scans all **connected USB devices** and extracts their system paths.
- Identifies:
  - **Sonde sensor**
  - **Oxygen sensor**
  - **Arduino board** (if used for control)
- Outputs detected devices for use in `run2.sh`.

#### **Relevance:**
Ensures proper device identification before launching monitoring scripts.

---

## **Conclusion**
This set of scripts forms an **automated sensor monitoring system** for a wastewater treatment facility, ensuring:
- **Continuous water quality monitoring.**
- **Automated sensor communication & calibration.**
- **Integration with SCADA systems via OPC UA and inCTRL opsCTRL Edge.**
- **Efficient startup & debugging with automated scripts.**

---

## **Additional Concepts**
### **What is a GUI?**
A **GUI (Graphical User Interface)** is a visual way for users to interact with software applications. Instead of using command-line inputs, a GUI provides **buttons, text fields, graphs, and other interactive elements** to make software more user-friendly.
- The `sonde.py` script implements a GUI using **Tkinter** (Python’s built-in GUI library).
- It provides **real-time sensor data** (e.g., pH, dissolved oxygen, temperature) in a **clear, structured format**.
- Users can **view and analyze sensor readings** without needing to interact with raw serial data.

---

### **What is an OPC UA Server?**
An **OPC UA (Open Platform Communications Unified Architecture) server** is a **machine-to-machine communication protocol** designed for **industrial automation and process control**. It is used to securely exchange **real-time data** between **devices, sensors, and control systems**.
- The **OPC UA server** in `opc_server.py` gathers **real-time sensor data** (e.g., pH, ORP, NH₄, NO₃, ODO, temperature, etc.).
- Other software applications (**SCADA systems, HMIs, or data loggers**) can connect to the **OPC UA server** to access this data in real-time.
- It allows **remote monitoring and control** of the wastewater treatment process without directly connecting to the sensors.

#### **Think of an OPC UA server as a translator and messenger:**
- **Translator:** It collects raw data from sensors and organizes it in a structured format.
- **Messenger:** It allows different clients (dashboards, control systems, data loggers) to request or receive updates from the sensors.

---

### **What is inCTRL opsCTRL Edge?**
**inCTRL opsCTRL Edge** is an industrial automation platform for **monitoring, analyzing, and optimizing process data**. 
- The `opc_server.py` script sends **real-time sensor data** to **opsCTRL Edge** using **HTTP requests**.
- This enables **remote monitoring** and **data-driven optimization** of wastewater treatment operations.

---

## **License**
This project is open-source and can be modified or extended to fit various wastewater treatment applications.

---

### **Contact**
For questions or contributions, feel free to submit an issue or pull request on GitHub.
