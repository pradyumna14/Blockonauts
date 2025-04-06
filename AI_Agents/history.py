from web3 import Web3
import json

ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

contract_address = "0x0105e5AFC10A97994aF941BaAC20A4373b4e951A"

contract_abi = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "doctor", "type": "address"},
            {"indexed": False, "internalType": "string", "name": "proof", "type": "string"},
            {"indexed": False, "internalType": "string", "name": "patientName", "type": "string"},
            {"indexed": False, "internalType": "string", "name": "medicine", "type": "string"},
            {"indexed": False, "internalType": "string", "name": "dosage", "type": "string"},
            {"indexed": False, "internalType": "uint256", "name": "tablets", "type": "uint256"},
            {"indexed": False, "internalType": "string", "name": "expiryDate", "type": "string"}
        ],
        "name": "PrescriptionStored",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "string", "name": "proof", "type": "string"}
        ],
        "name": "PrescriptionDispensed",
        "type": "event"
    }
]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def search_prescriptions_by_name(target_name):
    latest_block = w3.eth.block_number
    print(f"Scanning up to block: {latest_block}...\n")
    found = False

    for block_num in range(0, latest_block + 1):
        block = w3.eth.get_block(block_num, full_transactions=True)
        for tx in block.transactions:
            try:
                receipt = w3.eth.get_transaction_receipt(tx.hash)
                logs = contract.events.PrescriptionStored().process_receipt(receipt)
                for event in logs:
                    args = event['args']
                    if target_name.lower() in args['patientName'].lower():
                        found = True
                        print(f"Transaction Hash: {tx.hash.hex()}")
                        print(f"Doctor: {args['doctor']}")
                        print(f"Proof: {args['proof']}")
                        print(f"Patient Name: {args['patientName']}")
                        print(f"Medicine: {args['medicine']}")
                        print(f"Dosage: {args['dosage']}")
                        print(f"Tablets: {args['tablets']}")
                        print(f"Expiry Date: {args['expiryDate']}")
                        print("-" * 50)
            except Exception:
                continue

    if not found:
        print("No records found for this name.")

if __name__ == "__main__":
    name = input("Enter patient's name to search: ").strip()
    search_prescriptions_by_name(name)
