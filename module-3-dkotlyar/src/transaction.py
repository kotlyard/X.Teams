import wallet
import binascii
import codecs
import hashlib
import blockcypher
import new_tx
import block
import json
import serializer
import pickle
import tx_validator as validator
from serializer import Serializer as txSer
from serializer import Deserializer as txDeSer





class Input:
	def __init__(self, txouthash, tx_out_index, sigscript, sequence):
		self.txouthash = txouthash
		self.tx_out_index = tx_out_index
		self.sigscript = sigscript
		self.sequence = sequence


class Output:
	def __init__(self, value, pk_script):
		self.tx_hash = ""
		self.value = value
		self.pk_script = pk_script


class Transaction:
	""" Tranaction Class """
	serialized = ""
	def __init__(self, sender, recipient, amount):
		self.sender = sender
		self.recipient = recipient
		self.amount = amount
		#after serialize
		self.version = ""
		self.number_of_inputs = ""
		self.inputs = Input("", "", "", "")
		self.number_of_outputs = ""
		self.outputs = []

	def __repr__(self):
		return json.dumps(self, default=block.jsonDefault, indent=4)

	def CalcHash(self):
		first = hashlib.sha256(bytes(self.serialized, 'utf-8')).hexdigest()
		self.tx_hash = hashlib.sha256(bytes(first, 'utf-8')).hexdigest()



class CoinBaseTransaction(Transaction):
	""" CoinBaseTranaction Class """

	def __init__(self, recipient):
		Transaction.__init__(self, '0' * 34, recipient, 50)

	# def CalcHash(self):
	# 	first = hashlib.sha256(bytes(self.serialized, 'utf-8')).hexdigest()
	# 	self.tx_hash = hashlib.sha256(bytes(first, 'utf-8')).hexdigest()
		
def kek(tx):
	tx.version = 1

if __name__ == "__main__":
	tx1 = Transaction("mzE5nzmdsgBCpFwRdesqJn6AerrDHuh2Vj", "n2uGFGU798XqMEbzaP9g8TfgotvypyLYQa", 400000)
	print(tx1)
	kek(tx1)
	print(tx1)
	# tx_hash = "daf034a181ff6506d8575489dcd98126283910c445c727b40f90a23d3bbbc04e"
	# script_pub_key = "76a914cd3994123ab2ed6c66ab3660050098383174ffcc88ac"

	# new_utxo = utxo(tx_hash, 0, script_pub_key, 500000)

	# # new_utxos.append(utxo(tx1, 0, 1000000))
	# # saveUtxoToPool(new_utxos)
	# # kek = getUtxoFromFile("utxo_pool")
	# # needed_utxo = findUtxoByTxHash("43dcfaeb9474122663276a375cd6b14c17e23d3012c6ebce4f90c7965195a835", kek)
	# # updateUtxoPool("43dcfaeb9474122663276a375cd6b14c17e23d3012c6ebce4f90c7965195a835", kek)
	# # print(needed_utxo)
	# ser = formTransaction(tx1, new_utxo, "5JThXYhdNPHN13RdmNaV37StsxAeDc8bkc39X4ArrPLUsRH5FXj")
	# API_KEY = "6f7e01bc443c48b985918a96cbc3b85b"
	# check = blockcypher.pushtx(tx_hex = ser, coin_symbol='btc-testnet', api_key = API_KEY)	
	# le = "0100000001daf034a181ff6506d8575489dcd98126283910c445c727b40f90a23d3bbbc04e000000008a473044022022ed0fdcff2bb47659a25ae2040e2e7d33da4a95226e9fd3569f5ed3a58b8adc02204fc73af2aec32b4ffdf676428a0ca05d8a2ce395f12e219a2f1efc6e9ffbbeb4014104e224a6a395f900db26674a26e0bdf248718bbcd7d3db0b47d0cfa92d831792bf52e1cdb77f1728514e9755064741761c3fe089f08ecd90f12ce2e71feba6b5b9ffffffff02801a0600000000001976a914ea92c7355098ef1dcf33c6619ba28e6d4a6247e988ac905f0100000000001976a914cd3994123ab2ed6c66ab3660050098383174ffcc88ac00000000"
	# kek = hashlib.sha256(bytes(le, 'utf-8')).hexdigest()
	# second = hashlib.sha256(bytes(kek, 'utf-8')).hexdigest()
	# print(second)


# 278b1g3qittr4qDYXHCxnrqZmQ95n6BqoT4VHB1ByhcUsBJqfP3NA1opo2T4hYdoRa3smD8u04e043098d80d1cbe40f46e093fe95584a65a3c33f562b116e6c34a679857681be0ec21a83d515d0e46d6051d7a1bc1391bb22a7fb843564dc7d0993e3baf6ade3f7910a7055fec54f792d596bebc94d1bafe6f6dd131aef2e7196325372ae359134bbc532c674be0d604cacc51b92b6239598f042e3b2e631a1cd1a3dbee37785

# wif 5Kd2jYDcmGLxoyqsgm1U4rDqpBb4vhrfqKJNnDGYFK3XTMwiNLF

# public address 1Hm2wLv6ZNwPsnvW1XRVzqqrBX9AvpHANT  18o7Ub3Gv84ptck1cars1MkMdo4BCLazpo

# privatekey edd5872ff2afa2af8f5cb95532cf632c1b6a136023e9e41140cbc5b7281a412e
