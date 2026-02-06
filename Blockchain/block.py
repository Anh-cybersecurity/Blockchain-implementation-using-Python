import time
from dataclasses import dataclass
from typing import List

from .utilities import int_to_bytes, encode_hex

@dataclass
class Block:
    timestamp: int
    transactions: List[str]
    prev_hash: bytes
    hash: bytes
    nonce: int
    height: int

    @classmethod
    def create_block(cls, transactions: List[str], prev_hash: bytes, height: int):
        timestamp = int(time.time())

        block = cls(
            timestamp=timestamp,
            transactions=transactions,
            prev_hash=prev_hash,
            hash=b'',
            nonce=0,
            height=height
        )

        from .proof import ProofOfWork
        
        pow = ProofOfWork(block)
        nonce, hash_result = pow.run()

        block.nonce = nonce
        block.hash = hash_result
        
        return block

    @classmethod
    def genesis(cls):
        return cls.create_block(
            transactions=["Genesis Transaction - Hello Python Blockchain"],
            prev_hash=b'\x00' * 32,
            height=0
        )