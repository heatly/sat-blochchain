const xrpl = require("xrpl");

// ✅ Connect to XRPL Testnet
const client = new xrpl.Client("wss://s.altnet.rippletest.net:51233");

async function main() {
    await client.connect();

    // ✅ Load Wallet from Seed
    const wallet = xrpl.Wallet.fromSeed("sEdVogi23VrsderDEYPABrzdsVhbu49");
    console.log(`🔹 Wallet Address: ${wallet.classicAddress}`);

    // ✅ Get Account Balance
    const account_info = await client.request({
        command: "account_info",
        account: wallet.classicAddress,
        ledger_index: "validated"
    });

    const balance = account_info.result.account_data.Balance / 1_000_000;
    console.log(`💰 Balance: ${balance} XRP`);

    // ✅ Ensure Destination is Different from Sender
    const destination_address = "rB1zaF9yPMP2eF7BzWjoXPtVmX7s8eQd1d"; // Change to a valid recipient

    if (wallet.classicAddress === destination_address) {
        console.error("❌ Error: Sender and destination cannot be the same!");
        return;
    }

    // ✅ Prepare Payment Transaction
    const payment_tx = {
        TransactionType: "Payment",
        Account: wallet.classicAddress,
        Amount: xrpl.xrpToDrops("1"), // Convert 1 XRP to drops
        Destination: destination_address
    };

    // ✅ Autofill, Sign, and Submit Transaction
    const prepared_tx = await client.autofill(payment_tx);
    const signed_tx = wallet.sign(prepared_tx);
    const result = await client.submitAndWait(signed_tx.tx_blob);

    console.log("✅ Transaction Submitted:", result);
    
    // ✅ Close Connection
    await client.disconnect();
}

// Run the function
main().catch(console.error);
