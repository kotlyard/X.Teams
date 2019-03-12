import wallet
import ecdsa
import transaction as tx
import codecs


def VerifySignature(msg, signature, public_key):
	vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1)
	return (vk.verify(bytes.fromhex(signature), bytes(msg, 'ascii')))


def TxValidator(transaction):
	if (len(transaction.sender) not in range(24, 37) or len(transaction.recipient) not in range(24, 37)):
		print("Invalid sender/recipient address")
		return (False)
	if (hasattr(transaction, 'msg') and VerifySignature(transaction.msg, transaction.signature, transaction.public_key[2:]) == False):
		print("Invalid signature")
		return (False)
	if (transaction is tx.Transaction):
		main_key = "00" + wallet.CreateMainnetKeyFromPublicKey(transaction.public_key)
		checksum = wallet.GetMainnetKeyChecksum(main_key)
		add = wallet.CreatePublicAddress(main_key, checksum)
		if (transaction.sender != str(add)[2:-1]):
			print("The sender's public address doesn't belong to the public key")
			return (False)
	return (True)
