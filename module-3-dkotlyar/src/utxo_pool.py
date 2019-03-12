import binascii
import base58
import pickle
import json
import os
import block
import random




class utxo:
	""""""
	def __init__(self, prev_tx_hash, tx_output_n, script, value):
		self.tx_hash = prev_tx_hash
		# self.tx_index = tx.tx_index /// to do
		self.tx_output_n = tx_output_n
		self.script = script
		self.value = value


	def __repr__(self): 
		return json.dumps(self, default=block.jsonDefault, indent=4)


def getUtxoFromFile(filename = 'utxo_pool'):
	""" Возвращает список объектов класса utxo"""
	try:
		with open(filename, 'rb') as file:
			return (pickle.load(file))
	except IOError:
		print ("Could not read %s file" % filename)
		return(0)
		
def saveUtxoToPool(utxo, filename = 'utxo_pool'):
	try:
		with open(filename, 'wb') as file:
			pickle.dump(utxo, file)
			print("%s file was updated" % filename)
	except IOError:
		print ("Could not write to '%s' file" % filename)
		return(0)


def SortUtxoPool(utxo_set):
	return (utxo_set)


def deleteUtxoByScript(utxo_set, script):
	pass
	
def deleteUtxoByHash(tx_hash, utxo_set):
	utxo_set[:] = [d for d in utxo_set if d.tx_hash != tx_hash]
	return (utxo_set)

def findUtxoByScript(sender_add, amount):
	my_hashed_pubkey = base58.b58decode_check(sender_add)[1:].hex()
	my_script = ("76a914%s88ac" % my_hashed_pubkey)
	utxo_set = getUtxoFromFile()
	for element in utxo_set:
		if element.script == my_script:
			if (int(element.value) >= int(amount)):
				return (element)
	print("No such utxo, or not enough value")
	return (0)

# def findUtxoByTxHash(tx_hash, utxo_set):
# 	for element in utxo_set:
# 		if element.tx_hash == tx_hash:
# 			return element
# 	return -1


def updateUtxoPool(tx_hash, utxo_set):
	utxo_set = deleteUtxoByHash(tx_hash, utxo_set)
	saveUtxoToPool(utxo_set)
	return (utxo_pool)

def randbits(num):
	return (binascii.hexlify(os.urandom(num)).decode())

if __name__ == '__main__':
	# utxo_set = []
	# for x in range(0, 3):
	# 	utxo_set.append(utxo(randbits(32), random.randint(0, 4), randbits(16), random.randint(0, 100000000)))


	address = "n2uGFGU798XqMEbzaP9g8TfgotvypyLYQa"
	# base = base58.b58decode_check("n2uGFGU798XqMEbzaP9g8TfgotvypyLYQa")[1:].hex()
	# script = ("76a914%s88ac" % base)
	# utxo_set.append(utxo(randbits(32), random.randint(0, 4), script, random.randint(0, 100000000)))
	# saveUtxoToPool(utxo_set)
	utxo_set = getUtxoFromFile()
	print(utxo_set)
	res = findUtxoByScript(address, 10000000)
	print(res)








