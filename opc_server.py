from opcua import Server
import time
import json
import requests

# Load configuration settings (for inCTRL opsCTRL integration)
CONFIG_FILE = "config.json"
SENSOR_DATA_FILE = "sensor_data.json"

def load_config():
    """Loads configuration settings from config.json."""
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

def read_sensor_data():
    """Reads sensor data from sensor_data.json."""
    try:
        with open(SENSOR_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"pH": 0.0, "ORP": 0.0, "NH4": 0.0, "NO3": 0.0, "ODO": 0.0, "Temperature": 0.0}

# Initialize OPC UA Server
server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/mabr_server/")  # Set the server URL
server.set_server_name("MABR_OPC_UA_Server")

# Create a new address space for MABR data
uri = "http://mabr.system"
idx = server.register_namespace(uri)

# Create an object to store sensor data
mabr_object = server.nodes.objects.add_object(idx, "MABR_Sensors")

# Define variables (data points from the logger)
sensor_data = {
    "pH": mabr_object.add_variable(idx, "pH", 0.0),
    "ORP": mabr_object.add_variable(idx, "ORP", 0.0),
    "NH4": mabr_object.add_variable(idx, "NH4", 0.0),
    "NO3": mabr_object.add_variable(idx, "NO3", 0.0),
    "ODO": mabr_object.add_variable(idx, "ODO", 0.0),
    "Temperature": mabr_object.add_variable(idx, "Temperature", 0.0)
}

# Set variables as writable
for var in sensor_data.values():
    var.set_writable()

# Start OPC UA server
server.start()
print("OPC UA Server started at opc.tcp://0.0.0.0:4840/mabr_server/")

try:
    while True:
        # Read updated sensor data from JSON file
        updated_values = read_sensor_data()
        
        # Update OPC UA variables
        for key, value in updated_values.items():
            sensor_data[key].set_value(value)

        # Send data to inCTRL opsCTRL Edge
        config = load_config()
        opsctrl_api_url = config.get("opsCTRL_api_url", "http://opsctrl-edge.local/api")
        
        payload = {"sensor_data": updated_values}
        
        try:
            response = requests.post(opsctrl_api_url, json=payload, timeout=5)
            if response.status_code == 200:
                print("Successfully sent data to inCTRL opsCTRL Edge.")
            else:
                print(f"Error sending data: {response.status_code}, {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to opsCTRL Edge: {e}")
        
        print("Updated OPC UA Server and sent data to inCTRL opsCTRL Edge")
        
        time.sleep(5)  # Update every 5 seconds

except KeyboardInterrupt:
    print("Shutting down OPC UA Server...")
    server.stop()
