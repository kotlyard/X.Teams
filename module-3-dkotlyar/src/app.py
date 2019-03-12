# !flask/bin/python
from flask import Flask, jsonify, request
import wallet_cli
import pending_pool
import miner_cli as miner
import json


app = Flask(__name__)

@app.route('/transaction/pending')
def get_mempool():
    try:
        with open("mempool", 'r') as file:
            return (json.dumps(file.readlines()))
    except:
        return ("<h1>There is no mempool</h1>")

@app.route('/transaction/new', methods=['POST', 'DELETE'])
def post_tx():
	if request.method == 'POST':
		pending_pool.AddTxToFile(request.data)
		return ("Tranaction has been added to a  mempool")
	else:
		open('mempool', 'w').close()
		return ("Pool has been cleared")

@app.route('/nodes')
def return_nodes():
	try:
		with open("pitcoin.bc", 'rb') as file:
			PITCOIN = miner.importBlockChainFromFile(file)
			file.close()
	except IOError:
		return("<h1>There is no blockchain yet</h1>")	
	return (json.dumps(PITCOIN.nodes))

@app.route('/chain')
def return_chain():
	try:
		with open("pitcoin.bc", 'rb') as file:
			PITCOIN = miner.importBlockChainFromFile(file)
			file.close()
	except IOError:
		return("<h1>There is no blockchain yet</h1>")	
	return (PITCOIN.toJSON())

@app.route('/block/last')
def return_last_block():
	try:
		with open("pitcoin.bc", 'rb') as file:
			PITCOIN = miner.importBlockChainFromFile(file)
			file.close()
	except IOError:
		return("<h1>There is no blockchain yet</h1>")
	return (str(PITCOIN.chain[-1]))

@app.route('/block', methods=['GET'])
def return_block_by_index():
	hi = int(request.args.get('height'))
	try:
		with open("pitcoin.bc", 'rb') as file:
			PITCOIN = miner.importBlockChainFromFile(file)
			file.close()
	except IOError:
		return("<h1>There is no blockchain yet</h1>")
	if len(PITCOIN.chain) > hi:
		return (str(PITCOIN.chain[hi]))
	return("<h1>Nice try</h1>")

@app.route('/balance', methods=['GET'])
def  get_balance():
	add = request.args.get('address')
	try:
		with open("pitcoin.bc", 'rb') as file:
			PITCOIN = miner.importBlockChainFromFile(file)
			file.close()
	except IOError:
		return("<h1>There is no blockchain yet</h1>")
	return('<h1>Your balance is<font color="red"> ' + str(PITCOIN.GetBalance(add)) + ' </font>pitcoins</h1>' + '\nAnd you are the God'if add == '0' * 34 else '')

@app.route('/chain/length')
def return_length():
	try:
		with open("pitcoin.bc", 'rb') as file:
			PITCOIN = miner.importBlockChainFromFile(file)
			file.close()
	except IOError:
		return("<h1>There is no blockchain yet</h1>")	
	return ('<h1>The length is <font color="red">' + str(PITCOIN.height) + '</font> blocks</h1>')

if __name__ == '__main__':
    app.run(debug='on')