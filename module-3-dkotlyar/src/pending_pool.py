from tx_validator import TxValidator
import serializer


def AddTxToFile(dec_tx):
	try:
		with open("mempool", 'a') as pool:
			pool.write(str(dec_tx)[2:-1] + '\n')
	except IOError:
		print ("Could not write to a mempool")
		

def GetThreeTxFromFile(order):
	try:
		with open("mempool", 'r') as pool:
			file = pool.readlines()
			pool.close()
		if (len(file) < 3):
			print("Not enough txs in the pool")
			return(None)
	except IOError:
		print ("Could not read mempool")
		exit(1)
	ret = file[:3] if order == "first" else file[-3:]
	new_file = file[3:] if order == "first" else  file[:-3]
	try:
		with open("mempool", 'w') as pool:
			pool.writelines(new_file)
	except IOError:
		print ("Could not read mempool")
	return (ret)

if __name__ == '__main__':
	# AddTxToFile("278b1g3qittr4qDYXHCxnrqZmQ95n6BqoT4VHB1ByhcUsBJqfP3NA1opo2T4hYdoRa3smD8u04e043098d80d1cbe40f46e093fe95584a65a3c33f562b116e6c34a679857681be0ec21a83d515d0e46d6051d7a1bc1391bb22a7fb843564dc7d0993e3baf6ade3f7910a7055fec54f792d596bebc94d1bafe6f6dd131aef2e7196325372ae359134bbc532c674be0d604cacc51b92b6239598f042e3b2e631a1cd1a3dbee37785")
	print(GetThreeTxFromFile("first"))