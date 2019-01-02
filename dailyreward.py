#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      troyc
#
# Created:     02/12/2018
# Copyright:   (c) troyc 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import psycopg2
import os

DATABASE_HOST = os.environ["DATABASE_HOST"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_USER = os.environ["DATABASE_USER"]

def retrieveTime(user_id):
    conn = psycopg2.connect(host = DATABASE_HOST, database = DATABASE_NAME, user = DATABASE_USER, password = DATABASE_PASSWORD)
    cur = conn.cursor()

    cur.execute("select time_claimed from daily_reward where user_id = {0}".format(int(user_id)))
    timeClaimed = cur.fetchall()[0][0]

    cur.close()
    conn.commit()

    return timeClaimed

def changeTime(user_id, newTime):
    conn = psycopg2.connect(host = DATABASE_HOST, database = DATABASE_NAME, user = DATABASE_USER, password = DATABASE_PASSWORD)
    cur = conn.cursor()

    cur.execute("insert into daily_reward(user_id, time_claimed) values({0}, {1}) on conflict(user_id) do update set time_claimed = {1} where daily_reward.user_id = {0} ".format(int(user_id), newTime))

    cur.close()
    conn.commit()

    return





