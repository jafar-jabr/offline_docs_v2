#!/usr/bin/env python3

key = 'off_enc_key_777701'


def do_encrypt(msg):
    try:
        encryped = []
        for i, c in enumerate(msg):
            key_c = ord(key[i % len(key)])
            msg_c = ord(c)
            encryped.append(chr((msg_c + key_c) % 127))
        return ''.join(encryped)
    except:
        return ''


def do_decrypt(encryped):
    try:
        msg = []
        for i, c in enumerate(encryped):
            key_c = ord(key[i % len(key)])
            enc_c = ord(c)
            msg.append(chr((enc_c - key_c) % 127))
        return ''.join(msg)
    except:
        return ''


if __name__ == '__main__':
    enc = do_encrypt('123456')
    print(enc)
    denc = do_decrypt(enc)
    print(denc)
