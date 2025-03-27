import json
import serial
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import AccountSet, Memo

# Connect to XRPL Testnet
client = JsonRpcClient("https://s.altnet.rippletest.net:51234/")
wallet = Wallet.from_seed("sEdS2sDUbeCnqEerx2GtgyaSNYrAG7V")  # Replace with actual seed
wallet_address = wallet.classic_address  # Get the wallet address

# Open the serial port for ESP32 (COM6)
ser = serial.Serial("COM6", 115200, timeout=1)

print("Listening to ESP32 on COM6...")

def process_sensor_data(line):
    """Processes the received sensor data and creates an XRPL transaction."""
    try:
        sensor_data = json.loads(line)  # Parse JSON data
        print("Received:", sensor_data)

        # Convert data into a memo format for XRPL
        memo_data = json.dumps(sensor_data).encode("utf-8").hex()

        # Create a dummy transaction with only a memo (NO XRP transfer)
        transaction = AccountSet(
            account=wallet_address,
            memos=[Memo(memo_data=memo_data)]
        )
        print("Transaction created:", transaction)
    
    except json.JSONDecodeError as e:
        print("JSON Error:", e)

while True:
    try:
        # Read data from COM6 (ESP32)
        line = ser.readline().decode("utf-8").strip()
        if line:
            process_sensor_data(line)  # Process received data
    except Exception as e:
        print("Error:", e)
