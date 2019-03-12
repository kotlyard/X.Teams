import hashlib
import binascii


def GetHashOfTwo(a, b):
	h = hashlib.sha256(a + b).digest()
	return (h)

def CalcMerkleRoot(hashList):
	if len(hashList) == 1:
		return binascii.hexlify(hashList[0]).decode()
	newHashList = []
	for i in range(0, len(hashList) - 1, 2):
		newHashList.append(GetHashOfTwo(hashList[i], hashList[i + 1]))
	if len(hashList) % 2 == 1:
		newHashList.append(GetHashOfTwo(hashList[-1], hashList[-1]))
	return CalcMerkleRoot(newHashList)