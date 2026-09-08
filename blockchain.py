import hashlib
import json
from datetime import datetime


class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = datetime.now().isoformat()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash
        }

        block_string = json.dumps(block_data, sort_keys=True)

        return hashlib.sha256(
            block_string.encode()
        ).hexdigest()


class Blockchain:

    def __init__(self):
        self.chain = []

        # Create the first block
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(
            0,
            [],
            "0"
        )

        self.chain.append(genesis_block)

    def add_block(self, transactions):

        previous_block = self.chain[-1]

        new_block = Block(
            len(self.chain),
            transactions,
            previous_block.hash
        )

        self.chain.append(new_block)

        print(f"✅ Block {new_block.index} added successfully.")

    def display_chain(self):

        print("\n========== BLOCKCHAIN ==========")

        for block in self.chain:

            print("\nBlock:", block.index)
            print("Timestamp:", block.timestamp)
            print("Previous Hash:", block.previous_hash)
            print("Hash:", block.hash)
            print("Transactions:")

            print(
                json.dumps(
                    block.transactions,
                    indent=4
                )
            )

    def verify_chain(self):

        for i in range(1, len(self.chain)):

            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check current block hash
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check connection with previous block
            if current_block.previous_hash != previous_block.hash:
                return False

        return True


# ==========================================
# DEMONSTRATION
# ==========================================

if __name__ == "__main__":

    blockchain = Blockchain()

    # Example NFT transaction
    transaction1 = {
        "type": "NFT_MINTED",
        "nft_id": "NFT-001",
        "owner": "did:example:user001",
        "asset": "College Certificate"
    }

    blockchain.add_block([transaction1])

    # Example ownership transfer
    transaction2 = {
        "type": "OWNERSHIP_TRANSFER",
        "nft_id": "NFT-001",
        "old_owner": "did:example:user001",
        "new_owner": "did:example:user002"
    }

    blockchain.add_block([transaction2])

    # Display blockchain
    blockchain.display_chain()

    # Verify blockchain
    print("\n========== BLOCKCHAIN VERIFICATION ==========")

    if blockchain.verify_chain():
        print("✅ Blockchain is valid.")
    else:
        print("❌ Blockchain has been tampered with.")