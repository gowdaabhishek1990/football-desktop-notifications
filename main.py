from notifier import notification_system
from titlecase import titlecase

FIXTURES_URL = 'http://www.goal.com/en-india/fixtures/'
RESULTS_URL = 'http://www.goal.com/en-india/results/'
UCL_FIXED = 'uefa-champions-league/10'
EPL_FIXED = 'premier-league/8'
LL_FIXED = 'primera-divisi%C3%B3n/7'
BL_FIXED = 'bundesliga/9'

find_by = titlecase('Chelsea')

if __name__=='__main__':
    notification_system(EPL_FIXED, find_by)
