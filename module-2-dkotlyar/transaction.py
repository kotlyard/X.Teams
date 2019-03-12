import wallet
import tx_validator as validator
from serializer import Serializer as txSer
from serializer import Deserializer as txDeSer
import struct
import codecs
import base58
import script

def swap32(i):
    return struct.unpack("<I", struct.pack(">I", i))[0]


class Transaction:
	""" Tranaction Class """
	def __init__(self, version = 0x000001, input_count = 1, inputs = [], output_count = 1, outputs = [], locktime = "0000000000"):
		self.version = str(swap32(version))
		self.input_count = input_count
		self.inputs = self.initInputs("486c887f2378feb1ea3cdc054cb7b6722e632ab1edac962a00723ea0240f2e9c", 0, )
		self.output_count = output_count
		self.outputs = self.initOutputs()
		self.locktime = locktime


	def getRawTx(self):
		line = self.version + str(self.input_count)
		res = ""
		for element in self.inputs:
			res += str(element["prev_txid"] + str(swap32(element["tx_out_index"]))) + str(element["scriptLen"] + str(element["scriptSig"]) + elem["sequence"])
		line += res
		res = ""
		line += str(self.output_count)
		for element in self.outputs:
			res += str(self.outputs["prev_txid"])
		return (line + res + self.locktime)


	def initInputs(self, prev_txid, tx_out_index, scriptLen = 0, seq = "ffffffff", sig, pubkey):
		d_input = {}
		d_input["prev_txid"] = prev_txid #hash of the transaction containing desired UTXO
		d_input["tx_out_index"] = tx_out_index #index of the output of the ^
		d_input["scriptSig"] = hex(len(str(sig)) / 2) + str(sig) + "01" + hex(len(str(pubkey)) / 2) + str(pubkey) 
		d_input["scriptLen"] = len(d_input["scriptSig"]) / 2
		d_input["sequence"] = seq
		self.inputs.append(d_input)


	def	initOutputs(self, pubkey):
		d_output = {}
		d_output["value"] = str(swap32(value))
		d_output["pubkeyScript"] = str(swap32(value))
		d_input["pubkeyScript"] =  "76aa" + binascii.hexlify(script.hash160(pubkey)) + "88ac"
		d_output["scriptLen"] = len(d_input["pubkeyScript"]) / 2
		self.outputs.append(d_output)


	def CalcHash(self):
		conc = self.sender + self.recipient + hex(self.amount).split('x')[-1]
		self.tx_hash = wallet.hashlib.sha256(conc.encode('utf-8')).hexdigest()
		self.tx_hash = wallet.hashlib.sha256(self.tx_hash).hexdigest()



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

def swapBytes(data):
	return(codecs.encode(codecs.decode(data, 'hex')[::-1], 'hex').decode())

if __name__ == "__main__":
	tx = Transaction()
	print(tx.getRawTx())

# wif 5Kd2jYDcmGLxoyqsgm1U4rDqpBb4vhrfqKJNnDGYFK3XTMwiNLF

# public address 1Hm2wLv6ZNwPsnvW1XRVzqqrBX9AvpHANT  18o7Ub3Gv84ptck1cars1MkMdo4BCLazpo

# privatekey edd5872ff2afa2af8f5cb95532cf632c1b6a136023e9e41140cbc5b7281a412e
