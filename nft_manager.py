import hashlib
import json
from datetime import datetime


class NFT:
    def __init__(self, nft_id, name, description, creator, owner_did):
        self.nft_id = nft_id
        self.name = name
        self.description = description
        self.creator = creator
        self.owner_did = owner_did
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "nft_id": self.nft_id,
            "name": self.name,
            "description": self.description,
            "creator": self.creator,
            "owner_did": self.owner_did,
            "created_at": self.created_at
        }


class DigitalAssetManager:

    def __init__(self):
        self.assets = {}
        self.transactions = []

    # -------------------------------
    # Create / Mint NFT
    # -------------------------------
    def mint_nft(self, admin_did, name, description, owner_did):

        if not admin_did.startswith("did:"):
            print("❌ Unauthorized: Invalid administrator DID.")
            return None

        nft_id = "NFT-" + hashlib.sha256(
            f"{name}{datetime.now()}".encode()
        ).hexdigest()[:12]

        nft = NFT(
            nft_id,
            name,
            description,
            admin_did,
            owner_did
        )

        self.assets[nft_id] = nft

        self.record_transaction(
            "NFT_MINTED",
            admin_did,
            {
                "nft_id": nft_id,
                "name": name,
                "owner": owner_did
            }
        )

        print(f"✅ NFT successfully created: {nft_id}")
        return nft_id

    # -------------------------------
    # Assign NFT
    # -------------------------------
    def assign_asset(self, admin_did, nft_id, new_owner_did):

        if not admin_did.startswith("did:"):
            print("❌ Unauthorized administrator.")
            return False

        if nft_id not in self.assets:
            print("❌ NFT not found.")
            return False

        nft = self.assets[nft_id]

        old_owner = nft.owner_did
        nft.owner_did = new_owner_did

        self.record_transaction(
            "ASSET_ASSIGNED",
            admin_did,
            {
                "nft_id": nft_id,
                "old_owner": old_owner,
                "new_owner": new_owner_did
            }
        )

        print("✅ NFT assigned successfully.")
        return True

    # -------------------------------
    # Transfer Ownership
    # -------------------------------
    def transfer_asset(self, current_owner_did, nft_id, new_owner_did):

        if nft_id not in self.assets:
            print("❌ NFT not found.")
            return False

        nft = self.assets[nft_id]

        if nft.owner_did != current_owner_did:
            print("❌ Transfer denied: You are not the owner.")
            return False

        old_owner = nft.owner_did
        nft.owner_did = new_owner_did

        self.record_transaction(
            "OWNERSHIP_TRANSFER",
            current_owner_did,
            {
                "nft_id": nft_id,
                "old_owner": old_owner,
                "new_owner": new_owner_did
            }
        )

        print("✅ Ownership transferred successfully.")
        return True

    # -------------------------------
    # Verify Ownership
    # -------------------------------
    def verify_ownership(self, nft_id, user_did):

        if nft_id not in self.assets:
            print("❌ NFT not found.")
            return False

        nft = self.assets[nft_id]

        if nft.owner_did == user_did:
            print("✅ Ownership verified.")
            return True

        print("❌ Ownership verification failed.")
        return False

    # -------------------------------
    # Get NFT Details
    # -------------------------------
    def get_asset(self, nft_id):

        if nft_id not in self.assets:
            print("❌ NFT not found.")
            return None

        return self.assets[nft_id].to_dict()

    # -------------------------------
    # Record Blockchain Transaction
    # -------------------------------
    def record_transaction(self, transaction_type, actor, data):

        transaction = {
            "transaction_id": hashlib.sha256(
                f"{transaction_type}{datetime.now()}".encode()
            ).hexdigest()[:16],

            "type": transaction_type,
            "actor": actor,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }

        transaction_string = json.dumps(
            transaction,
            sort_keys=True
        )

        transaction["hash"] = hashlib.sha256(
            transaction_string.encode()
        ).hexdigest()

        self.transactions.append(transaction)

    # -------------------------------
    # Display Audit Trail
    # -------------------------------
    def show_transactions(self):

        print("\n========== AUDIT TRAIL ==========")

        for transaction in self.transactions:

            print("\nTransaction ID:",
                  transaction["transaction_id"])

            print("Type:",
                  transaction["type"])

            print("Actor:",
                  transaction["actor"])

            print("Data:",
                  transaction["data"])

            print("Timestamp:",
                  transaction["timestamp"])

            print("Hash:",
                  transaction["hash"])


# =========================================================
# DEMONSTRATION
# =========================================================

if __name__ == "__main__":

    manager = DigitalAssetManager()

    # Example DIDs
    admin = "did:example:admin123"
    user1 = "did:example:user001"
    user2 = "did:example:user002"

    print("\n===== NFT DIGITAL ASSET MANAGEMENT =====")

    # 1. Admin creates an NFT
    nft_id = manager.mint_nft(
        admin,
        "College Certificate",
        "Digital academic certificate",
        user1
    )

    # 2. Display NFT details
    print("\nNFT DETAILS:")
    print(json.dumps(
        manager.get_asset(nft_id),
        indent=4
    ))

    # 3. Verify ownership
    print("\nVERIFYING OWNERSHIP:")
    manager.verify_ownership(nft_id, user1)

    # 4. Transfer NFT
    print("\nTRANSFERRING NFT:")
    manager.transfer_asset(
        user1,
        nft_id,
        user2
    )

    # 5. Verify new ownership
    print("\nVERIFYING NEW OWNER:")
    manager.verify_ownership(
        nft_id,
        user2
    )

    # 6. Display updated NFT
    print("\nUPDATED NFT:")
    print(json.dumps(
        manager.get_asset(nft_id),
        indent=4
    ))

    # 7. Display blockchain audit trail
    manager.show_transactions()