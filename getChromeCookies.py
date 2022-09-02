# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 09:01:53 2022

@author: jarl.robert.pedersen
"""

import os
import json
import base64
import sqlite3
from shutil import copyfile


import win32crypt

from Crypto.Cipher import AES

def getChromeCookies(host_key):

    # Load encryption key
    encrypted_key = None
    with open(os.getenv("APPDATA") + r"\..\Local\Google\Chrome\User Data\Local State", 'r') as file:
        encrypted_key = json.loads(file.read())['os_crypt']['encrypted_key']
    encrypted_key = base64.b64decode(encrypted_key)
    encrypted_key = encrypted_key[5:]
    decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]


    # Connect to the Database
    conn = sqlite3.connect(os.getenv("APPDATA") + r"\..\Local\Google\Chrome\User Data\Default\Network\Cookies")
    conn.text_factory = bytes

    cursor = conn.cursor()

    # Get the results
    Dict = {}
    cursor.execute('SELECT name, value, encrypted_value FROM cookies WHERE host_key = \"%s\"'%(host_key)  )
    for name, value, encrypted_value in cursor.fetchall():
        
        #host_key = host_key.decode('utf-8')
        name = name.decode('utf-8')
        value = value.decode('utf-8')
        
        
        # Decrypt the encrypted_value
        try:
            # Try to decrypt as AES (modern method)
            cipher = AES.new(decrypted_key, AES.MODE_GCM, nonce=encrypted_value[3:3+12])
            decrypted_value = cipher.decrypt_and_verify(encrypted_value[3+12:-16], encrypted_value[-16:])
        except:
            # If failed try with the old method
            decrypted_value = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode('utf-8') or value or 0
            
        decrypted_value = decrypted_value.decode('utf-8')
        
        Dict.update({name : decrypted_value })
        #print("%s\t%s" %(name, decrypted_value ))
    
    conn.close()
    return Dict

def getChromeCookieHeader(host_key):
    d = getChromeCookies(host_key)
    return '; '.join([ key + "=" + val  for key,val in zip(d.keys(), d.values())])
