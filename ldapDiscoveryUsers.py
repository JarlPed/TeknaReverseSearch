# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 12:24:05 2022

https://www.accadius.com/listing-active-directory-users-using-python/

@author: jarl.robert.pedersen
"""

import sys
import subprocess
from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE
from ldap3.core.exceptions import LDAPCursorError

import os
from getpass import getpass


def getLocalADUsers():
    pipe = subprocess.Popen("echo %userdomain%",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    domain_name = pipe.stdout.read().decode().replace('\r\n', '')
    
    pipe = subprocess.Popen("wmic computersystem get domain",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    server_name = pipe.stdout.read().decode().split('\n')[1].replace('\r', '').strip()
    
    
    user_name = os.getlogin( )
    password = getpass('Enter password for %s@%s: '%(user_name, domain_name))
    
    
    
    
    server = Server(server_name, get_info=ALL)
    conn = Connection(server, user='{}\\{}'.format(domain_name, user_name), password=password, authentication=NTLM, auto_bind=True)
    conn.search('ou=country,dc={},dc=local'.format(domain_name), '(objectclass=person)', attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
    
    format_string = '{:25} {:>6} {:19} {:19} {:25} {:19} {}'
    #print(format_string.format('User', 'Logins', 'Last Login', 'Expires', 'Company', 'Location', 'Description'))
    count = 0
    
    names = []
    matchedUsers = []

    for e in conn.entries:
        try:
            desc = e.description
        except LDAPCursorError:
            desc = ""
        
        name = ''
        if e.name:
            name = str(e.name)
        logonCount = ''
        if hasattr( e, 'logonCount'):
            logonCount = str(e.logonCount)
        lastLogon = ''
        if hasattr( e, 'lastLogon'):
            lastLogon = str(e.lastLogon)
        accountExpires = ''
        if hasattr( e, 'accountExpires'):
            accountExpires = str(e.accountExpires)
        
        company = ''
        if hasattr( e, 'company'):
            company = str(e.company)
    
        location = ''
        if logonCount != '' and company != '':
            if len( e.entry_dn.split(',OU=') ) >= 5 :
                location =  e.entry_dn.split(',OU=')[2]  #+ ';' + e.entry_dn.split(',OU=')[3]
            else:
                location = e.entry_dn.split(',OU=')[2]
        if logonCount != '' and company != '' and hasattr( e, 'manager'):
            if domain_name.lower() in company.lower():
            #print(format_string.format(name, logonCount, lastLogon[:19], accountExpires[:19], company, location , desc))
            
                names.append(name)
                matchedUsers.append({'name' : name, 'location' :   location }) # company + ',' +
                count += 1
                
    return matchedUsers