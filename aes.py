from typing import List, Union, Tuple, Any, Generator
from itertools import chain


SBox = [
    [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
    [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
    [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
    [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
    [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
    [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
    [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
    [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
    [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
    [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
    [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
    [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
    [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
    [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
    [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
    [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
]

SBoxInv = [
    [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],
    [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],
    [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],
    [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],
    [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],
    [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],
    [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],
    [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],
    [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],
    [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],
    [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],
    [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],
    [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],
    [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],
    [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],
    [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d],
]


R_Con = (
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20,
    0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8,
    0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc,
    0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4,
    0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91,
)

def swap_byte(byte: int, box: List[List[bytes]]) -> bytes:
    byte = hex(byte)[2:]
    if len(byte) == 1:
        byte = '0' + byte
    row, col = list(byte)
    return box[int(row, 16)][int(col, 16)]


def sub_bytes(state, box):
    newStateArray = []
    for row in state:
        new_row = []
        for item in row:
            new_row.append(swap_byte(item, box))
        newStateArray.append(new_row)
    return newStateArray

def shift_rows(state: List[List[bytes]], invert: bool = False) -> List[List[bytes]]:
    if(invert):
        state[0][1], state[1][1], state[2][1], state[3][1] = state[3][1], state[0][1], state[1][1], state[2][1]
        state[0][2], state[1][2], state[2][2], state[3][2] = state[2][2], state[3][2], state[0][2], state[1][2]
        state[0][3], state[1][3], state[2][3], state[3][3] = state[1][3], state[2][3], state[3][3], state[0][3]
    else:
        state[0][1], state[1][1], state[2][1], state[3][1] = state[1][1], state[2][1], state[3][1], state[0][1]
        state[0][2], state[1][2], state[2][2], state[3][2] = state[2][2], state[3][2], state[0][2], state[1][2]
        state[0][3], state[1][3], state[2][3], state[3][3] = state[3][3], state[0][3], state[1][3], state[2][3]
    return state


# method from https://crypto.stackexchange.com/questions/14902/understanding-multiplication-in-the-aes-specification
def xtime(a): return (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

def mix_columns(state:  List[List[bytes]], invert: bool = False) -> list:
    result = []
    if(invert):
        for s in state:
            u = xtime(xtime(s[0] ^ s[2]))
            v = xtime(xtime(s[1] ^ s[3]))
            s[0] ^= u
            s[1] ^= v
            s[2] ^= u
            s[3] ^= v
    
    for col in state:
        t = col[0] ^ col[1] ^ col[2] ^ col[3]
        u = col[0]
        col[0] ^= t ^ xtime(col[0] ^ col[1])
        col[1] ^= t ^ xtime(col[1] ^ col[2])
        col[2] ^= t ^ xtime(col[2] ^ col[3])
        col[3] ^= t ^ xtime(col[3] ^ u)
        result.append(col)
    return result


def add_round_key(state: List[List[bytes]], round_key: List[Union[List[List[int]], List[list]]]) -> list:
    """
    Applies the current round key to the state matrix.
    :param state: the current state matrix
    :param round_key: the current round key
    :return: the new state after the round key has been applied
    """
    new_state = []
    for r1, r2 in zip(state, round_key):
        new_col = []
        for v1, v2 in zip(r1, r2):
            new_col.append(v1 ^ v2)
        new_state.append(new_col)
    return new_state



def cycle(state: List[List[bytes]], round_key: List[Union[List[List[int]], List[list]]], invert: bool = False) -> List[List[int]]:
    """
    Performs a complete round over a block using the provided roundkey
    :param state: the state matrix before the round transformations
    :param round_key: the round key to use for this round
    :return: state matrix after the round transformations have been applied
    """
    if(invert):
        state = shift_rows(state, invert=True)
        state = sub_bytes(state, SBoxInv)
        state = add_round_key(state, round_key)
        state = mix_columns(state, invert=True)
    else:
        state = sub_bytes(state, SBox)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_key)
    return state


def encrypt_block(data: bytes, round_keys: List[Union[List[List[int]], List[list]]], nr: int) -> bytes:
        """
        Performs encryption of a single block of the AES algorithm, unlike the encrypt method which will encrypt at
        least two blocks as it adds padding
        :param data:
        :return: encrypted block
        """
        k, m = divmod(len(data), 4)
        state = list(data[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(4))
        state = add_round_key(state, round_keys[0])

        for i in range(1, nr):
            state = cycle(state, round_keys[i])

        state = sub_bytes(state, SBox)
        state = shift_rows(state)
        state = add_round_key(state, round_keys[-1])

        state = bytes(list(chain(*state)))

        return state

def decrypt_block(data: bytes, round_keys: List[Union[List[List[int]], List[list]]], nr: int) -> bytes:
        """
        Performs decryption of a single block of the AES algorithm
        :param data:
        :return: encrypted block
        """
        k, m = divmod(len(data), 4)
        state = list(data[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(4))
        state = add_round_key(state, round_keys[-1])

        for i in range(nr - 1, 0, -1):
            state = cycle(state, round_keys[i], invert=True)

        state = shift_rows(state, invert=True)

        state = sub_bytes(state, SBoxInv)
        state = add_round_key(state, round_keys[0])

        state = bytes(list(chain(*state)))

        return state

def generate_confusion(block: List[int], rc: bytes) -> List[bytes]:
    """
    Performs the confusion step when expanding the key to roundkeys
    :param block: the block to operate on
    :param rc: the rcon value to use
    :return: the transformed block
    """
    block = [swap_byte(b, SBox) for b in block[1:] + [block[0]]]
    return [block[0] ^ rc] + block[1:]


def expand_key(key: bytes, nk: int = 4, nr: int = 10, nb: int = 4) -> List[Tuple[Any]]:
        """
        Performs operations to expand the key into the respective round keys.
        Uses class fields to determine how many keys to produce.
        :param key: the original key
        :return: list containing the expanded keys
        """
        w = []
        for i in range(nk):
            w.append([key[4 * i], key[4 * i + 1], key[4 * i + 2], key[4 * i + 3]])

        for i in range(nk, (nb * (nr + 1))):
            tmp = w[i - 1]
            if i % nk == 0:
                tmp = generate_confusion(tmp, R_Con[int(i / nk) - 1])
            elif nk > 6 and i % nk == nb:
                tmp = sub_bytes([tmp], SBox)[0]
            w.append([x ^ y for x, y in zip(w[i - nk], tmp)])
        return list(zip(*[iter(w)] * nb))

NUM_WORDS = {16: 4, 24: 6, 32: 8, 48: 12, 64: 16}

ECB = 1
CTR = 2
GCM = 3

def bytes_to_chunk(l: List[Any], n: int) -> Generator:
    for i in range(0, len(l), n):
        yield l[i:i + n]

def init(key: bytes, data: bytes, number_rounds=10, mode=ECB, counter_initial=0, counter_increment=1) -> bytes:
        
        if len(key) != 16:
            raise ValueError("Only 128 bit keys are supported!")
        
        if len(data) % 16 != 0:
            pad_len = 16 - (len(data) % 16)
            data = data + bytes([0] * pad_len)

        if mode != CTR and mode != ECB and mode != GCM:
            raise ValueError("Unsupported mode!")

        number_bytes = 4 # Fixed to 32bit
        number_keys = NUM_WORDS[len(key)]
        block_length = 16 # Fixed to 128bit
        round_keys = expand_key(key, number_keys, number_rounds, number_bytes)

        state = data
        
        blocks = list(bytes_to_chunk(list(state), block_length))
        if(mode == CTR):
            counter = counter_initial
            encrypted_blocks = []
            for block in blocks:
                next_block = bytes([x ^ counter for x in block]) # XOR with counter
                counter += counter_increment
                encrypted_blocks.append(encrypt_block(next_block, round_keys, number_rounds))
            cipher = b''.join(encrypted_blocks)
        elif(mode == ECB):
            cipher = b''.join([encrypt_block(block, round_keys, number_rounds) for block in blocks])

        blocks = list(bytes_to_chunk(list(cipher), block_length))
        if(mode == CTR):
            counter = counter_initial
            decrypted_blocks = []
            for block in blocks:
                block = decrypt_block(block, round_keys, number_rounds)
                block = bytes([x ^ counter for x in block]) # XOR with counter
                decrypted_blocks.append(block)
                counter += counter_increment

            decryted = b''.join(decrypted_blocks)
        elif(mode == ECB):
            decryted = b''.join([decrypt_block(block, round_keys, number_rounds) for block in blocks])


        return cipher, decryted


#testing code
# expected = bytes([0x29, 0xC3, 0x50, 0x5F, 0x57, 0x14, 0x20, 0xF6, 0x40, 0x22, 0x99, 0xB3, 0x1A, 0x02, 0xD7, 0x3A])
# print("expected: ", expected.decode("latin-1"))
# decoded = [b.decode("utf-8") for b in expected]
# print(decoded)
# data = bytes([0x54, 0x77, 0x6F, 0x20, 0x4F, 0x6E, 0x65, 0x20, 0x4E, 0x69, 0x6E, 0x65, 0x20, 0x54, 0x77, 0x6F])
# data = b'this is my plaintext7865263748502'
# in_file = open("foto-perfil.jpeg", "rb") # opening for [r]eading as [b]inary
# data = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
# print("data: ", data)
# print(type(data))
# in_file.close()
# print("data: ", data.decode("latin-1"))
# key = bytes([0x54, 0x68, 0x61, 0x74, 0x73, 0x20, 0x6D, 0x79, 0x20, 0x4B, 0x75, 0x6E, 0x67, 0x20, 0x46, 0x75])
# key = b'MySecretKey59283'
# print("key: ", key.decode("latin-1"))
# actual_cypher, actual_decryted = init(key, data, 13)
# plaintext = base64.b64encode(actual_cypher).decode('ASCII')
# print("actual_cypher: ", plaintext)
# out_file = open("out-file.txt", "wb") # open for [w]riting as [b]inary
# out_file.write(str.encode(plaintext))
# out_file.close()
# print("actual_cypher: ", actual_cypher)
# print("actual_decryted: ", actual_decryted)
# equals1 = actual_cypher == expected
## showing results
# plaintext1 = base64.b64encode(actual_cypher).decode('ASCII')
# plaintext2 = actual_decryted.decode("utf-8")
# print("Actual 1: " + plaintext1)
# print("Decrypt 1: " + plaintext2)


# data = bytes(bytearray.fromhex('00112233445566778899aabbccddeeff'))
# print(data)
# key = bytes(bytearray.fromhex('000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f'))
# print(key)
# expected = bytes(bytearray.fromhex('8ea2b7ca516745bfeafc49904b496089'))
# actual_cypher = init(key, data)
# equals2 = actual_cypher == expected
# ## showing results
# print("Actual 2: " + str(actual_cypher))
# print("Expected 2: " + str(expected))


# expected = b'Hello, World!123'
# print(expected)
# print(expected.decode("latin-1"))
# data = b'Hello, World!123'
# print(data.decode("latin-1"))
# key = bytes([0x54, 0x68, 0x61, 0x74, 0x73, 0x20, 0x6D, 0x79, 0x20, 0x4B, 0x75, 0x6E, 0x67, 0x20, 0x46, 0x75])
# print(key.decode("latin-1"))
# actual_cypher = init(key, data)
# equals3 = actual_cypher == expected
# ## showing results
# print(actual_cypher)
# return base64.b64encode(value).decode('ASCII')

# decoc = actual_cypher.decode('utf-16')
# print(decoc)
# print("Actual 3: " + actual_cypher.decode('cp1252'))
# print("Expected 3: " + str(expected))


# print("Equals? " + str(equals1 and equals2 and equals3))
