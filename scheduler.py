'''
Created on Aug 6, 2014

@author: Amit

Scheduling Algorithms to pick the next query
'''
from database import *

# query type corresponds to table_name
def last_accessed_first(con,worker_id,debug=False):
    try:
        user = get_user(con, worker_id, debug)
        if debug:
            print "taskid--" + str(worker_id) +" got user " + str(user)
        
        keyword = get_keyword(con, worker_id, debug)
        if debug:
            print "taskid--" + str(worker_id) +" got keyword " + str(keyword)
    
        if user and keyword:
            user_last_access_time = user['last_access']
            keyword_last_access_time = keyword['last_access']
            if user_last_access_time < keyword_last_access_time:
                release_keyword(con, worker_id, keyword["id"], debug)
                return ("users",user)
            else:
                release_user(con, worker_id, user["id"], debug)
                return ("keywords",keyword)
        elif keyword:
            return ("keywords",keyword)
        elif user:
            return ("users",user)
        return
    except Exception, e:
        try:
            if user:
                release_user(con, worker_id, user["id"], debug)
        except Exception, e:
             pass                
    
        try:
            if keyword:
                release_keyword(con, worker_id, keyword["id"], debug)
        except Exception, e:
             pass                
    
    
if __name__ == '__main__':
    pass
