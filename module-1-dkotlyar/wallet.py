import hashlib
import base58
import binascii
import ecdsa
from ecdsa import SigningKey, SECP256k1
import codecs
import os

def GenerateNewPrivateKey():
	return binascii.hexlify(os.urandom(32)).decode()

def SafePrivateKeyToFile(key):
	file = open('../privkey', 'w')
	if file == -1:
		print("Open error with file 'privkey'")
		return("Open Error")
	else:
		file.write(key)
        
def privateKeyToWif(priv):
	priv_add_x80 = "80" + priv
	first_sha256 = hashlib.sha256(binascii.unhexlify(priv_add_x80)).hexdigest()
	second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
	result_wif = base58.b58encode(binascii.unhexlify(priv_add_x80 + second_sha256[:8]))
	return result_wif

def GetPrivateKeyFromFile(file):
	fd = open('../' + file, "r")
	if fd == -1:
		print("Open error")
		return(-1)
	return(privateKeyToWif(fd.read()))
    
def WifToPrivateKey(wif):  
	first_encode = base58.b58decode(wif)
	private_key_full = binascii.hexlify(first_encode)
	private_key = private_key_full[2:-8]
	return (private_key)

def PrivateKeyToPublicKey(priv_key):
	priv_key = codecs.decode(priv_key, 'hex')
	sk = ecdsa.SigningKey.from_string(priv_key, curve=ecdsa.SECP256k1)
	vk = sk.get_verifying_key()
	return ('04' + binascii.hexlify(vk.to_string()).decode())

def CreateMainnetKeyFromPublicKey(public_key):
    public_key_bytes = codecs.decode(public_key, 'hex')
    sha256_bpk = hashlib.sha256(public_key_bytes)
    sha256_bpk_digest = sha256_bpk.digest()
    ripemd160_bpk = hashlib.new('ripemd160')
    ripemd160_bpk.update(sha256_bpk_digest)
    ripemd160_bpk_digest = ripemd160_bpk.digest()
    ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')
    return (binascii.hexlify(codecs.decode(ripemd160_bpk_hex, 'hex')).decode())

def GetMainnetKeyChecksum(mainnet_key):
    mainnet_key = codecs.decode(mainnet_key, 'hex')
    sha256_nbpk = hashlib.sha256(mainnet_key)
    sha256_nbpk_digest = sha256_nbpk.digest()
    sha256_2_nbpk = hashlib.sha256(sha256_nbpk_digest)
    sha256_2_nbpk_digest = sha256_2_nbpk.digest()
    sha256_2_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')
    return (sha256_2_hex[:8])

def CreatePublicAddress(mainnet_key, checksum):
    return (base58.b58encode(codecs.decode(mainnet_key, 'hex') + codecs.decode(checksum, 'hex')))

def GetNewPublicAdress(priv_key):
	public_key = PrivateKeyToPublicKey(priv_key)
	main_key = "00" + CreateMainnetKeyFromPublicKey(public_key)
	checksum = GetMainnetKeyChecksum(main_key)
	return (CreatePublicAddress(main_key, checksum))

def sign(priv, msg):
	sk = SigningKey.from_string(binascii.unhexlify(priv), curve=SECP256k1)
	public_key = sk.get_verifying_key()
	sig = sk.sign(bytes(msg, 'ascii'))
	return (codecs.encode(sig, 'hex'), binascii.hexlify(public_key.to_string()).decode())

def CheckWifPrivateKey(file):
	i = 0
	for line in file:
		i += 1
	if (i != 1):
		print("Invalid WIF private key")
		return (0)
	if (line[0] != '5'):
		print("Only mainnet key is accepted")
		return (0)
	return (line)



