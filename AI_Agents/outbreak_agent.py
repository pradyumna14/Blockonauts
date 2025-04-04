from web3 import Web3
from collections import Counter
import openai  
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    print("ERROR: OpenAI API key not found. Check your .env file!")
    exit()

openai.api_key = openai_api_key
print("Loaded Successfully")


GANACHE_URL = "http://127.0.0.1:7545" 
web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# Check blockchain connection
if web3.is_connected():
    print("Connected to Ganache Blockchain")
else:
    print("Failed to connect to Ganache")
    exit()


CONTRACT_ADDRESS = "0x0105e5AFC10A97994aF941BaAC20A4373b4e951A"
ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "doctor", "type": "address"},
            {"indexed": False, "name": "proof", "type": "string"},
            {"indexed": False, "name": "patientName", "type": "string"},
            {"indexed": False, "name": "medicine", "type": "string"},
            {"indexed": False, "name": "dosage", "type": "string"},
            {"indexed": False, "name": "tablets", "type": "uint256"},
            {"indexed": False, "name": "expiryDate", "type": "string"}
        ],
        "name": "PrescriptionStored",
        "type": "event"
    }
]


contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

medicine_counter = Counter()

latest_block = web3.eth.block_number
print(f"Scanning blocks up to {latest_block}")

for block_number in range(max(0, latest_block - 50), latest_block + 1):
    block = web3.eth.get_block(block_number, full_transactions=True)

    for tx in block.transactions:
        try:
            receipt = web3.eth.get_transaction_receipt(tx.hash)
            for log in receipt.logs:
                if log.address.lower() == CONTRACT_ADDRESS.lower():
                    decoded_event = contract.events.PrescriptionStored().process_log(log)
                    
                    medicine_name = decoded_event["args"]["medicine"]
                    medicine_counter[medicine_name] += 1
                    print(f"🔍 Found: {medicine_name}")
        
        except Exception as e:
            print(f"Skipping transaction {tx.hash.hex()} - {str(e)}")

def analyze_prescription_trends(medicine_data, threshold=3):
    """
    Analyzes prescription trends, detects spikes in demand, and generates an organized report.

    Args:
    - medicine_data (Counter): Counter object with medicine counts.
    - threshold (int): The minimum count to trigger an alert for unusual demand.

    Returns:
    - str: A formatted AI analysis report.
    - list: A list of flagged medicines for potential outbreak detection.
    """
    most_used_meds = medicine_data.most_common(5)
    outbreak_alerts = [med for med, count in medicine_data.items() if count >= threshold and med in ["Paracetamol", "PainKiller", "Antibiotic", "Antiviral"]]

    report = f"""
    📊 **AI Analysis: Prescription Trends** 📊

    🔹 **Top Prescribed Medicines**: {', '.join(med for med, _ in most_used_meds) if most_used_meds else 'None'}
    🔹 **Moderate Usage Medicines**: {', '.join(med for med, count in medicine_data.items() if 2 <= count < threshold) if medicine_data else 'None'}
    🔹 **Low Usage Medicines**: {', '.join(med for med, count in medicine_data.items() if count == 1) if medicine_data else 'None'}

    🔍 **Outbreak Detection Alerts**:
    {f"⚠️ Sudden spike detected for: {', '.join(outbreak_alerts)}. Health authorities have been notified." if outbreak_alerts else "✅ No unusual spikes detected."}

    """

    return report.strip(), outbreak_alerts

summary_prompt = f"Analyze the following medicine usage data and summarize key trends:\n{medicine_counter.most_common(5)}"

try:
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are an AI analyzing prescription trends."},
                  {"role": "user", "content": summary_prompt}]
    )

    ai_summary = response["choices"][0]["message"]["content"]
    print("\n📊 AI Analysis Summary:")
    print(ai_summary)

except Exception as e:
    print(f"❌ ERROR: API call failed - {e}")

report, alerts = analyze_prescription_trends(medicine_counter)
print("\n📊 AI Analysis:")
print(report)

if alerts:
    print("\n🚨 ALERT: Outbreak detected! Notifying blockchain network...")
