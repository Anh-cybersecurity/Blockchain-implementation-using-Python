import sys
from .utilities import int_to_bytes, sha256_digest, encode_hex
# Trong Rust code của bạn DIFFICULTY = 12. Ta giữ nguyên mức này để test cho nhanh.
# Nếu muốn khó như Bitcoin thật thì phải tăng lên 20-30.
DIFFICULTY = 12

class ProofOfWork:
    def __init__(self, block):
        self.block = block
        # Target: Giống hệt Rust: 1 << (256 - DIFFICULTY)
        # Nghĩa là: Số 1 dịch trái (256 - 12) bit.
        # Bất kỳ hash nào (dạng số) nhỏ hơn số Target này đều hợp lệ.
        self.target = 1 << (256 - DIFFICULTY)

    def init_data(self, nonce: int) -> bytes:
        """
        Gom tất cả dữ liệu của Block + Nonce lại thành một cục bytes để chuẩn bị Hash.
        Tương đương hàm init_data trong Rust.
        """
        # 1. Lấy prev_hash
        data = self.block.prev_hash
        
        # 2. Lấy dữ liệu Transaction 
        # (Sau này ta sẽ nâng cấp thành Merkle Root giống Rust, giờ tạm thời nối chuỗi cho đơn giản)
        tx_data = "".join(self.block.transactions).encode()
        data += sha256_digest(tx_data)
        
        # 3. Thêm Nonce, Timestamp, Difficulty, Height
        data += int_to_bytes(nonce)
        data += int_to_bytes(DIFFICULTY)
        data += int_to_bytes(self.block.timestamp)
        data += int_to_bytes(self.block.height)
        
        return data

    def run(self):
        """
        Vòng lặp đào coin.
        Tương đương hàm run() trong Rust.
        """
        nonce = 0
        print(f"\n--- Bắt đầu đào Block Height {self.block.height} ---")
        
        while True:
            # 1. Chuẩn bị dữ liệu với nonce hiện tại
            data = self.init_data(nonce)
            
            # 2. Hash SHA-256
            hash_bytes = sha256_digest(data)
            
            # 3. Chuyển bytes thành số nguyên lớn (Big Integer) để so sánh toán học
            hash_int = int.from_bytes(hash_bytes, 'big')

            # 4. Kiểm tra điều kiện PoW: Hash phải nhỏ hơn Target
            if hash_int < self.target:
                print(f"\n Tìm thấy Nonce: {nonce}")
                print(f"Hash: {encode_hex(hash_bytes)}")
                return nonce, hash_bytes
            else:
                nonce += 1
                # Hiệu ứng in đè dòng cũ để nhìn cho chuyên nghiệp (giống \r trong Rust)
                if nonce % 100000 == 0:
                    sys.stdout.write(f"\r Mining... Nonce: {nonce}")
                    sys.stdout.flush()

    def validate(self) -> bool:
        """
        Kiểm tra lại block có hợp lệ không (Dành cho các Node khác verify)
        """
        data = self.init_data(self.block.nonce)
        hash_bytes = sha256_digest(data)
        hash_int = int.from_bytes(hash_bytes, 'big')
        return hash_int < self.target