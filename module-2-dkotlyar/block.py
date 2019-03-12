import time
import json
import pending_pool as pool
import merkle
import hashlib
import binascii
import transaction as tx
from tinydb import TinyDB, Query
from serializer import Serializer as ser
from serializer import Deserializer as deser
import tx_validator as validator




def jsonDefault(OrderedDict):
	return OrderedDict.__dict__

class Block:
	"""docstring for Block"""

	def __init__(self, prev_hash = 0):
		self.timestamp = time.time()
		self.nonce = 0
		self.height = 0
		self.prev_hash = prev_hash;
		if (prev_hash == 0):
			try:
				with open("address", 'r') as f:
					self.txs = tx.CoinBaseTransaction(f.readline())
			except IOError:
				print ("Could not read sender address in a file 'address'")


	def __repr__(self): 
		return json.dumps(self, default=jsonDefault, indent=4)


	def GetHash(self):
		con = str(self.timestamp) + str(self.nonce) + str(self.txs) + str(self.prev_hash) + str(self.merkle_root)
		self.hash = hashlib.sha256(con.encode('utf-8')).hexdigest()

	def MineBlock(self, comp):
		self.GetHash()
		while ('0' * comp != self.hash[:comp]):
			self.nonce += 1
			self.GetHash()

	def GetMerkleRoot(self):
		hashlist = []
		if (type(self.txs) is tx.CoinBaseTransaction):
			self.txs.CalcHash()
			self.txs.SignTx(self.txs.tx_hash)
			new = ser.serialize(self.txs)
			hashlist.append(hashlib.sha256(new.encode('utf-8')).hexdigest().encode('utf-8'))
		else:
			for element in self.txs:
				element.CalcHash()
				hashlist.append(hashlib.sha256(element.tx_hash.encode('utf-8')).hexdigest().encode('utf-8'))
		self.merkle_root = merkle.CalcMerkleRoot(hashlist)


	def PrintBlockInfo(self):
		print('{')
		print('\ttimestamp :\t\t', self.timestamp, "\n\tnonce :\t\t\t", self.nonce)
		print("\tBlock hash :\t\t", self.hash)
		print("\tPrevious block hash :\t", self.prev_hash)
		print("\tSearialized Transactions:\t")
		if (type(self.txs) is tx.CoinBaseTransaction):
			print('\t\t' + ser.serialize(self.txs))
		else:
			for elem in self.txs:
				print('\t\t' + elem)
		print("\tMerkle root hash :\t", self.merkle_root)
		print('}')


def InitNewBlock(prev_hash, comp = 2):
	block = Block(prev_hash)
	dec_txs = []
	try:
		with open("address", 'r') as add:
			coinbase = tx.CoinBaseTransaction(add.readline())
			coinbase.CalcHash()
			coinbase.SignTx(coinbase.tx_hash)
	except IOError:
		print ("Could not read 'address' file")
		return (0)
	dec_txs.append(coinbase)
	fresh_txs = pool.GetThreeTxFromFile("last")
	if (fresh_txs == None):
		return (None)
	for element in fresh_txs:
		dec_txs.append(deser.deserialize(element))
		validator.TxValidator(dec_txs[-1])
	block.txs = dec_txs
	block.GetMerkleRoot()
	block.MineBlock(comp)
	return(block)

if __name__ == '__main__':
	block = InitNewBlock("1234")
	print(block)




