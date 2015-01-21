#fbadmin
## A python library to admin facebook groups that uses selenium and phantomjs behind the scenes

### Dependencies
####phantomjs                               
Easiest way to install phantomjs is via ```npm```                    
```npm install phantomjs```                        

####selenium                                          
```pip install selenium```

###Usage
####Login and instantiate FBgroup

```
from fbadmin import login,FBGroup
group_url='https://www.facebook.com/groups/782652721814257/'
group=FBGroup(login(),group_url)
```
####Print all applicants and the number of groups they are members of.                          

```
for applicant in group.applicants:
    print applicant.name,applicant.groupcount
     
Liviu Vs Ze'us 17
Iliya Tamarkin 24
Raj K Rana 21
Royendgel Silberie 41
Bishnu Prasad Chowdhury 27
Taranjeet Galactus Singh 13
Aws Al-Aisafa 4
أحمد محمود محمد عبدالوهاب 49
Lha Ckg 22
Krishna Jha 10
Bhavesh Nigam 48
Jeevan Anand Anne 19
Sai Sandeep 19
Raga Tarun 25
Tarun Tremendous 48
Aakeem Coleman 37
Bill Pearce 17
Derrick Kearney 17

```

####Block if member of more than 100 groups and approve if member of less than 10 groups

```
for applicant in group.applicants:
    if applicant.groupcount>100:
        group.block(applicant)
    elif applicant.groupcount<=10:
        group.approve(applicant)

```

####Get members

```
for page in group.get_members():
    for member in page:
        print member.name #prints member names one page at a time
```

####Get source of member's homepage(for spam analysis)

```
html=group.peak(member.url)
```

####Teardown when done with it                  

```
group.quit()
```
####Please look at the code for other functionality. There are docstrings.

###needs a config file of following format to be saved as credentials.cfg

```
#This is the configuration file. Enter FB credentials here.
[credentials]
email = malcolmreynolds@serenity.com
password = youcanttaketheskyfromme
```

Suggestions/Comments/Issues can be sent at dodo.dodder@gmail.com