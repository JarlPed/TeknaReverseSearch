# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 10:49:19 2022

@author: jarl.robert.pedersen
"""

from TeknaAPIsearch import searchTeknaMember
from ldapDiscoveryUsers import getLocalADUsers

from tqdm import tqdm

def writeTeknaUsersinAD():
    format_string = '{:30} {:30} {:30} {:30} {:60}'
    
    ADUsers = getLocalADUsers()
    
    MemberReg = []
    
    
    for ADuser in tqdm(ADUsers):
        fullName = ADuser['name']
        LastName = fullName.split(' ')[-1]
        FirstName = fullName.replace(LastName, '').strip()
        
        s = searchTeknaMember(FirstName, LastName)
        
        for i in s:
            
            lName = i['Name'].split(' ')[0]
            fName = i['Name'].replace(lName, '').strip()
            contains = False
            for  e in  fName.split(' ') :
                if e in FirstName:
                    contains = True
                    break
            
            if (lName == LastName and FirstName in fName and  contains ):
                MemberReg.append({'nameTekna' : i['Name'], 'nameAD' : fullName, 'workplaceTekna': i['Workplace'], \
                                  'TeknaDepartment' : i['Department'].replace('Tekna', '').replace('avdeling', '').strip() , \
                                      'ADLocation' : ADuser['location']})
            
    # print
    print('\n\n')
    print(format_string.format('Navn (AD)', 'Lokalasjon (AD)', 'Navn (Tekna)', 'Tekna Avd.' ,'Tekna Arbeidssted'))
    for member in MemberReg:
        if (member['workplaceTekna']  != None):
            print(format_string.format(member['nameAD'], member['ADLocation'], member['nameTekna'], member['TeknaDepartment'], member['workplaceTekna']  ))
        else:
            print(format_string.format(member['nameAD'], member['ADLocation'], member['nameTekna'], member['TeknaDepartment'],'<Ingen oppføring>' ))


if __name__ == '__main__':
    writeTeknaUsersinAD()