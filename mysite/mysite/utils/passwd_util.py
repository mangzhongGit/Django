#!/usr/bin/env python3
# !-*-coding:utf-8 -*-
import hashlib


def encryption(data):
    salt = 'dsajkgnjkasdhogoisadhgi'
    ret = hashlib.md5(salt.encode("utf-8"))
    ret.update(data.encode("utf-8"))
    result = ret.hexdigest()
    return result


def decrypt(ciphertext):
    print(ciphertext)

