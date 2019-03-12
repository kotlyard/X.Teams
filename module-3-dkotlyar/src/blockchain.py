import block
import json
import serializer as ser
import tx_validator as validator
import transaction as tx
from itertools import chain
from collections import OrderedDict
import pending_pool as pool




def jsonDefault(OrderedDict):
    return OrderedDict.__dict__

def CalcBalanceFromTx(address, tx):
	if type(tx) is str:
		tx = new_tx.make_raw_transaction(tx, )
	if (tx.sender == address):
		return (-tx.amount)
	if (tx.recipient == address):	
		return (tx.amount)
	return (0)

def GetTxBalanceFromBlock(block, address):
	balance = 0
	if (type(block.txs) is tx.CoinBaseTransaction):
		if (address == block.txs.sender):
			balance -= block.txs.amount
		if (address == block.txs.recipient):
			balance += block.txs.amount
	else:
		for element in block.txs:
			balance += CalcBalanceFromTx(address, element)
	return (balance)	

class Blockchain:
	"""docstring for Blockchain"""
	def __init__(self):
		self.complexity = 2
		self.chain = []
		self.nodes = []
		self.height = 0


	def mine(self, block):
		pass

	def __repr__(self): 
		return json.dumps(self, default=jsonDefault, indent=4)
	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
	def add_record_as_data(self,_record):
		self.__dict__.update(_record.__dict__)
	def add_record_as_attr(self,_record):
		self.record = _record


	def AddNewBlock(self, block):
		self.height += 1
		block.height = self.height
		self.chain.append(block)

	def resolve_conflicts():
		pass

	def is_valid_chain(self):
		for element in self.chain:
			if (self.chain.index(element) % 2 == 0):
				prev_hash = element.hash
				if (prev_hash != element.hash):
					print("Invalid chain(block hashes)")
					return (False)
		print("Chain is valid")	
		return (True)

	def add_node(self, new_node):
		self.nodes.append(new_node)

	def genesis_block(self):
		self.height = 0
		genesis = block.Block()
		print(genesis.txs)
		exit()
		genesis.GetMerkleRoot()
		genesis.MineBlock(self.complexity)
		self.chain.clear()
		self.chain.append(genesis)

	def submit_tx():
		pass

	def GetBalance(self, address): #old
		balance = 0
		for x in self.chain:
			balance += GetTxBalanceFromBlock(x, address)
		return (balance)



def PrintBlockChain(blockchain):
	for element in blockchain.chain:
		i = 0
		print("Nubmer of block is", i)
		i += 1
		element.PrintBlockInfo()


if __name__ == '__main__':
	blockchain = Blockchain()
	blockchain.genesis_block()
	# print(blockchain.chain)
	blc = Blockchain()
	blc.genesis_block()	
	blc.chain.append(block.InitNewBlock(0))
	blc.chain.append(block.InitNewBlock(blc.chain[-1].hash))
	blc.chain.append(block.InitNewBlock(blc.chain[-1].hash))
	print(blc.toJSON())
