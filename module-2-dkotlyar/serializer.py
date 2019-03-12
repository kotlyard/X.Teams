import transaction as tx


class Serializer:
	"""docstring for Serializer"""
	def serialize(tx):
		return(str('%04x' % tx.amount) + tx.sender + tx.recipient + tx.public_key + tx.signature)


class Deserializer:
	"""docstring for Deerializer"""
	def deserialize(to_des):
		des_tx = tx.Transaction(to_des[4:38], to_des[38:72], int(to_des[:4], 16))
		des_tx.public_key = to_des[72:202]
		des_tx.signature = to_des[202:]
		return(des_tx)
	