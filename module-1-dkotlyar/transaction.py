import wallet
import tx_validator as validator
from serializer import Serializer as txSer
from serializer import Deserializer as txDeSer

	
class Transaction:
	""" Tranaction Class """
	def __init__(self, sender, recipient, amount):
		if sender == recipient:
			exit("Are you serious?You can't send coins to yourself")
		self.sender = sender
		self.recipient = recipient
		self.amount = amount
		# self.tx_hash = ""
		# self.public_key = ""
		# self.signature = ""						


	def CalcHash(self):
		conc = self.sender + self.recipient + hex(self.amount).split('x')[-1]
		self.tx_hash = wallet.hashlib.sha256(conc.encode('utf-8')).hexdigest()


	def SignTx(self, priv_key, msg):
		signature_and_public_key =  wallet.sign(priv_key, msg)
		self.msg = msg
		self.signature = str(signature_and_public_key[0])[2:-1]
		self.public_key = '04' + signature_and_public_key[-1]


class CoinBaseTransaction(Transaction):
	""" CoinBaseTranaction Class """

	def __init__(self, recipient):
		Transaction.__init__(self, '0' * 34, recipient, 50)


	def SignTx(self, msg):
		try:
			with open("minerkey", 'r') as minerkey:
				Transaction.SignTx(self, wallet.WifToPrivateKey(minerkey.readline()), msg)
		except IOError:
			print ("Could not read 'minerkey' file")
			exit(0)


if __name__ == "__main__":
	tx1 = Transaction("1g3qittr4qDYXHCxnrqZmQ95n6BqoT4VHB", "1ByhcUsBJqfP3NA1opo2T4hYdoRa3smD8u", 10123)
	tx1.CalcHash()
	tx1.SignTx("80ce0575586694819d80d67bc7e74bd3e8de78866abf5fd4d2f3143154545cb9", tx1.tx_hash)
	# tx1.CalcHash()
	# tx1.SignTx("edd5872ff2afa2af8f5cb95532cf632c1b6a136023e9e41140cbc5b7281a412e","kek")
	# print(validator.TxValidator(tx1))
	# serialized_tx = txSer.serialize(tx1)
	# print(serialized_tx)
	# dec = txDeSer.deserialize(serialized_tx)
	# print(dec.amount == tx1.amount)
	# print(dec.sender == tx1.sender)
	# print(dec.recipient == tx1.recipient)
	# print(dec.public_key == tx1.public_key)
	# print(dec.signature == tx1.signature)


# 278b1g3qittr4qDYXHCxnrqZmQ95n6BqoT4VHB1ByhcUsBJqfP3NA1opo2T4hYdoRa3smD8u04e043098d80d1cbe40f46e093fe95584a65a3c33f562b116e6c34a679857681be0ec21a83d515d0e46d6051d7a1bc1391bb22a7fb843564dc7d0993e3baf6ade3f7910a7055fec54f792d596bebc94d1bafe6f6dd131aef2e7196325372ae359134bbc532c674be0d604cacc51b92b6239598f042e3b2e631a1cd1a3dbee37785

# wif 5Kd2jYDcmGLxoyqsgm1U4rDqpBb4vhrfqKJNnDGYFK3XTMwiNLF

# public address 1Hm2wLv6ZNwPsnvW1XRVzqqrBX9AvpHANT  18o7Ub3Gv84ptck1cars1MkMdo4BCLazpo

# privatekey edd5872ff2afa2af8f5cb95532cf632c1b6a136023e9e41140cbc5b7281a412e
