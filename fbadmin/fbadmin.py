# coding: utf-8
from __future__ import unicode_literals
from selenium import webdriver
from ConfigParser import SafeConfigParser
from os.path import exists
import sys
import re
import time
def get_cred(path):
    if exists(path):
        parser=SafeConfigParser()
        parser.read(path)
        em=parser.get('credentials', 'email')
        pw=parser.get('credentials', 'password')
        return em,pw
    else:
        print('config file not found')
        sys.exit(1)

def login():    
    em,pw= get_cred('credentials.cfg')
    driver = webdriver.PhantomJS()
    driver.set_window_size(1600, 900)
    driver.get('http://www.facebook.com')
    email=driver.find_element_by_id('email')
    email.send_keys(em)
    password=driver.find_element_by_id('pass')
    password.send_keys(pw)
    button=driver.find_element_by_id('loginbutton')
    button.click()
    return driver

class Applicant(object):
    def __init__(self,container):
        self.container=container
        self.name,self.age,self.othergroupstext=tuple(container.text.split('\n')[1:4])
        match=re.search(r'\d+',self.othergroupstext)
        if match:
            self.groupcount=match.group(0)
        else:
            self.groupcount=0
        self.approvebutton=container.find_element_by_link_text('Approve')
        self.blockbutton=container.find_element_by_link_text('Block')
        self.url=self.container.find_element_by_link_text(self.name).get_attributes('href')
    
    def block(self):
        self.blockbutton.click()

    def approve(self):
        self.approvebutton.click()


class FBGroup(object):
    def __init__(self,driver,groupurl):
        self.driver=driver
        self.groupurl=groupurl
        self.applicants=self.get_applicants()

    def get_applicants(self):
        self.driver.get(self.groupurl+'requests')
        blocks=self.driver.find_elements_by_link_text('Block')
        if blocks:
            containers=[block.find_element_by_xpath('../..') for block in blocks]
            applicants=[Applicant(container) for container in containers]
            return applicants
        else:
            return None


group=FBGroup(login(),'https://www.facebook.com/groups/782652721814257/')
for applicant in group.applicants:
    print applicant.name,applicant.age,applicant.groupcount
    if applicant.groupcount>50:
        applicant.block()
    elif applicant.groupcount<10:
        applicant.approve()
        time.sleep(1)
# r'\d+'