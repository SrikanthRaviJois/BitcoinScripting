from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# Connect to the Bitcoin Core RPC server
rpc_user = "Nkp"
rpc_password = "Nkpp"
rpc_host = "127.0.0.1"
rpc_port = "18443"
rpc_url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}"

try:
    rpc_connection = AuthServiceProxy(rpc_url, timeout=120)
    
    # Load the wallet
    try:
        # List available wallets
        available_wallets = rpc_connection.listwallets()
        print("Available wallets:", available_wallets)
        
        # Try to load wallet (replace 'wallet.dat' with your wallet name if different)
        wallet_name = "TestWallet3"
        if wallet_name not in available_wallets:
            try:
                rpc_connection.loadwallet(wallet_name)
                print(f"Successfully loaded wallet: {wallet_name}")
            except JSONRPCException as e:
                if "Wallet already loaded" in str(e):
                    print(f"Wallet {wallet_name} is already loaded")
                else:
                    print(f"Error loading wallet: {str(e)}")
        else:
            print(f"Wallet {wallet_name} is already loaded")
            
    except JSONRPCException as e:
        print(f"Wallet operation error: {str(e)}")

    print(f"Connected successfully! Block count: {rpc_connection.getblockcount()}")

    # Generate 3 segwit Addresses
    segwit_address_A = rpc_connection.getnewaddress("", "legacy")
    segwit_address_B = rpc_connection.getnewaddress("", "legacy")
    segwit_address_C = rpc_connection.getnewaddress("", "legacy")

    print("segwit Address A:", segwit_address_A)
    print("segwit Address B:", segwit_address_B)
    print("segwit Address C:", segwit_address_C)

    # Function to send Bitcoin using sendtoaddress
    def send_bitcoin(address, amount, comment="", comment_to=""):
        try:
            txid = rpc_connection.sendtoaddress(address, amount, comment, comment_to)
            print(f"Sent {amount} BTC to {address}. TXID: {txid}")
            return txid
        except JSONRPCException as e:
            print(f"RPC Error: {str(e)}")
            return None

    # Fund Address A with 10 BTC
    mining_address = rpc_connection.getnewaddress()
    rpc_connection.generatetoaddress(1, mining_address)  # Mine 1 block for funds

    txid_A = send_bitcoin(segwit_address_A, 10.0, "Funding Address A", "For testing")

    # Mine another block to confirm the funding transaction
    rpc_connection.generatetoaddress(1, mining_address)

    # Get UTXO for Address A
    utxos_A = rpc_connection.listunspent(1, 9999999, [segwit_address_A])

    if not utxos_A:
        raise ValueError("No UTXO available for Address A")

    input_utxo_A = utxos_A[0]
    txid_A = input_utxo_A["txid"]
    vout_A = input_utxo_A["vout"]
    amount_A = float(input_utxo_A["amount"])

    # Create raw transaction: A → B
    raw_tx_AB = rpc_connection.createrawtransaction(
        [{"txid": txid_A, "vout": vout_A}],
        {segwit_address_B: amount_A - 0.0001}  # Subtracting small fee
    )

    # Sign and Broadcast
    signed_tx_AB = rpc_connection.signrawtransactionwithwallet(raw_tx_AB)
    txid_AB = rpc_connection.sendrawtransaction(signed_tx_AB["hex"])
    print(f"Transaction A → B sent. TXID: {txid_AB}")

    # Mine another block to confirm A → B transaction
    rpc_connection.generatetoaddress(1, mining_address)

    # Get UTXO for Address B
    utxos_B = rpc_connection.listunspent(1, 9999999, [segwit_address_B])

    if not utxos_B:
        raise ValueError("No UTXO available for Address B")

    input_utxo_B = utxos_B[0]
    txid_B = input_utxo_B["txid"]
    vout_B = input_utxo_B["vout"]
    amount_B = float(input_utxo_B["amount"])

    # Create raw transaction: B → C
    raw_tx_BC = rpc_connection.createrawtransaction(
        [{"txid": txid_B, "vout": vout_B}],
        {segwit_address_C: amount_B - 0.0001}  # Subtracting small fee
    )

    # Sign and Broadcast
    signed_tx_BC = rpc_connection.signrawtransactionwithwallet(raw_tx_BC)
    txid_BC = rpc_connection.sendrawtransaction(signed_tx_BC["hex"])
    print(f"Transaction B → C sent. TXID: {txid_BC}")

    # Mine another block to confirm B → C transaction
    rpc_connection.generatetoaddress(1, mining_address)

    # Decode and analyze transaction scripts
    decoded_tx_AB = rpc_connection.decoderawtransaction(signed_tx_AB["hex"])
    decoded_tx_BC = rpc_connection.decoderawtransaction(signed_tx_BC["hex"])

    print("Decoded Transaction A → B:", decoded_tx_AB)
    print("Decoded Transaction B → C:", decoded_tx_BC)

except Exception as e:
    print(f"Unexpected error: {str(e)}")