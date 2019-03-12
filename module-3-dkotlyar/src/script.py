from pythonds.basic.stack import Stack
import hashlib
import binascii

OP_HASH160 = "a9"
OP_DUP = "76"
OP_EQUALVERIFY = "88"
OP_CHECKSIGVERIFY = "ad"
OP_CHECKSIG = "ac"
OP_RIPEMD160 = "a6"
OP_HASH256 = "aa"




def op_dup(stack):
	stack.push(stack.peek())
	return stack


def op_checksig(stack):
	return (stack)



def op_chacksigverify(stack):
	stack = op_verify(stack)
	stack = op_checksig(stack)
	return (stack)

def hash160(data):
	val = hashlib.sha256(data).digest()
	h = hashlib.new('ripemd160')
	h.update(val)
	return (h.digest())

def op_hash160(stack):
	val = hash160(stack.pop())
	stack.push(val)
	return (stack)





if __name__ == '__main__':
	stack = Stack()
	stack.push(b"kek")
	print(stack.size())
	stack = op_hash160(stack)
	print(stack.size())
