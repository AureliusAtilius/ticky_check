#!/usr/bin/env python3
import operator
import sys
import re
import csv

error = {}
per_user = {}
#edit "syslog.log" with the desired filepath/file
with open("syslog.log","r") as log:
    for line in log.readlines():
        line = line.strip()
        log_type = (re.search(r"(INFO|ERROR)",line)).group(1)
        username = (re.search(r"\((.*)\)",line)).group(1)
        log_message = (re.search(r"(INFO|ERROR) ([\w ']*) ",line)).group(2)
        bad_names = ["jackowens","kirknixon","mai.hendrix","mcintosh","mdouglas","montanap","noel","nonummy","oren","rr.robinson","sri","xlg"]
        
        if username not in per_user:
            log_count = {'INFO': 0, 'ERROR': 0}
            per_user[username] = log_count
            per_user[username][log_type]+=1
        else:
            per_user[username][log_type]+=1
        if log_type =="ERROR":
            if log_message not in error:
                    error[log_message]=0
                    error[log_message]+=1
            else:
                    error[log_message]+=1



#sort dictionaries, per_user is sorted by username, error is sorted by number of occurences.
per_user_list = {}
per_user_list = sorted(per_user.items(), key = operator.itemgetter(0))

error_list = sorted(error.items(), key=operator.itemgetter(1),reverse=True)

#create error_message.csv
with open("error_message.csv","w", newline='') as err_report:
    header = ["Error".strip(), "Count".rstrip()]
    csv.writer(err_report).writerow(header)
    for line in error_list:
        csv.writer(err_report).writerow( [line[0], str(line[1]).rstrip()])

with open("user_statistics.csv", "w", newline = "") as user_report:
    header = ["Username", "INFO", "ERROR"]
    csv.writer(user_report).writerow(header)
    for line in per_user_list:
        csv.writer(user_report).writerow([line[0],line[1]["INFO"],line[1]["ERROR"]])
