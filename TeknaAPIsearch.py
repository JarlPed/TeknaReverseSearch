# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 09:29:51 2022

@author: jarl.robert.pedersen
"""

import requests
from getChromeCookies import getChromeCookieHeader

Cookie = getChromeCookieHeader('www.tekna.no')

def searchTeknaMember(FirstName, LastName):
    r=requests.post(
        'https://www.tekna.no/api/searchuser',
        headers={
            'Cookie' : Cookie ,
            },
        data={
            "FirstName": FirstName,
            "LastName": LastName,
            "Workplace": "",
            "Institution": "",
           "ExamYear": "",
           "IsExamYearPlusMinus": False,
           "TeknaDepartmentId": "",
           "Age": "",
           "JobTitle": "",
           "Place": "",
           "CurrentPaging": 0,
           "MaxPage": 500,
           "TotalMembers": 0,
           "OrderBy": 0,
           "UserSearchScope": 0
           },
        )
    
    if (r.status_code != 200):
        raise Exception('Bad responce')
    
    return r.json()['Users']