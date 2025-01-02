import threading
import time
import random
import ast

class BankAccount:
    print("inside bank account")
    def __init__(self, bank, ifsc, account_no, balance):
        self.balance = balance
        self.bank = bank
        self.ifsc = ifsc
        self.account_no = account_no
        self.lock = threading.Lock()  # Ensures concurrency control (locking)

    def debit(self, amount):
        with self.lock:  # Lock ensures no other operations occur during this debit
            if self.balance >= amount:
                self.balance -= amount
                print(f"Debited {amount}, New balance: {self.balance}")
                return True
            else:
                print("Insufficient funds!")
                return False

    def credit(self, amount):
        with self.lock:
            self.balance += amount
            print(f"Credited {amount}, New balance: {self.balance}")

def transfer_money(sender, receiver, amount):
    try:
        # Step 1: Debit the sender's account
        if sender.debit(amount):
            print("Sender debited successfully, now attempting to credit the receiver.")
            # Simulating a potential network delay or failure here
            if random.choice([True, False]):
                raise Exception("Network failure during transfer!")

            # Step 2: Credit the receiver's account
            receiver.credit(amount)
            print(f"Transfer of {amount} from sender to receiver was successful.")
        else:
            print("Transfer failed: Sender balance is insufficient.")
    except Exception as e:
        print(f"Transfer failed: {e}")
        # Rollback the debit in case of failure (compensating transaction)
        print("Rolling back debit...")
        return False
    return True

# Function to collect a list of dictionaries as input
def collect_bank_details():
    # Prompt the user to enter a list of dictionaries as a string ,need to pass atleast two account details
    user_input = input("Enter a list of dictionaries (e.g., [{'bank':'sbi', 'ifsc':'SBIN0000','account_no':11212932,'balance':2000}, {'bank':'union', 'ifsc':'UNIN0000','account_no':1125467,'balance':4000}]): ")
    
    try:
        # Convert the string input into a list of dictionaries
        bank_details = ast.literal_eval(user_input)
        
        # Check if the input is a valid list of dictionaries
        if isinstance(bank_details, list) and all(isinstance(i, dict) for i in bank_details):
            print("Valid input. Collected bank details:")
            return bank_details
        else:
            print("Invalid format. Please make sure you enter a list of dictionaries.")
            return []
    except (ValueError, SyntaxError):
        print("Invalid input. Please enter a properly formatted list of dictionaries.")
        return []

# Collect bank details
bank_details = collect_bank_details()

# Display the collected bank details
if bank_details:
    for detail in bank_details:
        print(detail)

def login_to_account(bank_details):
    print("please login to your account")
    insert_details={
        "bank":input('Enter bank name of sender: '),
        "ifsc":input('Enter bank ifsc in capital of sender: '),
        "account":input('Enter bank account no of sender: '),
        
    }
    for r in bank_details:
        if r.get("bank")==insert_details.get("bank") and r.get("ifsc")==insert_details.get("ifsc") and r.get("account_no")==int(insert_details.get("account")):
            print("login success")
            return(r)
        else:
            raise Exception("incorrect account details,please recheck!")

def receiver_account(bank_details):
    print("please enter banificiary account details")
    insert_details={
        "bank":input('Enter bank name of reciever: '),
        "ifsc":input('Enter ifsc code for reciever in Capital: '),
        "account":int(input('Enter Reciever Account Number: ')),
        
    }
    
    for r in bank_details:
        if r.get("bank")==insert_details.get("bank") and r.get("ifsc")==insert_details.get("ifsc") and r.get("account_no")==insert_details.get("account"):
            print("transfer proccess started account is valid")
            amount=int(input('Enter Amount to transfer: '))
            return(r,amount)
        else:
           continue
        
sender_account=login_to_account(bank_details)
receiver_details,amount = receiver_account(bank_details)
# Simulating two accounts and a transfer
account_A = BankAccount(sender_account.get("bank"),sender_account.get("ifsc"),sender_account.get("account_no"),sender_account.get("balance"))
account_B = BankAccount(receiver_details.get("bank"),receiver_details.get("ifsc"),receiver_details.get("account_no"),receiver_details.get("balance"))
time.sleep(5)
def run_transfer():
    
    transfer_successful = transfer_money(account_A, account_B, amount)
    if not transfer_successful:
        print(f"Transfer of {amount} failed, retrying...")
        # Retry mechanism (retry logic after failure)
        time.sleep(2)
        transfer_money(account_A, account_B, amount)
    
# Running the transfer in separate threads to simulate concurrent operations
threads = []
for _ in range(1):
    # Simulating 3 transfers happening concurrently
    t = threading.Thread(target=run_transfer)
    threads.append(t)
    t.start()

for t in threads:
    t.join()