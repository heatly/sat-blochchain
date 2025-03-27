import json
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment
from xrpl.models.requests import AccountInfo, Submit
from xrpl.ledger import get_latest_validated_ledger_sequence
from xrpl.utils import xrp_to_drops
from xrpl.transaction import sign

# ✅ Connect to XRPL Testnet
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234"
client = JsonRpcClient(JSON_RPC_URL)

# ✅ Load Wallet from Seed
wallet = Wallet.from_seed("sEdVogi23VrsderDEYPABrzdsVhbu49")
print(f"Wallet Address: {wallet.classic_address}")

# ✅ Get Account Balance
def get_balance():
    account_request = AccountInfo(account=wallet.classic_address, ledger_index="validated")
    account_response = client.request(account_request)
    
    if "account_data" in account_response.result:
        balance = int(account_response.result["account_data"]["Balance"]) / 1_000_000
        print(f"Balance: {balance} XRP")
    else:
        print("❌ Error: Could not fetch account balance.")

# ✅ Ensure Destination is Not the Same as Sender
destination_address = "rhPBDMZ3Bh5SChaM9FZ4fKgXBJzPPZSomf"  # Replace with a different valid address

if wallet.classic_address == destination_address:
    raise ValueError("❌ Error: Sender and destination cannot be the same!")

# ✅ Create and Sign Payment Transaction
def send_payment():
    latest_ledger = get_latest_validated_ledger_sequence(client)

    payment_tx = Payment(
        account=wallet.classic_address,
        destination=destination_address,
        amount=xrp_to_drops(1),  # 1 XRP converted to drops
        sequence=latest_ledger + 1
    )

    # 🔹 Sign the transaction manually
    signed_tx = sign(payment_tx, wallet)

    # 🔹 Submit the transaction
    submit_request = Submit(tx_blob=signed_tx.to_hex())
    submit_response = client.request(submit_request)

    print(f"Transaction Response: {json.dumps(submit_response.result, indent=4)}")

# ✅ Run the Functions
get_balance()   # Get account balance
send_payment()  # Send XRP payment
