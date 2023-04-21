from Cryptodome.Cipher import AES
import argparse
import os.path

parser = argparse.ArgumentParser(description='Encrypt the file using AES algorithm.')

parser.add_argument("-f", '--filename', metavar='filename', type=str, required=True,
                    help='the name of the file to encrypt')

parser.add_argument('-k', '--key', metavar='key', type=str, required=True,
                    help='the key for encrypt')

group = parser.add_mutually_exclusive_group(required = True)
group.add_argument('-e', action='store_true', help='encrypt the file')
group.add_argument('-d', action='store_true', help='decrypt the file')

args = parser.parse_args()

# check if args.filename exists
if not os.path.isfile(args.filename):
    print(f"{args.filename} does not exist or is not a file")
    exit(1)
if len(args.key) < 8:
    print(f"the length of key should be at least larger then 8 bytes")
    exit(1)



AES_BLOCK_SIZE = AES.block_size
AES_KEY_SIZE = 16
key = args.key


# 待加密文本补齐到 block size 的整数倍
def PadTest(bytes):
    while len(bytes) % AES_BLOCK_SIZE != 0:
        bytes += ' '.encode()                   # 通过补空格（不影响源文件的可读）来补齐
    return bytes


# 待加密的密钥补齐到对应的位数
def PadKey(key):
    if len(key) > AES_KEY_SIZE:
        return key[:AES_KEY_SIZE]
    while len(key) % AES_KEY_SIZE != 0:
        key += '&'.encode()                     # 补齐的字符可用任意字符代替
    return key


# AES 加密
def EnCrypt(key, bytes):
    myCipher = AES.new(key, AES.MODE_ECB)
    encryptData = myCipher.encrypt(bytes)
    return encryptData

# AES 解密
def DeCrypt(key, encryptData):
    myCipher = AES.new(key, AES.MODE_ECB)
    bytes = myCipher.decrypt(encryptData)
    return bytes

def rename_file(file_path):
    """
    Rename the file at the given file path by appending a number to the file name
    if the file already exists.

    Returns the new file path.
    """
    # Split the file path into its directory and filename components
    dir_path, base_name = os.path.split(file_path)
    name, ext = os.path.splitext(base_name)

    new_path = file_path
    if os.path.exists(file_path):
        index = 1
        while True:
            new_name = f"{name}_{index}{ext}"
            new_path = os.path.join(dir_path, new_name)
            if not os.path.exists(new_path):
                break
            index += 1
    return new_path


def encrypt_OFB(key, input_file, output_file):
    with open(input_file, 'rb') as fin, open(output_file, 'ab') as fout:
        iv = os.urandom(AES.block_size)
        cipher = AES.new(key, AES.MODE_OFB, iv=iv)
        fout.write(iv)
        while True:
            chunk = fin.read(1024)
            if len(chunk) == 0:
                break
            fout.write(cipher.encrypt(chunk))

def decrypt_OFB(key, input_file, output_file):
    with open(input_file, 'rb') as fin, open(output_file, 'ab') as fout:
        iv = fin.read(AES.block_size)
        cipher = AES.new(key, AES.MODE_OFB, iv=iv)
        while True:
            chunk = fin.read(1024)
            decrypted_chunk = cipher.decrypt(chunk)
            fout.write(decrypted_chunk)
            if len(chunk) < 1024:
                break


if __name__ == '__main__':
    key = PadKey(key.encode())

    if args.e:
        output_file = args.filename + '.ens'
        encrypt_OFB(key, args.filename, output_file)

    if args.d:
        output_file = rename_file(args.filename[:-4])
        decrypt_OFB(key, args.filename, output_file)