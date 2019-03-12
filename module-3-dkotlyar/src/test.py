import hashlib
import binascii
import base58
import ecdsa
import struct
from enum import Enum
from ecdsa.util import string_to_number, number_to_string
from ecdsa.curves import SECP256k1

CURVE_ORDER = SECP256k1.order
input_amount = 850000
output_amount = 100000
fee = 50000
sender_address = "n2uGFGU798XqMEbzaP9g8TfgotvypyLYQa"
sender_compressed_pub = "0375FDCC66C12BEDC970FB2EE37CA53E6AC61A70EF4DB3B066D2F4B19248926AEB"
# sender_pub_bytes = bytes.fromhex(sender_pub)
# sender_compressed_pub_bytes = bytes.fromhex(sender_compressed_pub)
# sender_priv = "beeb439ea4a4c2ab6a112120c071ae6ebbbff8c1d2edb7888c34e827150825c6"
sender_wif_priv = "5KGNMKUr6S2QtGbrmqkKfL6nAz5SMiCabiTTz8hzukkHuzfoCNe"
recipient_address = "mzE5nzmdsgBCpFwRdesqJn6AerrDHuh2Vj"
prev_txid = "43dcfaeb9474122663276a375cd6b14c17e23d3012c6ebce4f90c7965195a835"


def ripemd160(x):
    d = hashlib.new('ripemd160')
    d.update(x)
    return d


class Network(Enum):
    TEST_NET = 0
    PROD_NET = 1


class raw_tx:
    version = struct.pack("<L", 1)
    tx_in_count = struct.pack("<B", 1)
    tx_in = {}  # TEMP
    tx_out_count = struct.pack("<B", 1)
    tx_out1 = {}  # TEMP
    tx_out2 = {}  # TEMP
    lock_time = struct.pack("<L", 0)


def flip_byte_order(string):
    flipped = "".join(reversed([string[i:i + 2] for i in range(0, len(string), 2)]))
    return flipped


def normalize_secret_bytes(privkey_bytes: bytes) -> bytes:
    scalar = string_to_number(privkey_bytes) % CURVE_ORDER
    if scalar == 0:
        raise Exception('invalid EC private key scalar: zero')
    privkey_32bytes = number_to_string(scalar, CURVE_ORDER)
    return privkey_32bytes
    
def make_raw_transaction():
    rtx = raw_tx()

    my_address = sender_address
    my_hashed_pubkey = base58.b58decode_check(my_address)[1:].hex()

    my_private_key = sender_wif_priv
    my_private_key_hex = base58.b58decode_check(my_private_key)[1:33].hex()

    recipient = recipient_address
    recipient_hashed_pubkey = base58.b58decode_check(recipient)[1:].hex()

    my_output_tx = prev_txid
    input_value = input_amount
    # form tx_in
    rtx.tx_in["txouthash"] = bytes.fromhex(my_output_tx)
    rtx.tx_in["tx_out_index"] = struct.pack("<L", 1)
    rtx.tx_in["script"] = bytes.fromhex("76a914%s88ac" % my_hashed_pubkey)
    rtx.tx_in["scrip_bytes"] = struct.pack("<B", len(rtx.tx_in["script"]))
    rtx.tx_in["sequence"] = bytes.fromhex("ffffffff")

    # form tx_out
    rtx.tx_out1["value"] = struct.pack("<Q", output_amount)
    rtx.tx_out1["pk_script"] = bytes.fromhex("76a914%s88ac" % recipient_hashed_pubkey)
    rtx.tx_out1["pk_script_bytes"] = struct.pack("<B", len(rtx.tx_out1["pk_script"]))

    # return_value = input_value - output_amount - fee # 1000 left as fee
    # rtx.tx_out2["value"] = struct.pack("<Q", return_value)
    # rtx.tx_out2["pk_script"] = bytes.fromhex("76a914%s88ac" % my_hashed_pubkey)
    # rtx.tx_out2["pk_script_bytes"] = struct.pack("<B", len(rtx.tx_out2["pk_script"]))
    # =========================================
    # form raw_tx
    raw_tx_string = (
            rtx.version
            + rtx.tx_in_count
            + rtx.tx_in["txouthash"]
            + rtx.tx_in["tx_out_index"]
            + rtx.tx_in["scrip_bytes"]
            + rtx.tx_in["script"]
            + rtx.tx_in["sequence"]
            + rtx.tx_out_count
            + rtx.tx_out1["value"]
            + rtx.tx_out1["pk_script_bytes"]
            + rtx.tx_out1["pk_script"]
            # + rtx.tx_out2["value"]
            # + rtx.tx_out2["pk_script_bytes"]
            # + rtx.tx_out2["pk_script"]
            + rtx.lock_time
            + struct.pack("<L", 1)
    )

    hashed_tx_to_sign = hashlib.sha256(hashlib.sha256(raw_tx_string).digest()).digest()
    pk_bytes = bytes.fromhex(my_private_key_hex)
    sk = ecdsa.SigningKey.from_string(pk_bytes, curve=ecdsa.SECP256k1)
    # vk = sk.verifying_key

    # can be used for uncompressed pubkey
    # vk_string = vk.to_string()
    # public_key_bytes = b'\04' + vk_string

    public_key_bytes_hex = sender_compressed_pub

    signature = sk.sign_digest(hashed_tx_to_sign, sigencode=ecdsa.util.sigencode_der_canonize)

    sigscript = (

            signature
            + b'\01'
            + struct.pack("<B", len(bytes.fromhex(public_key_bytes_hex)))
            + bytes.fromhex(public_key_bytes_hex)

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
            # + rtx.tx_out2["value"]
            # + rtx.tx_out2["pk_script_bytes"]
            # + rtx.tx_out2["pk_script"]
            + rtx.lock_time

    )
    print("raw_tx " + '=' * 30)
    print(real_tx.hex())


def main():
    make_raw_transaction()
    pass


if __name__ == "__main__":
    main()