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
from operator import itemgetter

DATABASE_HOST = os.environ["DATABASE_HOST"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_USER = os.environ["DATABASE_USER"]

def changeBalance(user_id, amount):
    conn = psycopg2.connect(host = DATABASE_HOST, database = DATABASE_NAME, user = DATABASE_USER, password = DATABASE_PASSWORD)
    cur = conn.cursor()

    cur.execute("select balance from coins where user_id = {0}".format(int(user_id)))
    fetched = cur.fetchall()
    try:
        beforeBalance = fetched[0][0]
    except IndexError:
        beforeBalance = 0

    if beforeBalance + amount < 0:
        return False

    cur.execute("insert into coins(user_id, balance) values({0}, {1}) on conflict(user_id) do update set balance = (select coins.balance from coins where coins.user_id = {0}) + {1} where coins.user_id = {0}".format(int(user_id), int(amount)))

    cur.close()
    conn.commit()
    return True

def retrieveBalance(user_id):
    conn = psycopg2.connect(host = DATABASE_HOST, database = DATABASE_NAME, user = DATABASE_USER, password = DATABASE_PASSWORD)
    cur = conn.cursor()

    cur.execute("select balance from coins where user_id = {0}".format(int(user_id)))
    balances = cur.fetchall()

    cur.close()
    conn.commit()

    return (balances[0][0])

def retrieveServerTopBalances(list):
    conn = psycopg2.connect(host = DATABASE_HOST, database = DATABASE_NAME, user = DATABASE_USER, password = DATABASE_PASSWORD)
    cur = conn.cursor()
    memberAndBalances = {}
    for memberID in list:
        cur.execute("select balance from coins where user_id = {0}".format(memberID))
        fetched = cur.fetchall()
        if not fetched == [] and len(memberAndBalances) < 10:
            memberAndBalances[memberID] = fetched[0][0]
    sortedMemberList = sorted(memberAndBalances.items(), key=itemgetter(1), reverse = True)

    cur.close()
    conn.commit()

    return sortedMemberList

def retrieveGlobalTopBalances():
    conn = psycopg2.connect(host = DATABASE_HOST, database = DATABASE_NAME, user = DATABASE_USER, password = DATABASE_PASSWORD)
    cur = conn.cursor()
    cur.execute("select user_id, balance from coins")
    fetched = cur.fetchall()
    counter = 1
    memberAndBalances = {}
    for member in fetched:
        memberAndBalances[member[0]] = member[1]
    sortedMemberList = sorted(memberAndBalances.items(), key=itemgetter(1), reverse = True)

    cur.close()
    conn.commit()

    return sortedMemberList

def checkMemberExists(user_id):
    conn = psycopg2.connect(host = DATABASE_HOST, database = DATABASE_NAME, user = DATABASE_USER, password = DATABASE_PASSWORD)
    cur = conn.cursor()

    cur.execute("select user_id from coins where user_id = {0}".format(user_id))

    if cur.fetchone() is not None:
        return True
    else:
        return False

def createMember(user_id, startingAmount):
    conn = psycopg2.connect(host = DATABASE_HOST, database = DATABASE_NAME, user = DATABASE_USER, password = DATABASE_PASSWORD)
    cur = conn.cursor()

    cur.execute("insert into coins(user_id, balance) values({0}, {1})".format(user_id, startingAmount))

    cur.close()
    conn.commit()





