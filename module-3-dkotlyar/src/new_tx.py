import hashlib
import wallet
import binascii
import base58
import ecdsa
import codecs
import struct
import transaction
from enum import Enum
from ecdsa.util import string_to_number, number_to_string
from ecdsa.curves import SECP256k1



# my_private_key_testnet1 = "beeb439ea4a4c2ab6a112120c071ae6ebbbff8c1d2edb7888c34e827150825c6"
# my_wif = "5KGNMKUr6S2QtGbrmqkKfL6nAz5SMiCabiTTz8hzukkHuzfoCNe"
# unc_pub_key = "0475fdcc66c12bedc970fb2ee37ca53e6ac61a70ef4db3b066d2f4b19248926aeb3215a792af509bc2e13e80882b83e020e825467e0a1c357b05c2751c858dbee5"
# comp_pub_key = "0375fdcc66c12bedc970fb2ee37ca53e6ac61a70ef4db3b066d2f4b19248926aeb"
# my_pub_address_testnet1 = "n2uGFGU798XqMEbzaP9g8TfgotvypyLYQa"


# my_private_key_testnet2 = "54f35298ac3af4ef4b01f6025705fe0f407cda32275b20d8902c3986ec4f8751"
# my_pub_address_testnet2 = "mzE5nzmdsgBCpFwRdesqJn6AerrDHuh2Vj"
# wif2 = "5JThXYhdNPHN13RdmNaV37StsxAeDc8bkc39X4ArrPLUsRH5FXj"


CURVE_ORDER = SECP256k1.order
fee = 10000

def ripemd160(x):
    d = hashlib.new('ripemd160')
    d.update(x)
    return d


class raw_tx:
    version = struct.pack("<L", 1)
    tx_in_count = struct.pack("<B", 1)
    tx_in = {}  # TEMP
    tx_out_count = struct.pack("<B", 1)
    tx_out1 = {}  # TEMP
    return_out = {}  # TEMP
    lock_time = struct.pack("<L", 0)



def make_raw_Coinbase(tx):
    rtx = raw_tx()

    priv = wallet.GetPrivateKeyFromFile("miner_key")
    my_hashed_pubkey = base58.b58decode_check(tx.sender)[1:].hex()

    my_private_key = base58.b58decode_check(priv)[1:33].hex()

    recipient_hashed_pubkey = base58.b58decode_check(tx.recipient)[1:].hex()

    # form tx_in
    rtx.tx_in["txouthash"] = bytes.fromhex(34 * '0')
    rtx.tx_in["tx_out_index"] = struct.pack("<L", 0)
    rtx.tx_in["script"] = bytes.fromhex("03" + 30 * "f")
    rtx.tx_in["script_bytes"] = struct.pack("<B", len(rtx.tx_in["script"]))
    rtx.tx_in["sequence"] = bytes.fromhex("ffffffff")

    # form tx_out
    rtx.tx_out1["value"] = struct.pack("<Q", tx.amount)
    rtx.tx_out1["pk_script"] = bytes.fromhex("76a914%s88ac" % recipient_hashed_pubkey)
    rtx.tx_out1["pk_script_bytes"] = struct.pack("<B", len(rtx.tx_out1["pk_script"]))
    
    # form raw_tx
    raw_tx_string = (
            rtx.version
            + rtx.tx_in_count
            + rtx.tx_in["txouthash"]
            + rtx.tx_in["tx_out_index"]
            + rtx.tx_in["script_bytes"]
            + rtx.tx_in["script"]
            + rtx.tx_in["sequence"]
            + rtx.tx_out_count
            + rtx.tx_out1["value"]
            + rtx.tx_out1["pk_script_bytes"]
            + rtx.tx_out1["pk_script"]           
    )

    raw_tx_string += rtx.lock_time + struct.pack("<L", 1)

    hashed_tx_to_sign = hashlib.sha256(hashlib.sha256(raw_tx_string).digest()).digest()
    pk_bytes = bytes.fromhex(my_private_key)
    sk = ecdsa.SigningKey.from_string(pk_bytes, curve=ecdsa.SECP256k1)

    vk = sk.verifying_key
    # can be used for uncompressed pubkey
    vk_string = vk.to_string()
    public_key_bytes = b'\04' + vk_string

    signature = sk.sign_digest(hashed_tx_to_sign, sigencode=ecdsa.util.sigencode_der_canonize)

    sigscript = (
            signature
            + b'\01'
            + struct.pack("<B", len(public_key_bytes))
            + public_key_bytes
    )


    real_tx = (
            rtx.version
            + rtx.tx_in_count
            + rtx.tx_in["txouthash"]
            + rtx.tx_in["tx_out_index"]
            + struct.pack("<B", len(sigscript) + 1)
            + struct.pack("<B", len(signature) + 1)
            + sigscript
            + rtx.tx_in["sequence"]
            + rtx.tx_out_count
            + rtx.tx_out1["value"]
            + rtx.tx_out1["pk_script_bytes"]
            + rtx.tx_out1["pk_script"]
    )        
    real_tx += rtx.lock_time

    tx.serialized = real_tx
    tx.version = 1
    tx.number_of_inputs = rtx.tx_in_count

    tx.inputs = transaction.Input(rtx.tx_in["txouthash"], rtx.tx_in["tx_out_index"], sigscript, rtx.tx_in["sequence"])
    tx.outputs.append(transaction.Output(rtx.tx_out1["value"], rtx.tx_out1["pk_script"]))
    tx.CalcHash()
    print(tx.tx_hash)
    exit()
    return(real_tx.hex())



def make_raw_transaction(tx, utxo, priv = 0):
    rtx = raw_tx()

    if (priv == 0):
        priv = wallet.GetPrivateKeyFromFile("wif_key")

    my_hashed_pubkey = base58.b58decode_check(tx.sender)[1:].hex()

    # kek = ripemd160(hashlib.sha256(binascii.unhexlify(wallet.PrivateKeyToPublicKey("54f35298ac3af4ef4b01f6025705fe0f407cda32275b20d8902c3986ec4f8751"))).digest()).digest()    
    my_private_key = base58.b58decode_check(priv)[1:33].hex()
    sender_compressed_pub = wallet.get_compressed_key(wallet.PrivateKeyToPublicKey(my_private_key))
    # sender_compressed_pub_bytes = bytes.fromhex(sender_compressed_pub)

    recipient_hashed_pubkey = base58.b58decode_check(tx.recipient)[1:].hex()

    # form tx_in
    rtx.tx_in["txouthash"] = bytes.fromhex(utxo.tx_hash)
    rtx.tx_in["tx_out_index"] = struct.pack("<L", utxo.tx_output_n)
    rtx.tx_in["script"] = bytes.fromhex(utxo.script)
    rtx.tx_in["script_bytes"] = struct.pack("<B", len(rtx.tx_in["script"]))
    rtx.tx_in["sequence"] = bytes.fromhex("ffffffff")

    # form tx_out
    rtx.tx_out1["value"] = struct.pack("<Q", tx.amount)
    rtx.tx_out1["pk_script"] = bytes.fromhex("76a914%s88ac" % recipient_hashed_pubkey)
    rtx.tx_out1["pk_script_bytes"] = struct.pack("<B", len(rtx.tx_out1["pk_script"]))

    return_value = utxo.value - tx.amount - fee
    if return_value > 0:
        rtx.tx_out_count = struct.pack("<B", 2)
        rtx.return_out["value"] = struct.pack("<Q", return_value)
        rtx.return_out["pk_script"] = bytes.fromhex("76a914%s88ac" % my_hashed_pubkey)
        rtx.return_out["pk_script_bytes"] = struct.pack("<B", len(rtx.return_out["pk_script"]))
    # =========================================
    
    # form raw_tx
    raw_tx_string = (
            rtx.version
            + rtx.tx_in_count
            + rtx.tx_in["txouthash"]
            + rtx.tx_in["tx_out_index"]
            + rtx.tx_in["script_bytes"]
            + rtx.tx_in["script"]
            + rtx.tx_in["sequence"]
            + rtx.tx_out_count
            + rtx.tx_out1["value"]
            + rtx.tx_out1["pk_script_bytes"]
            + rtx.tx_out1["pk_script"]           
    )

    if return_value > 0:
        raw_tx_string += (
        rtx.return_out["value"]
        + rtx.return_out["pk_script_bytes"]
        + rtx.return_out["pk_script"]
    )
    raw_tx_string += rtx.lock_time + struct.pack("<L", 1)

    hashed_tx_to_sign = hashlib.sha256(hashlib.sha256(raw_tx_string).digest()).digest()
    pk_bytes = bytes.fromhex(my_private_key)
    sk = ecdsa.SigningKey.from_string(pk_bytes, curve=ecdsa.SECP256k1)

    vk = sk.verifying_key
    # can be used for uncompressed pubkey
    vk_string = vk.to_string()
    public_key_bytes = b'\04' + vk_string

    signature = sk.sign_digest(hashed_tx_to_sign, sigencode=ecdsa.util.sigencode_der_canonize)

    sigscript = (
            signature
            + b'\01'
            + struct.pack("<B", len(public_key_bytes))
            + public_key_bytes
    )


    real_tx = (
            rtx.version
            + rtx.tx_in_count
            + rtx.tx_in["txouthash"]
            + rtx.tx_in["tx_out_index"]
            + struct.pack("<B", len(sigscript) + 1)
            + struct.pack("<B", len(signature) + 1)
            + sigscript
            + rtx.tx_in["sequence"]
            + rtx.tx_out_count
            + rtx.tx_out1["value"]
            + rtx.tx_out1["pk_script_bytes"]
            + rtx.tx_out1["pk_script"]
            
    )
    if return_value > 0:
        real_tx += (
        rtx.return_out["value"]
        + rtx.return_out["pk_script_bytes"]
        + rtx.return_out["pk_script"]
    )
    real_tx += rtx.lock_time

    tx.serialized = real_tx
    tx.version = 1

    tx.number_of_inputs = rtx.tx_in_count


    tx.inputs = transaction.Input(rtx.tx_in["txouthash"], rtx.tx_in["tx_out_index"], sigscript, rtx.tx_in["sequence"])
    tx.outputs.append(transaction.Output(rtx.tx_out1["value"], rtx.tx_out1["pk_script"]))
    if (return_value > 0):
        tx.outputs.append(transaction.Output(rtx.return_out["value"], rtx.return_out["pk_script"]))
    tx.CalcHash()
    return(real_tx.hex())


def main():
    # TX = tx.Transaction("n2uGFGU798XqMEbzaP9g8TfgotvypyLYQa", "mzE5nzmdsgBCpFwRdesqJn6AerrDHuh2Vj", 50000)
    # make_raw_transaction(TX)
    pass


if __name__ == "__main__":
    main()
