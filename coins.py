#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      troyc
#
# Created:     03/11/2018
# Copyright:   (c) troyc 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import psycopg2
import os

DATABASE_HOST = os.environ["DATABASE_HOST"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_USER = os.environ["DATABASE_USER"]

def changeBalance(user_id, amount):
    conn = psycopg2.connect(host = DATABASE_HOST, database = DATABASE_NAME, user = DATABASE_USER, password = DATABASE_PASSWORD)
    cur = conn.cursor()

    cur.execute("insert into coins(user_id, balance) values({0}, {1}) on conflict(user_id) do update set balance = (select coins.balance from coins where coins.user_id = {0}) + {1} where coins.user_id = {0}".format(int(user_id), int(amount)))

    cur.close()
    conn.commit()
    return

def retrieveBalance(user_id):
    conn = psycopg2.connect(host = DATABASE_HOST, database = DATABASE_NAME, user = DATABASE_USER, password = DATABASE_PASSWORD)
    cur = conn.cursor()

    cur.execute("select balance from coins where user_id = {0}".format(int(user_id)))
    balances = cur.fetchall()
    print(balances[0][0])

    cur.close()
    conn.commit()
