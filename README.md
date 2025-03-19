# MABR Control System - Automated Wastewater Monitoring

## Overview
This project involves automating and monitoring a **wastewater treatment system** by integrating **sensors, a data logger, and an industrial communication protocol (Modbus RTU)**. The system is designed to monitor and control a **Membrane Aerated Biofilm Reactor (MABR)** by handling **sensor data acquisition, logging, and communication** using serial and Modbus protocols. 

This implementation now utilizes **SQLite** for structured data storage, **OPC UA with secure certificates** for external system integration, and **automated daily CSV exports** for data tracking.

## Project Structure
### **Python Scripts**
- `logger.py` - Sensor Monitoring & Data Logging to SQLite
- `opc_server.py` - OPC UA Server & Data Sharing to ifakFAST & Dropbox CSV Export
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
- `sensor_data.db` - SQLite database storing real-time sensor data
- `sensor_database.sql` - SQL script for database initialization
- Automated daily CSV files stored in **Dropbox**

### **Hardware Design Files**
- `backplane_rev_2.brd` - Circuit board design
- `backplane_rev_2.sch` - Schematic design

---

## **Script Descriptions**
### **1. `logger.py` - Sensor Monitoring & Data Logging**
- Continuously **retrieves real-time sensor data** from connected devices.
- Stores sensor readings in **`sensor_data.db`** for structured data management.
- Serves as the primary data source for **OPC UA and external system integrations**.

#### **Relevance:**
Ensures accurate logging of wastewater parameters and provides structured, queryable data storage.

---

### **2. `opc_server.py` - OPC UA Server & Data Sharing to ifakFAST and Dropbox**
- Reads sensor data from **`sensor_data.db`**.
- Updates the **OPC UA Server** to allow real-time secure data access.
- Utilizes **self-signed certificates** for secure OPC UA communication.
- Exports daily CSV logs to **Dropbox** at midnight.
- Supports dynamic **tag management via GUI or Excel import**.

#### **Relevance:**
Provides a standardized and secure data-sharing mechanism for industrial automation and process control, while also generating historical records via CSV exports.

---

### **3. `sensor_data.db` - Real-time Sensor Data Storage**
- A **SQLite database** that stores timestamped wastewater treatment data.
- Continuously updated by **`logger.py`**.
- Read by **`opc_server.py`** to share data via **OPC UA and CSV exports**.

#### **Relevance:**
Acts as a structured data bridge between sensor monitoring and external integration systems, ensuring long-term storage and reliability.

---

### **4. `sensor_database.sql` - Database Initialization Script**
- Creates the **`sensor_data.db`** structure.
- Defines tables for **sensor data logging and OPC UA tags**.
- Ensures proper indexing and query efficiency.

#### **Relevance:**
This must be run **once** before starting the system to set up the database structure.

---

### **5. `sonde.py` - Sonde Sensor Communication**
- Establishes a **serial connection** with a **sonde sensor** (water quality monitoring device).
- Retrieves **real-time water quality parameters** (e.g., pH, ammonia, nitrate levels).

#### **Relevance:**
Ensures continuous monitoring of water quality in the treatment process.

---

### **6. `modbus.py` - Modbus Sensor Data Retrieval & Calibration**
- Handles **Modbus RTU communication** for sensors using a serial port.
- Reads raw sensor data from **Modbus registers** and applies calibration to obtain meaningful values.

#### **Relevance:**
Ensures precise data collection from Modbus-based sensors used in wastewater treatment.

---

### **7. `run2.sh` - Logger Script Automation**
- Detects and assigns **correct serial ports** for sensors.
- Runs the **logger script** (`logger.py`) with detected ports.
- Prints the **assigned ports for debugging**.

#### **Relevance:**
Automates the startup process for continuous monitoring.

---

### **8. `get_port.sh` - USB Device Identification**
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
This set of scripts forms an **automated, secure sensor monitoring system** for a wastewater treatment facility, ensuring:
- **Continuous water quality monitoring.**
- **Automated sensor communication & calibration.**
- **Secure integration with SCADA systems via OPC UA with certificates.**
- **Daily historical logging with automatic CSV exports to Dropbox.**
- **Efficient startup & debugging with automated scripts.**

---

## **Security & Data Access**
### **🔒 OPC UA Secure Access**
- The system **uses security certificates** for trusted communication.
- **Certificates must be added to ifakFAST’s trusted folder** for access.
- Only authorized systems can pull real-time data.

---

### **💾 Historical Data Storage & Access**
- **All sensor data is stored in `sensor_data.db`** for long-term analysis.
- **Automated daily CSV exports** provide external data tracking via Dropbox.
- **Query past sensor readings via SQLite.**

---

## **License**
This project is open-source and can be modified or extended to fit various wastewater treatment applications.

---

### **Contact**
For questions or contributions, feel free to submit an issue or pull request on GitHub.
