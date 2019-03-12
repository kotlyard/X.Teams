import transaction as tx




def flip_byte_order(string):
    flipped = "".join(reversed([string[i:i + 2] for i in range(0, len(string), 2)]))
    return flipped


class Serializer:
	"""docstring for Serializer"""
	def serialize(tx):
		return()


class Deserializer:
	"""docstring for Deerializer"""
	def deserialize(to_des):
		my_input = {}
		my_output = {}
		des_tx = tx.Transaction("", "", "0")
		des_tx.version = int(flip_byte_order(to_des[:8]))
		# print("version = ", des_tx.version)
		des_tx.number_of_inputs = int(to_des[8:10])
		# print("input_number =", des_tx.number_of_inputs)
		x = 0
		while x < des_tx.number_of_inputs:
			my_input["txouthash"] = to_des[10:74]
			# print("tx_hash = ", my_input["txouthash"])
			my_input["tx_out_index"] = int(flip_byte_order(to_des[74:82]), 16)
			# print("tx_out_index =", my_input["tx_out_index"])
			my_input["script_bytes"] = int(to_des[82:84], 16) * 2
			# print("script_bytes =", my_input["script_bytes"])
			my_input["scriptSig"] = to_des[84:84 + my_input["script_bytes"]]
			# print("scriptSig =", my_input["scriptSig"])
			my_input["sequence"] = flip_byte_order(to_des[84 + my_input["script_bytes"]:84 + my_input["script_bytes"] + 8])
			# print("sequence =", my_input["sequence"])
			des_tx.inputs.append(my_input)
			x += 1
		des_tx.number_of_outputs = int(to_des[84 + my_input["script_bytes"] + 8:84 + my_input["script_bytes"] + 10], 16)
		# print("output_number =", des_tx.number_of_outputs)
		x = 0
		while x < des_tx.number_of_outputs:
			my_output["value"] = int(flip_byte_order(to_des[94 + my_input["script_bytes"]:110 + my_input["script_bytes"]]), 16)
			# print("value =", my_output["value"])
			my_output["scriptPubKeySize"] = int(to_des[110 + my_input["script_bytes"]:112 + my_input["script_bytes"]], 16) * 2
			# print("scriptPubKeySize =", my_output["scriptPubKeySize"])
			my_output["scriptPubKey"] = to_des[112 + my_input["script_bytes"]:112 + my_input["script_bytes"] + my_output["scriptPubKeySize"]]
			# print("scriptPubKey =", my_output["scriptPubKey"])
			des_tx.outputs.append(my_output)
			x += 1
		des_tx.locktime = int(flip_byte_order(to_des[112 + my_input["script_bytes"] + my_output["scriptPubKeySize"]:]), 16)
		return(des_tx)
	


def main():
	TX = Deserializer.deserialize("01000000019c2e0f24a03e72002a96acedb12a632e72b6b74c05dc3ceab1fe78237f886c48010000006a47304402203da9d487be5302a6d69e02a861acff1da472885e43d7528ed9b1b537a8e2cac9022002d1bca03a1e9715a99971bafe3b1852b7a4f0168281cbd27a220380a01b3307012102c9950c622494c2e9ff5a003e33b690fe4832477d32c2d256c67eab8bf613b34effffffff02b6f50500000000001976a914bdf63990d6dc33d705b756e13dd135466c06b3b588ac845e0201000000001976a9145fb0e9755a3424efd2ba0587d20b1e98ee29814a88ac00000000")
	print(TX.version)
	print(TX.number_of_inputs)
	print(TX.inputs)
	print(TX.number_of_outputs)
	print(TX.outputs)

if __name__ == '__main__':
	main()
