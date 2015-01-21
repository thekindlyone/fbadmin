from fbadmin import FBGroup, login

group = FBGroup(login(), 'https://www.facebook.com/groups/782652721814257/')
for applicant in group.applicants:
    print applicant.name, applicant.age, 'other groups =', applicant.groupcount
    if applicant.groupcount > 50:
        try:
            group.block(applicant)
        except:
            print'Failed'
    elif applicant.groupcount < 10 and 'month' not in applicant.age:
        try:
            group.approve(applicant)
        except:
            print 'Failed'

group.quit()  # teardown
