#-------------------------------------------------------------------------------
# Name:        <name>
# Purpose:
#
# Author:      troyc
#
# Created:     <date>
# Copyright:   (c) troyc 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from discord.ext.commands import Bot
import discord
import random
import requests
import os
import pickle
import time
import asyncio

TOKEN = os.environ["BOT_TOKEN"]
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]
DICTIONARY_APP_KEY = os.environ["DICTIONARY_APP_KEY"]
DICTIONARY_APP_ID = os.environ["DICTIONARY_APP_ID"]
BOT_PREFIX = ("d!","D!")
client = Bot(command_prefix = BOT_PREFIX,  case_insensitive = True)


@client.command(name = "8ball",
                description = "Answers a yes or no question",
                brief = "d!8ball",
                aliases = ["eightball"],
                pass_context = True)
async def eight_ball(context):
    possible_answers = [
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes - definitely",
    "You may rely on it",
    "As I see it, yes",
    "Most likely",
    "Reply hazy, try again",
    "Outlook good",
    "Yes",
    "Signs point to yes",
    "Ask again later",
    "Better not tell you now",
    "Cannot predict now",
    "Concentrate and ask again",
    "Don't count on it",
    "My reply is no",
    "My sources say no",
    "Outlook not so good",
    "Very doubtful"]
    await client.say(random.choice(possible_answers) + ", " + context.message.author.mention)


@client.command(name = "sqauare number",
                description = "Squares a number that is given",
                brief = "d!square [number]",
                aliases = ["squared", "square"])
async def square(number):
    try:
        squared_number = int(number) * int(number)
        await client.say(str(number) + " squared is " + str(squared_number))
    except:
        await client.say("That is not supported")


#Clears a channel
@client.command(name = "clear channel",
                description = "Clears a channel",
                brief = "d!clear [channel name]",
                aliases = ["clear"],
                pass_context = True)
async def clearChannel(context, channel: discord.Channel, number, *rubbish):
    if (context.message.author.permissions_in(channel).administrator):
        try:
            '''
            Fails on the delete line in the try section
            '''
            print("1")
            clearNumber = int(number)
            if channel == context.message.channel:
              clearNumber += 1
            print("2")
            await client.send_message(context.message.channel, "Clearing messages...")
            print("3")
            
            for msg in client.logs_from(channel):
                print("4")
                if clearNumber == 0:
                  return
                else:
                  clearNumber -= 1        
                print("5")
                await client.delete_message(msg)
        except:                       
            await client.send_message(context.message.channel, "Clearing messages...")
            async for msg in client.logs_from(channel):
                await client.delete_message(msg)


@client.command(name = "roll dice",
                description = "Rolls a dice",
                brief = "d!rolldice [number of sides]",
                aliases = ["rolldice"],
                pass_context = True)
async def diceRoll(context, numOfSides: int, *rubbish):
    if numOfSides > 9223372036854775807:
        await client.send_message(context.message.channel, ("Sorry we don't have the means to roll a die with " + str(numOfSides) + " sides"))
        return
    possibleResponses = [" is your lucky number", " is the number that has been rolled", " comes out on top"]
    randomNumber = random.choice(range(numOfSides))
    await client.send_message(context.message.channel, (str(randomNumber) + random.choice(possibleResponses)))


@client.command(name = "weather",
            description = "Tells you the weather in a given city",
            brief = "d!weather [city]",
            pass_context = True)
async def weather(context, cityName, *rubbish):
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?q={0}&APPID={1}&units=metric".format(cityName, WEATHER_API_KEY))
    response = r.json()
    weather = response["weather"][0]["main"]
    tempC = response["main"]["temp"]
    tempF = "{0:.1f}".format(float(tempC) / (5/9) + 32)
    print(weather, tempC, tempF)
    await client.send_message(context.message.channel, ("Weather: " + str(weather) + "\nTemperature in Celsius: " + str(tempC) + "\nTemperature in Fahrenheit: " + str(tempF)))


#@client.command(name = "givepoint",
#                description = "Gives you one point",
#                brief = "d!give",
#                aliases = ["give"],
#                pass_context = True)
#async def givePoint(context):
#    author = context.message.author
#    with open("pointFile", "rb") as file:
#        pointList = pickle.load(file)
#    try:
#        pointList[author.id] += 1
#    except:
#        pointList[author.id] = 1
#    with open("pointFile", "wb") as file:
#            pickle.dump(pointList,file)
#    with open("pointFile", "rb") as file:
#        pointList = pickle.load(file)
#        await client.send_message(context.message.channel, ("{0} you know have {1} points".format(author.mention, pointList[author.id])))


@client.command(name = "ping",
                description = "Returns the ping",
                brief = "d!ping",
                pass_context = True)
async def ping(context):
    t1 = time.perf_counter()
    await client.send_typing(context. message.channel)
    t2 = time.perf_counter()
    pingTime = round(t2-t1, 4)
    await client.send_message(context.message.channel, ("Pong: {0}ms".format(pingTime)))


@client.command(name = "google",
                description = "Googles the given search term",
                brief = "d!google [searchTerm]",
                aliases = ["search"],
                pass_context = True)
async def google(context, *searchTerm):
    newSearchTerm = ""
    for character in searchTerm:
        if character == " ":
            character = "+"
        newSearchTerm += character
    r = requests.get("https://www.googleapis.com/customsearch/v1?q={0}&cx=015437053243024247291%3Axwsquiacyd0&key={1}".format(searchTerm, GOOGLE_API_KEY))
    response = r.json()
    try:
        title = response["items"][0]["title"]
        link = response["items"][0]["link"]
        msg = "{0}\n{1}\n".format(title,link)
    except:
        msg = "Sorry that search term returned 0 results"
    await client.send_message(context.message.channel, msg)


@client.command(name = "define",
                description = "Returns the definition of the base word of the given word",
                brief = "d!define [searchWord]",
                aliases = ["dictionary", "definition"],
                pass_context = True)
async def dictionary(context, searchWord):
    language = 'en'
    r = requests.get('https://od-api.oxforddictionaries.com:443/api/v1/inflections/' + language + '/' + searchWord.lower(), headers = {'app_id': DICTIONARY_APP_ID, 'app_key': DICTIONARY_APP_KEY})
    try:
        response = r.json()
    except:
        await client.send_message(context.message.channel, "Sorry no entries of the word {0} could be found".format(searchWord))
        return
    baseword = response["results"][0]["lexicalEntries"][0]["inflectionOf"][0]["id"]
    r = requests.get('https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + baseword, headers = {'app_id': DICTIONARY_APP_ID, 'app_key': DICTIONARY_APP_KEY})
    response = r.json()
    definition = response["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]
    await client.send_message(context.message.channel, (baseword + ", " + definition))


async def print_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current Servers: ")
        for server in client.servers:
            print("{0} : {1}".format(server.name, server.id))
        await asyncio.sleep(86400)

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print('------')

    #try:
    #    with open("pointFile", "rb") as file:
    #        i = 0
    #except:
    #    with open("pointFile", "wb") as file:
    #        pickle.dump({},file)

    await client.change_presence(game=discord.Game(name="d!help", type=0))


client.loop.create_task(print_servers())
client.run(TOKEN)
