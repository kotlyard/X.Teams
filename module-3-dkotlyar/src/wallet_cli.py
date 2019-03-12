import wallet
import transaction as tx
import tx_validator as validator
import cmd
from serializer import Serializer as txSer
from serializer import Deserializer as txDeSer
import blockchain
import block
import new_tx
from utxo_pool import utxo, findUtxoByScript
import pickle
import requests



PRIVATE_KEY = ""
PENDING_TXS = []

# for x in range(10):
#     prev_hash = PITCOIN.chain[x].hash
#     PITCOIN.chain.append(block.InitNewBlock(prev_hash))

def DoImportCmd(file):
    line = file.readline()
    global PRIVATE_KEY 
    PRIVATE_KEY = wallet.WifToPrivateKey(line)
    if line == 0:
        return (0)
    try:
        with open("address", 'w') as new_file:
            add = str(wallet.GetNewPublicAdress(PRIVATE_KEY))[2:-1]
            new_file.write(add)
        print("Public address was saved in file 'address'\n", add)  
    except IOError:
        print ("Could not write to a file")

def DoSendCmd(recipient, amount, fd):
    if (len(recipient) <= 25 or len(recipient) >= 36):
        print("Invalid recepient address format, aborting...")
        return (1)
    if (int(amount) not in range (0, 9999999999999)):
        print("Invalid amount")
        return (1)
    sender = fd.readline()
    newtx = tx.Transaction(sender, recipient, int(amount))
    global PRIVATE_KEY
    if PRIVATE_KEY == "":
        PRIVATE_KEY = input("Enter your private key in WIF format:\n")
    utxo = findUtxoByScript(sender, amount)
    if (utxo == 0):
        return 0
    # utxo = requests.get('https://testnet.blockchain.info/unspent?active=%s' % sender)
    serialized_tx = new_tx.make_raw_transaction(newtx, utxo)
    # print("serialized tx =\033[1;32;40m\t", serialized_tx, "\033[0m")
    print(newtx)
    print()
    print()
    print()
    print(serialized)
    return (serialized_tx)

class Cli(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "฿ "
        self.intro  = "Welcome\nType 'help' for help"
        self.doc_header ="Available commands (to read manual of certain command 'help cmd_name')"


    def do_new(self, args):
        """new - create new private key and public address and display on the screen"""
        global PRIVATE_KEY
        PRIVATE_KEY = wallet.GenerateNewPrivateKey()
        print("Your private_key\t\033[1;32;40m ", PRIVATE_KEY)
        print("\033[0;37;40mYour public_address\t\033[1;33;40m ", str(wallet.GetNewPublicAdress(PRIVATE_KEY))[2:-1])
        try:
            with open("address", 'w') as new_file:
                new_file.write(str(wallet.GetNewPublicAdress(PRIVATE_KEY))[2:-1])
                print("\033[0mPublic address is saved in file 'address'")
        except IOError:
            print ("Could not write to a file")
        if input("\033[1;37;40mDo you want to save your private key in WIF format in a file?(type 'yes' if so)\n \033[0m") == 'yes':
            try:
                with open("wif_key", 'w') as f:
                    f.write(str(wallet.privateKeyToWif(PRIVATE_KEY))[2:-1])
                    print("WIF private key saved in file 'wif_key'")
            except IOError:
                print ("Could not write WIF to a file")


    def do_import(self, args):
        """import  [file] - create new public address and save it in file "address" from private key in WIF format from file [file]. """
        if (len(args.split(' ')) == 1 and args == ""):
            print("Only 1 file is accepted")
        else:
            try:
                with open(args, 'r') as f:
                    DoImportCmd(f)
                f.close()
            except IOError:
                print ("Can not read file:", repr(args))

    def do_send(self, args):
        """send <% Recipient Address%>, <% Amount%> - create new transaction . """
        global PENDING_TXS
        if (len(args.split(' ')) != 2 or args == ""):
            print("Only 2 files is accepted")
        else:
            try:
                with open("address", 'r') as f:
                    PENDING_TXS.append(DoSendCmd(args.split(' ')[0], args.split(' ')[1], f))
            except IOError:
                print("Can not read file 'address'")                    


    def do_balance(self, arg):
        """balance [uncompressed public address] - prints a balance of given address"""
        global PITCOIN
        if (arg == "" or len(arg.split(' ')) != 1):
            print("Enter 1 address")
        else:
            PITCOIN.GetBalance(arg)


    def do_broadcast(self, args):
        if not PENDING_TXS:
            print("No pending tx")
        else:
            for element in PENDING_TXS:
                if (args == "-t"):
                    check = blockcypher.pushtx(tx_hex = element, coin_symbol='btc-testnet', api_key = "6f7e01bc443c48b985918a96cbc3b85b")  
                    print(check)
                else:
                    print(requests.post('http://127.0.0.1:5000/transaction/new', data=element).text)
            PENDING_TXS.clear()



    def do_delete_pool(self, args):
        print(requests.delete("http://127.0.0.1:5000/transaction/new").text)

    def do_exit(self, line):
    	"""exit"""
    	print ("Exiting...")
    	exit(0)


    def default(self, line):
        print ("There is no such command")


if __name__ == "__main__":
    cli = Cli()
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        print ("Exiting...")

# 18qyDKMafHJgekA1RGmJxxdXtAh5LV1fKL
# 1QLNV7gbABGs7rNoJhKEGzJY5GK5nEQxca