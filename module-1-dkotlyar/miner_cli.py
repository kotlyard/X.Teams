import random
import blockchain
import wallet
import argparse
import wallet_cli
import block
import cmd
import json
import pickle
import transaction as tx
import pending_pool as pool
import serializer as ser
import pending_pool as pool
from collections import OrderedDict
from tinydb import TinyDB, Query


PITCOIN = None

class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def getKeysByValue(dictOfElements, valueToFind):
	listOfItems = dictOfElements.items()
	for item in listOfItems:
		if item[1] == valueToFind:
			return (item[0])
	return (None)

def addRandomTxsToPool(keys_adds, count = 10):
	txs = []
	ser_txs = []
	add1, add2 = 1, 1 
	for x in range(count):
		while add1 == add2:
			add1 = random.choice(list(keys_adds.values()))
			add2 = random.choice(list(keys_adds.values()))
		txs.append(tx.Transaction(add1, add2, random.randrange(1, 1000)))
		txs[x].CalcHash()
		txs[x].SignTx(getKeysByValue(keys_adds, add1), txs[x].tx_hash)
		txs[x] = ser.Serializer.serialize(txs[x])
		pool.AddTxToFile(txs[x])
		print(color.HEADER + "Tranaction was added to a pending pool" + color.ENDC)	


def premine():
	global PITCOIN
	print(color.OKGREEN + "Premine mode is active now.\nGenerating 3 private keys...")
	keys_adds = {}
	keys = []
	addresses = []
	for i in range(3):
		keys.append(str(wallet.GenerateNewPrivateKey()))
		open("key" + str(i), 'w').write(str(wallet.privateKeyToWif(keys[i]))[2:-1])
		addresses.append(str(wallet.GetNewPublicAdress(keys[i]))[2:-1])
		keys_adds[keys[i]] = addresses[i]
	open("minerkey", 'w').write(str(wallet.privateKeyToWif(keys[0]))[2:-1])
	open("address", 'w').write(addresses[0])
	print("Keys was saved in files key[0-2].\nAlso minerkey from the first key and miner address files were created." + color.BOLD)
	PITCOIN = blockchain.Blockchain()
	PITCOIN.genesis_block()
	addRandomTxsToPool(keys_adds, 30)
	for x in range(10):
		new_block = block.InitNewBlock(PITCOIN.chain[-1].hash)
		print("New block has been mined and added to a chain.\nBlock hash =", new_block.hash)
		PITCOIN.AddNewBlock(new_block)
	saveBlockchainToFile(PITCOIN)
	print(color.ENDC)



def importBlockChainFromFile(file):
	return(pickle.load(file))


def saveBlockchainToFile(bc):
	try:
		with open("pitcoin.bc", 'wb') as file:
			pickle.dump(bc, file)
			print (color.OKBLUE + "Blockchain has been saved in file 'pitcoin.bc'" + color.ENDC)  
	except IOError:
		print ("Could not write to a file 'pitcoin.bc'")
		return (1)


class Cli(cmd.Cmd):

	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = "฿ "
		self.intro  = "Welcome\nType 'help' for help"
		self.doc_header ="Available commands (to read manual of certain command 'help cmd_name')"

	def do_mine(self, args):
		""" mine - takes 3 tranactions from the pending pool, validates it and mine a block, prints its hash then adds block to chain"""
		global PITCOIN
		if (PITCOIN is None):
			inp = input("There is no chain in memory\nType 'new' if you want to create a new chain otherwise type a file name to import from\n(new/'filename')\n")
			if inp == "new":
				PITCOIN = blockchain.Blockchain()
				PITCOIN.genesis_block()
			else:
				try:
					with open(inp, 'rb') as file:
						PITCOIN = importBlockChainFromFile(file)
				except IOError:
					print ("Could not write read a file '", inp + "'")
					return (1)
		new = block.InitNewBlock(PITCOIN.chain[0].hash)
		if  new == None:
			return (None)
		PITCOIN.AddNewBlock(new)
		print("New block hash =", PITCOIN.chain[-1].hash)
		saveBlockchainToFile(PITCOIN)

	def do_add_node(self, arg):
		"""adds a node to a blockchain"""
		if (PITCOIN is None):
			inp = input("There is no chain in memory\nType 'new' if you want to create a new chain otherwise type a file name to import from\n(new/'filename')\n")
			if inp == "new":
				PITCOIN = blockchain.Blockchain()
				PITCOIN.genesis_block()
				PITCOIN.add_node(arg)
		saveBlockchainToFile(PITCOIN)


	def do_exit(self, line):
		"""exit"""
		print ("Exiting...")
		exit(0)


	def default(self, line):
		print ("There is no such command")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Miner client, you know.You can see help menu after entering miner_cli and typing "help"')
	parser.add_argument('-p', dest='feature', action='store_true', help='activates premine mode')
	options = parser.parse_args()
	if (options.feature == True):
		premine()
	cli = Cli()
	try:
		cli.cmdloop()
	except KeyboardInterrupt:
		print ("Exiting...")