import wallet
import transaction
import tx_validator
import serializer
import binascii
import codecs
import pending_pool
import cmd
import requests
import script
import utxo_set as utxo
from hashlib import sha256
import blockcypher
import config as cnf

API_KEY = "6f7e01bc443c48b985918a96cbc3b85b"
PORT = None


class Cli(cmd.Cmd):
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = "฿ "
		self.intro  = "\t\tWelcome to the bitcoin wallet\nHow to use? 'help'!!"
		self.doc_header ="For detail information use 'help _command_')"
		self.transaction = 1
		self.swtransaction = 1
		self.private_key = '0'

	def do_new(self, args):
		"""'new' is using for generating private and 
		public keys. Bitcoin address is in the file."""
		self.private_key = output(0)
	
	def do_import(self, args):
		"""import [file...] - import private key (import in a WIF)"""
		if len(args.split(' ')) == 1:
			self.private_key = import_command(args)
		else:
			print("usage\timport /path/to/file/with/WIF/Private/Key\n")

	def do_send(self, args):
		"""send get three parameters flag: -t means create transaction for broadcating to testnet or -p means broadcas to Pitcoin
		 recipient and amount and build, sign and serialize transaction"""

		args = args.split(' ')
		i = 0
		if len(args) >= 2:
			if args[0] == '-p':
				i = 1
				self.transaction = wallet.send(args[1], int(args[2]), self.private_key, "Pitcoin", 0)
			if args[0] == '-t':
				i = 1
				self.transaction = wallet.send(args[1], int(args[2]), self.private_key, "Testnet", 0)
			if args[0] == '-swp':
				i = 1
				self.transaction = wallet.send(args[1], int(args[2]), self.private_key, "Pitcoin", 1)
			if args[0] == '-swt':
				i = 1
				self.transaction = wallet.send(args[1], int(args[2]), self.private_key, "Testnet", 1)
			
			if i == 0:
				print("Something get wrong! Use help command")
				return
			print(self.transaction)
		else:
			print("usage\n\tsend -flag address_of_recipient amount\n")

	def do_broadcast(self, args):
		""" broadcast - send POST request with serialized transaction data to
		web API of Pitcoin full node, which provide route /transaction/new.
		broadcast Testnet - send POST request with serialized transaction data to Testnet"""
		if self.transaction != 1:
			args = args.split()
			if len(args) > 0 and args[0] == "-t":
				check = blockcypher.pushtx(tx_hex = self.transaction, coin_symbol='btc-testnet', api_key = API_KEY)
			else:
				broadcast_command(self.transaction)
				# deserialized_transaction = serializer.Deserializer.deserializer(self.transaction, 0)
				self.transaction = 1
		else:
			print('Use command send before broadcast command!\n')

	def do_balance(self, args):
		""" return balance of address, transmit in parameter. Iterating for
		each blocks and each transactions and calculate balance, based on sender and
		recipient address (if its sender, there is subtraction, in otherwise its
		addition)"""
		args = args.split(' ')
		if args[0] == '-t':
			which = "Testnet"
		else:
			which = "Pitcoin"
		utxo_set = utxo.get_utxo_set(which, args[1])
		balance = utxo.check_balance(utxo_set)
		print("Your balance is\t" + '\033[1m' + str(balance) + '\033[0m')

	def do_swnew(self, args):
	# """'swnew' is using for generating address for segwit transactions. If you haven't used a command 
	# 	new or import, you would be asked to provide your private key.  Bitcoin address is saved in 
	# 	the file."""
		if self.private_key == '0':
			self.private_key = get_private_key()
		# public_key = wallet.get_public_key(self.private_key)
		# compressed_key = wallet.get_compressed_key(public_key)
		# swaddr = get_bech32(compressed_key)
		swaddr = wallet.get_swaddress(self.private_key)
		print("Your sigwit address is:\n" + swaddr + "\nYou can find it in the file swaddress")
		f = open('swaddress', 'a')
		f.write(swaddr + "\n")

	def get_data(self):
		data = {}
		data['transaction'] = self.transaction
		data['private_key'] = self.private_key

	def do_test(self, args):
		print(wallet.bech32_address_from_compressed_publkey('0279BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798'))


	def do_exit(self, args):
		"""exit"""
		print("\nBye, have a nice day!")
		exit(0)

def output(private_key):
	if private_key == 0:
		private_key = wallet.get_private_key()
	print("Your private key:\n" + private_key + "Please keep it in secret!!!")
	wif_key = wallet.convert_to_WIF(private_key)
	print("Your private key in wif format is:")
	print(wif_key)
	bitcoin_address = wallet.get_bitcoin_address(private_key)
	print("Your public address is:\n" + bitcoin_address + "\nYou can find it in the file address")
	f = open('address', 'a')
	f.write(bitcoin_address + "\n")
	return private_key

def import_command(arg):
	try:
		f = open(arg, 'r')
		private_key = wallet.WIF_to_key(f.read())
		private_key = output(private_key)
		return private_key
	except IOError:
		print("usage:\timport /path/to/file/with/WIF/Private/Key\n")
	
def get_current_private_key():
	print("Enter your private key:\t")
	private_key = input()
	if (len(private_key) != 64 and len(private_key) != 51):
		print("Invalid private key\n")
		exit(0)
	if len(private_key) != 64:
		private_key = wallet.WIF_to_key(private_key)
	return private_key


def sign_verify(private_key, message, sender, recipient, amount):
	sign_pub_key = wallet.sign(private_key, message)
	return sign_pub_key


def create_hash(sender, recipient, amount):
	message = transaction.Transaction(sender, recipient, amount)
	message = message.transaction_hash_calculate()
	return message

def broadcast_command(transaction):
	# requests.post("http://" + port + "/transaction/new", json = transaction)
	cnf.broadcast_to_friend(transaction, '/transaction/new')
	print("Successfuly broadcasted")

def main():
	PORT = cnf.getPortFromFile()
	print("Port = ", PORT)
	cli = Cli()
	try:
		cli.cmdloop()
	except KeyboardInterrupt:
		print("Bye, have a nice day!")

if __name__ == '__main__':
	main()