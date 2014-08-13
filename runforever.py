'''
Created on Aug 10, 2014

@author: Amit
'''
import sys
import time
from main import *
import MySQLdb as mdb
from util import *
from database import *
from monitoring import *
from celery.task.control import discard_all

config = read_config_file(get_absolute_path("config.ini"))

def main_loop(debug=False):
    con = None
    count = 1
    generate_report_nth_hour = 0.5
    last_report_generated_time = time.time()
    worker_id = 0
    while 1:
        cur_time = time.time()
        if ( cur_time - last_report_generated_time ) / (60 * 60) > generate_report_nth_hour:
            generate_and_send_report(config,last_report_generated_time,cur_time)
            print "generating report at" 
            print cur_time
            last_report_generated_time = cur_time
        
        con = test_and_get_mysql_con(0, con, config,debug=False)
        ans = select_from_table(con,worker_id, "twitter_auths", "COUNT(*) as count", {"active_status" : 0}, count="one", debug=False)
        print get_current_timestamp() + " --> Starting " + str(ans['count']) + " workers"
        for i in range(0,ans['count']):
            worker_main.delay(count,debug=True)
            count = count + 1
            time.sleep(0.5)
        time.sleep(5)

if __name__ == '__main__':
    try:
        main_loop(debug=True)
    except KeyboardInterrupt:
        discard_all()
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)