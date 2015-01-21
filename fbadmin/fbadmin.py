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
        parser = SafeConfigParser()
        parser.read(path)
        em = parser.get('credentials', 'email')
        pw = parser.get('credentials', 'password')
        return em, pw
    else:
        print('config file not found')
        sys.exit(1)


def login(configfile='credentials.cfg'):
    """logs in to facebook using credentials from credentials.cfg config file by default.
    Keyword Arguments
    configfile -- path to configfile
    """
    em, pw = get_cred(configfile)
    driver = webdriver.PhantomJS(service_args=['--load-images=no'])
    driver.set_window_size(1600, 900)
    driver.get('http://www.facebook.com')
    email = driver.find_element_by_id('email')
    email.send_keys(em)
    password = driver.find_element_by_id('pass')
    password.send_keys(pw)
    button = driver.find_element_by_id('loginbutton')
    button.click()
    return driver


class Applicant(object):

    def __init__(self, name, age, othergroupstext, url):
        """ Stores details of an applicant
        Useful Attributes:
        self.name             Contains name of applicant
        self.age              Contains the 'joined facebook..ago' string. Check for 'month' in age or
                               'year' in age to get an estimate of how old the account is. 
        self.othergroupstext  String containing the 'Member of X groups'. For printing purposes
        self.groupcount       Integer containing number of groups applicant is a member of
        self.url              FB URL of applicant
        """
        self.name, self.age, self.othergroupstext, self.url = name, age, othergroupstext, url
        match = re.search(r'\d+', self.othergroupstext)
        if match:
            self.groupcount = int(match.group(0))
        else:
            self.groupcount = 0


class Member(object):

    def __init__(self, name, url, member_since):
        """
        Member class
        Attributes
        self.name
        self.url
        self.member_since  "Added by X about T time ago"
        """
        self.name = name
        self.url = url
        self.member_since = member_since


class FBGroup(object):

    def __init__(self, driver, groupurl):
        """main class that deals with group
        Arguments
        driver   -- A selenium webdriver object. Generally what fbadmin.login() returns.
        groupurl -- Complete url of the FB group (with trailing slash).

        Attributes
        self.applicants -- List of fbadmin.Applicant objects. Represents all the applicants pending membership approval.
                           Refresh by calling self.get_applicants()
        """
        self.driver = driver
        self.groupurl = groupurl
        self.applicants = self.get_applicants()

    def get_applicants(self):
        """Returns List of fbadmin.Applicant objects. Represents all the applicants pending membership approval."""
        self.driver.get(self.groupurl + 'requests')
        try:
            blocks = self.driver.find_elements_by_link_text('Block')
            containers = [
                block.find_element_by_xpath('../..') for block in blocks]
            applicants = [
                Applicant(*self.parse_applicant(container)) for container in containers]
        except:
            applicants = None
        return applicants

    def parse_applicant(self, container):
        name, age, othergroupstext = tuple(container.text.split('\n')[1:4])
        url = container.find_element_by_link_text(name).get_attribute('href')
        return name, age, othergroupstext, url

    def block(self, applicant):
        """blocks applicant. returns name.
        Arguments
        applicant -- fbadmin.Applicant object to be blocked
        """
        self.driver.find_element_by_link_text(applicant.name).find_element_by_xpath(
            '../../../..').find_element_by_link_text('Block').click()
        time.sleep(1)
        print 'blocking', applicant.name
        return applicant.name

    def approve(self, applicant):
        """approves applicant. returns name.
        Arguments
        applicant -- fbadmin.Applicant object to be approved
        """
        self.driver.find_element_by_link_text(applicant.name).find_element_by_xpath(
            '../../../..').find_element_by_link_text('Approve').click()
        time.sleep(1)
        print 'approving', applicant.name
        return applicant.name

    def get_members(self):
        """
        this is a generator method that yields a list of Member objects every iteration.
        changes page every iteration (delay > 3 secs).
        example :
        for page in group.get_members():
            for member in page:
                print member.name #prints member names one page at a time
        """
        self.driver.get(self.groupurl + 'members')
        count = 0
        more = True
        while more:
            members = [Member(*self.parse_member(td))
                       for td in self.driver.find_elements_by_tag_name('td')[count:] if td.text]
            count = len(members)
            more = self.seemore()
            yield members

    def seemore(self):
        try:
            button = self.driver.find_element_by_link_text('See More')
            button.click()
            time.sleep(3)
            return True
        except:
            return False

    def parse_member(self, container):
        d = container.text.split('\n')
        name = d[0]
        member_since = d[-1]
        url = container.find_element_by_link_text(name).get_attribute('href')
        return name, url, member_since

    def peak(self, url):
        """returns the homepage html of url of user
        Arguments
        url -- url of user to peak at
        """
        self.driver.get(url)
        return self.driver.page_source

    def quit(self):
        """Tear Down"""
        self.driver.quit()
