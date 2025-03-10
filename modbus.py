# =============================================================
# Modbus Sensor Data Retrieval & Calibration
# -------------------------------------------------------------
# This script communicates with a sensor using the Modbus RTU protocol
# to retrieve raw sensor readings and convert them into meaningful values
# using calibration data.
#
# Key Functions:
# 1. Connects to a Modbus RTU sensor via a serial port.
# 2. Reads raw sensor data from a specific register.
# 3. Uses a calibration function to map the raw values to actual units.
# 4. Handles errors in communication and ensures proper data retrieval.
# =============================================================

from pymodbus.client.sync import ModbusSerialClient  # Modbus RTU communication library

# --------------------------
# Calibration Constants
# --------------------------
# These values define how raw sensor data (in milliamps) is converted to meaningful measurements.
input_max = 20  # Maximum expected input value in mA
current_3 = 8.34  # Calibration point 3
percent_3 = 20.95  # Corresponding percentage for calibration point 3
current_2 = 5.425  # Calibration point 2
percent_2 = 10.475  # Corresponding percentage for calibration point 2
current_1 = 1.592  # Calibration point 1 (minimum)
percent_1 = 0  # Corresponding percentage for calibration point 1
output_max = 25  # Maximum expected output percentage

# Function to map raw sensor values to calibrated percentages
def map_value(value, input_min, input_max, output_min, output_max):
    """
    Converts a raw sensor reading (mA) into a calibrated percentage value
    using linear interpolation between known calibration points.
    """
    return output_min + (value - input_min) * (output_max - output_min) / (input_max - input_min)

# --------------------------
# Modbus RTU Configuration
# --------------------------
# This section configures the connection to the Modbus RTU device.
client = ModbusSerialClient(
    method="rtu",  # Modbus RTU mode
    port="COM8",  # Serial port (update based on your hardware setup)
    baudrate=9600,  # Communication speed in bits per second
    bytesize=8,  # Data byte size
    parity="N",  # No parity bit
    stopbits=1,  # Number of stop bits
    timeout=1  # Timeout for response in seconds
)

# --------------------------
# Continuous Data Retrieval
# --------------------------
while True:
    client.connect()  # Establish connection with the Modbus device

    slave_address = 5  # Address of the sensor on the Modbus network
    register_address = 7  # Memory location storing the sensor reading
    number_of_registers = 1  # We are reading a single data point

    # Read sensor data from the Modbus register
    response = client.read_input_registers(register_address, number_of_registers, unit=slave_address)

    if response.isError():  # Handle errors in communication
        print(f"Error in reading register: {response}")
    else:
        measuring_value_channel_1 = response.registers[0] * 0.001  # Convert raw value to mA
        
        # Apply calibration mapping to get a meaningful percentage value
        if measuring_value_channel_1 >= current_3:
            mapped_value = map_value(measuring_value_channel_1, current_3, input_max, percent_3, output_max)
        elif measuring_value_channel_1 >= current_2:
            mapped_value = map_value(measuring_value_channel_1, current_2, current_3, percent_2, percent_3)
        else:
            mapped_value = map_value(measuring_value_channel_1, current_1, current_2, percent_1, percent_2)

        # Apply linear extrapolation if values exceed the highest calibration point
        if measuring_value_channel_1 > current_3:
            slope = (percent_3 - percent_2) / (current_3 - current_2)
            intercept = percent_3 - slope * current_3
            mapped_value = slope * measuring_value_channel_1 + intercept

        # Display the raw and mapped values for reference
        print(f"Raw sensor value: {measuring_value_channel_1} mA, Calibrated Value: {mapped_value}%")

    client.close()  # Close the Modbus connection after each reading
