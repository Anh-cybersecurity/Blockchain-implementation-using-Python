import shelve
from typing import List, Iterator

from .block import Block
from .utilities import encode_hex

DB_FILE = 'db_blockchain'
LAST_HASH_KEY = 'lh'

class Blockchain:
    def __init__(self):
        """
        Khởi tạo Blockchain.
        """
        self.db = shelve.open(DB_FILE, writeback=True)
        
        if LAST_HASH_KEY not in self.db:
            print("No existing blockchain found. Creating Genesis Block...")
            genesis = Block.genesis()
            self.db[encode_hex(genesis.hash)] = genesis
            self.db[LAST_HASH_KEY] = genesis.hash
            self.tip = genesis.hash
        else:
            self.tip = self.db[LAST_HASH_KEY]
            print(f"Resuming blockchain from: {encode_hex(self.tip)}")

    def add_block(self, transactions: List[str]):
        """
        Đào block mới và thêm vào chuỗi.
        """
        last_hash = self.tip
        last_block = self.db[encode_hex(last_hash)]
        new_height = last_block.height + 1
        
        new_block = Block.create_block(transactions, last_hash, new_height)
        
        self.db[encode_hex(new_block.hash)] = new_block
        self.db[LAST_HASH_KEY] = new_block.hash
        self.tip = new_block.hash
        
        return new_block

    def get_all_blocks(self) -> Iterator[Block]:
        """
        Lặp qua toàn bộ blockchain từ MỚI NHẤT -> CŨ NHẤT.
        """
        current_hash = self.tip
        
        while True:
            block_hex = encode_hex(current_hash)
            block = self.db.get(block_hex)
            
            if block:
                yield block
                current_hash = block.prev_hash
                
                if current_hash == b'\x00' * 32:
                    break
            else:
                break
    
    def close(self):
        self.db.close()