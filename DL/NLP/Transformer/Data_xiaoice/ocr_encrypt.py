import os

from pyDes import des, CBC, PAD_PKCS5
from tqdm import tqdm


def encrypt_file(key, tgt_txt):
    with open(tgt_txt, 'rb') as f:
        lines = f.read()
    des_obj = des(key, CBC, key, pad=None, padmode=PAD_PKCS5)
    lines_bytes = des_obj.encrypt(lines, padmode=PAD_PKCS5)
    with open(tgt_txt.replace('.txt', '.xmas'), 'wb') as f:
        f.write(lines_bytes)


def decrypt_file(key, tgt_txt):
    with open(tgt_txt, 'rb') as f:
        lines_bytes = f.read()
    des_obj = des(key, CBC, key, pad=None, padmode=PAD_PKCS5)
    lines = des_obj.decrypt(lines_bytes, padmode=PAD_PKCS5)
    with open(tgt_txt.replace('.xmas', '.txt'), 'wb') as f:
        f.write(lines)


def conversion(dec=True, enc=False):
    # hint: What happened on December 24th, 2029?
    encrypt_key = input('input encryption key string:')
    files = os.listdir('texts')
    for file in tqdm(files):
        if file.endswith('.txt') and enc:
            encrypt_file(encrypt_key, os.path.join('texts', file))
        if file.endswith('.xmas') and dec:
            decrypt_file(encrypt_key, os.path.join('texts', file))


if __name__ == '__main__':
    conversion()
