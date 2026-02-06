import sys
from Blockchain import Blockchain, encode_hex

def main():
    print("Initializing Bitcoin Core...")
    bc = Blockchain()

    while True:
        print("\n=== PYTHON BITCOIN CORE CLI ===")
        print("1. Add new Transaction (Mine Block)")
        print("2. Print Chain")
        print("3. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            tx_data = input("Enter transaction data (e.g., 'Alice send 10 BTC'): ")
            if tx_data:
                print("\nMining new block...")
                block = bc.add_block([tx_data]) 
                print(f"\nBlock Mined! Hash: {encode_hex(block.hash)}")
        
        elif choice == '2':
            print("\n--- BLOCKCHAIN HISTORY ---")
            for block in bc.get_all_blocks():
                print(f"Height: {block.height}")
                print(f"Hash  : {encode_hex(block.hash)}")
                print(f"Prev  : {encode_hex(block.prev_hash)}")
                print(f"Tx    : {block.transactions}")
                print(f"Nonce : {block.nonce}")
                print("-" * 40)
        
        elif choice == '3':
            print("Stopping node...")
            bc.close()
            sys.exit(0)
            
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()