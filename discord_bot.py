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
from discord.ext import commands
import discord
import random
import requests
import os
import pickle
import time
import asyncio
import psycopg2
import coins
import daily_reward
import time

TOKEN = os.environ["BOT_TOKEN"]
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]
DICTIONARY_APP_KEY = os.environ["DICTIONARY_APP_KEY"]
DICTIONARY_APP_ID = os.environ["DICTIONARY_APP_ID"]
TRN_API_KEY = os.environ["TRN_API_KEY"]
DATABASE_HOST = os.environ["DATABASE_HOST"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_USER = os.environ["DATABASE_USER"]

BOT_PREFIX = ("d!","D!")
client = commands.Bot(command_prefix = BOT_PREFIX,  case_insensitive = True)


@client.command(name = "8ball",
                description = "Answers a yes or no question",
                brief = "d!8ball",
                aliases = ["eightball"],
                pass_context = True)
async def eight_ball(ctx):
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
    await client.send_message(ctx.message.channel, ctx.message.author.mention + ", " + random.choice(possible_answers))


@client.command(name = "sqauare number",
                description = "Squares a number that is given",
                brief = "d!square [number]",
                aliases = ["squared", "square"],
                pass_context = True)
async def square(ctx, number):
    try:
        squared_number = int(number) * int(number)
        await client.send_message(ctx.message.channel, str(number) + " squared is " + str(squared_number))
    except:
        await client.send_message(ctx.message.channel, "That is not supported")


#Clears a channel
@client.command(name = "clear channel",
                description = "Clears a channel, the number of messages to delete is optional but if not provided it will delete all",
                brief = "d!clear [channel name] [num of msgs]",
                aliases = ["clear"],
                pass_context = True)
async def clearChannel(ctx, channel: discord.Channel, number, *rubbish):
    if (ctx.message.author.permissions_in(channel).administrator):
        try:
            clearNumber = int(number) + 1
            if channel != ctx.message.channel:
              clearNumber -= 1
              await client.send_message(ctx.message.channel, "Clearing messages...")

            async for msg in client.logs_from(channel):
                if clearNumber == 0:
                  return
                else:
                  clearNumber -= 1
                await client.delete_message(msg)
        except:
            await client.send_message(ctx.message.channel, "Clearing messages...")
            async for msg in client.logs_from(channel):
                await client.delete_message(msg)
    else:
        return

@client.command(name = "roll dice",
                description = "Rolls a dice",
                brief = "d!rolldice [number of sides]",
                aliases = ["rolldice"],
                pass_context = True)
async def diceRoll(ctx, numOfSides, *rubbish):
    if numOfSides > 9223372036854775807:
        await client.send_message(ctx.message.channel, ("Sorry I do not have the means to roll a die with " + str(numOfSides) + " sides"))
        return
    try:
        numOfSides = int(numOfSides)
    except:
        client.send_message(ctx.message.channel, "I can not roll a die with \"" + numOfSides + "\" sides" )
        return
    possibleResponses = [" is your lucky number", " is the number that I have rolled", " comes out on top"]
    randomNumber = random.choice(range(numOfSides))
    await client.send_message(ctx.message.channel, (str(randomNumber) + random.choice(possibleResponses)))


@client.command(name = "weather",
            description = "Tells you the weather in a given city",
            brief = "d!weather [city]",
            pass_context = True)
async def weather(ctx, cityName, *rubbish):
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?q={0}&APPID={1}&units=metric".format(cityName, WEATHER_API_KEY))
    response = r.json()
    try:
        weather = response["weather"][0]["main"]
    except:
        client.send_message(ctx.message.channel, ("I could not find a city with the name " + cityName))
        return
    tempC = response["main"]["temp"]
    tempF = "{0:.1f}".format(float(tempC) / (5/9) + 32)
    await client.send_message(ctx.message.channel, ("Weather: " + str(weather) + "\nTemperature in Celsius: " + str(tempC) + "\nTemperature in Fahrenheit: " + str(tempF)))


@client.command(name = "ping",
                description = "Returns the ping",
                brief = "d!ping",
                pass_context = True)
async def ping(ctx):
    t1 = time.perf_counter()
    await client.send_typing(ctx. message.channel)
    t2 = time.perf_counter()
    pingTime = round(t2-t1, 4)
    await client.send_message(ctx.message.channel, ("Pong: {0}ms".format(pingTime)))


@client.command(name = "google",
                description = "Googles the given search term",
                brief = "d!google [searchTerm]",
                aliases = ["search"],
                pass_context = True)
async def google(ctx, *searchTerm):
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
        return
    await client.send_message(ctx.message.channel, msg)

@client.command(name = "img",
                description = "Finds an image from the given search term",
                brief = "d!img [searchTerm]",
                aliases = ["image"],
                pass_context = True)
async def imageSearcher(ctx, *searchTerm):
    newSearchTerm = ""
    for character in searchTerm:
        if character == " ":
            character = "+"
        newSearchTerm += character
    r = requests.get("https://www.googleapis.com/customsearch/v1?q={q}&cx={cx}&safe={safe}&searchType={searchType}&key={key}".format(q=searchTerm, key=GOOGLE_API_KEY, searchType="image", safe="active", cx="015437053243024247291:m03jsgc6a6g"))
    response = r.json()
    # try:
    await client.send_message(ctx.message.channel, response["items"][0]["link"])
    #except:
    #    await client.send_message(ctx.message.channel, "lol fail")

    #await client.send_message(ctx.message.channel, msg)


@client.command(name = "define",
                description = "Returns the definition of the base word of the given word",
                brief = "d!define [searchWord]",
                aliases = ["dictionary", "definition"],
                pass_context = True)
async def dictionary(ctx, searchWord):
    language = 'en'
    r = requests.get('https://od-api.oxforddictionaries.com:443/api/v1/inflections/' + language + '/' + searchWord.lower(), headers = {'app_id': DICTIONARY_APP_ID, 'app_key': DICTIONARY_APP_KEY})
    try:
        response = r.json()
    except:
        await client.send_message(ctx.message.channel, "Sorry no entries of the word {0} could be found".format(searchWord))
        return
    baseword = response["results"][0]["lexicalEntries"][0]["inflectionOf"][0]["id"]
    r = requests.get('https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + baseword, headers = {'app_id': DICTIONARY_APP_ID, 'app_key': DICTIONARY_APP_KEY})
    response = r.json()
    definition = response["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]
    await client.send_message(ctx.message.channel, (baseword + ", " + definition))


@client.command(name = "fortnite_stats",
                description = "Gives a wide range of stats.\nCredit: Fortnite Tracker, https://fortnitetracker.com/",
                brief = "d!fortnite [platform] [playerName]",
                pass_context = True)
async def fortniteStats(ctx, platform, playerName):
    r = requests.get("https://api.fortnitetracker.com/v1/profile/{0}/{1}".format(platform.lower(), playerName), headers = {"TRN-Api-Key": TRN_API_KEY})

    try:
            response = r.json()
    except:
        client.send_message(ctx.message.channel, ("Sorry the platform {0} is not recognized".format(platform)))
        return
    #p2 = solo
    #p10 = duo
    #p9 = squad

    try:
        lifeTimeStats = response.get("lifeTimeStats", "not found")
        overallGamesPlayed = lifeTimeStats[7]["value"]
        overallWins = lifeTimeStats[8]["value"]
        overallWinPercentage = lifeTimeStats[9]["value"]
        overallKills = lifeTimeStats[10]["value"]
        overallKD = lifeTimeStats[11]["value"]
    except:
        await client.send_message(ctx.message.channel, "The player {0} could either not be found on the platform {1} or has not played a game".format(platformName, platform))
        return

    try:
        soloStats = response["stats"].get("p2", "not found")
        soloGamesPlayed = soloStats["matches"]["valueInt"]
        soloWins = soloStats["top1"]["valueInt"]
        soloWinPercentage = soloStats["winRatio"]["valueDec"]
        soloKills = soloStats["kills"]["valueInt"]
        soloKD = soloStats["kd"]["valueDec"]
    except:
        soloGamesPlayed = 0
        soloWins = 0
        soloWinPercentage = 0
        soloKills = 0
        soloKD = 0

    try:
        duoStats = response["stats"].get("p10", "not found")
        duoGamesPlayed = duoStats["matches"]["valueInt"]
        duoWins = duoStats["top1"]["valueInt"]
        duoWinPercentage = duoStats["winRatio"]["valueDec"]
        duoKills = duoStats["kills"]["valueInt"]
        duoKD = duoStats["kd"]["valueDec"]
    except:
        duoGamesPlayed = 0
        duoWins = 0
        duoWinPercentage = 0
        duoKills = 0
        duoKD = 0

    try:
        squadStats = response["stats"].get("p9", "not found")
        squadGamesPlayed = squadStats["matches"]["valueInt"]
        squadWins = squadStats["top1"]["valueInt"]
        squadWinPercentage = squadStats["winRatio"]["valueDec"]
        squadKills = squadStats["kills"]["valueInt"]
        squadKD = squadStats["kd"]["valueDec"]
    except:
        squadGamesPlayed = 0
        squadWins = 0
        squadWinPercentage = 0
        squadKills = 0
        squadKD = 0

    platformName = response.get("platformNameLong", "not found")
    epicName = response.get("epicUserHandle", "not found")

    await client.send_message(ctx.message.channel, "{0} - {21}\n\nOverall: \nGames Played: {1}\nWins: {2}\nWin Percentage: {3}\nKills: {4}\nK/D: {5}\n\nSolo: \nGames Played: {6}\nWins: {7}\nWin Percentage: {8}%\nKills: {9}\nK/D: {10}\n\nDuo: \nGames Played: {11}\nWins: {12}\nWin Percentage: {13}%\nKills: {14}\nK/D: {15}\n\nSquad: \nGames Played: {16}\nWins: {17}\nWin Percentage: {18}\nKills: {19}\nK/D: {20}".format(epicName, overallGamesPlayed, overallWins, overallWinPercentage, overallKills, overallKD, soloGamesPlayed, soloWins, soloWinPercentage, soloKills, soloKD, duoGamesPlayed, duoWins, duoWinPercentage, duoKills, duoKD, squadGamesPlayed, squadWins, squadWinPercentage, squadKills, squadKD, platformName))


@client.command(name = "give",
                pass_context = True)
async def giveCoins(ctx, amount, *, receiver: discord.Member):
    sender = ctx.message.author
    channel = ctx.message.channel
    if not await checkMemberExists(channel, sender):
        return
    if not await checkMemberExists(channel, receiver):
        return

    #checks if the amount is not an int
    try:
        amount = int(amount)
    except:
        await client.send_message(ctx.message.channel, "The amount given needs to be a whole number")
        return

    #checks if the amount is negative
    if amount < 0:
        await client.send_message(ctx.message.channel, sender.mention + " tryna steal " + receiver.mention + "\'s coins :thinking:")
        return

    #take cash from the sender
    accepted = coins.changeBalance(sender.id, int(amount*-1))
    if accepted:
        #give cash to the receiver
        coins.changeBalance(receiver.id, int(amount))
        await client.send_message(ctx.message.channel, "Transfer Complete")
        return
    else:
        await client.send_message(ctx.message.channel, "Transfer Declined")
        return


@client.command(name = "balance",
                pass_context = True)
async def printBalance(ctx):
    member = ctx.message.author
    channel = ctx.message.channel
    if not await checkMemberExists(channel, member):
        return
    balance = coins.retrieveBalance(member.id)
    await client.send_message(channel, "{0} Balance: {1} Coins".format(member.mention, balance))


@client.command(name = "servertop",
                pass_context = True)
async def getServerTopBalances(ctx):
    memberIDs = []
    allServerMembers = ctx.message.server.members
    for member in allServerMembers:
        memberIDs.append(member.id)
    topServerMembers = coins.retrieveServerTopBalances(memberIDs)
    msg = "```\nTop 10 in your Server\n"
    counter = 1
    for member in topServerMembers:
        serverMember = await client.get_user_info(member[0])
        msg += "{0}. {1} - {2} Coins\n".format(counter, serverMember.display_name, member[1])
        counter += 1
    await client.send_message(ctx.message.channel, msg + "```")


@client.command(name = "globaltop",
                pass_context = True)
async def getGlobalTopBalances(ctx):
    topGlobalMembers = coins.retrieveGlobalTopBalances()
    msg = "```\nTop 10 Global\n"
    counter = 1
    for member in topGlobalMembers:
        globalMember = await client.get_user_info(member[0])
        msg += "{0}. {1} - {2} Coins\n".format(counter, globalMember.display_name, member[1])
        counter += 1
    await client.send_message(ctx.message.channel, msg + "```")


@client.command(name = "rps",
                pass_context = True)
async def rps(ctx):
    player = ctx.message.author
    channel = ctx.message.channel

    if not await checkMemberExists(channel, player):
        return

    beforeBalance = coins.retrieveBalance(player.id)
    if beforeBalance < 1:
        await client.send_message(channel, "You don't have enough coins to play Paper Scissors Rock")
        return

    await client.send_message(channel, "- Rock Paper Scissors - \nChoose your weapon")
    response = await client.wait_for_message(author = player, channel = channel)
    choices = ["r","p","s"]
    botChoice = random.choice(choices)
    botChoice = [item for item in ["rock", "paper", "scissors"] if item.startswith(botChoice)][0]
    result = None
    if response:
        if not response.content[0].lower() in choices:
            await client.send_message(channel, "Input not recognized, Session Terminated")
            return
        elif response.content[0].lower() == botChoice[0]:
            result = "tied"
            balanceChange = 0
        elif response.content[0].lower() == "r":
            if "p" == botChoice[0]:
                result = "lost"
                balanceChange = -1
        elif response.content[0].lower() == "p":
            if "s" == botChoice[0]:
                result = "lost"
                balanceChange = -1
        elif response.content[0].lower() == "s":
            if "r" == botChoice[0]:
                result = "lost"
                balanceChange = -1
        if result == None:
            result = "won"
            balanceChange = 1
    else:
        return
    coins.changeBalance(player.id, balanceChange)
    if result in ["won", "lost"]:
        await client.send_message(channel, player.mention + "I played {0} meaning you {1} 1 coin!".format(botChoice, result))
    else:
        await client.send_message(channel, player.mention + "I played {0} meaning we tied!".format(botChoice, result))
    newBalance = coins.retrieveBalance(player.id)
    await client.send_message(channel, "You're new balance is {0} coins".format(newBalance))


async def checkMemberExists(channel, member):
    memberExists = coins.checkMemberExists(member.id)
    if not memberExists:
        await client.send_message(channel, "The user {0} has not opened an account with me\nTo do so type d!start in a channel where I have access to".format(ctx.message.author.mention))
        return False
    else:
        return True


@client.command(name = "start",
                pass_context = True)
async def createMember(ctx):
    member = ctx.message.author
    channel = ctx.message.channel
    startingBalance = 10

    if checkMemberExists(channel, member):
        await client.send_message(channel, "{0} you have already opened an account with me".format(member.mention))

    coins.changeBalance(member.id, startingBalance)
    dailyreward.changeTime(member.id, 0)


@client.command(name = "daily",
                pass_context = True)
async def dailyReward(ctx):
    member = ctx.message.author
    channel = ctx.message.channel
    dailyRewardAmount = 10
    currentTime = time.time()

    if not await checkMemberExists(channel, member):
        return

    secondsPassedBetweenClaim = currentTime - dailyreward.retrieveTime(member.id)

    if secondsPassedBetweenClaim > 86400:
        coins.changeBalance(member.id, dailyRewardAmount)
        dailyreward.changeTime(member.id, currentTime)
        await client.send_message(channel, "Daily Reward of {0} coins claimed by {1}".format(dailyRewardAmount, member.mention))
    else:
        await client.send_message(channel, "{0} you need to wait {1} hours and {2} minutes to claim your daily reward".format(member.mention, int(23 - secondsPassedBetweenClaim // 3600), int(59 - secondsPassedBetweenClaim // 60)))



async def print_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("------\nCurrent Servers: ")
        for server in client.servers:
            print("{0} : {1}".format(server.name, server.id))
        print("------")
        await asyncio.sleep(259200)


#@client.event
#async def on_command_error(event, ctx, *args, **kwargs):
#    if isinstance(event, commands.CommandNotFound):
#        await client.send_message(ctx.message.channel, event)
#        return
#    elif isinstance(event, commands.BadArgument):
#        await client.send_message(ctx.message.channel, event)
#        return




@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print('------')

    await client.change_presence(game=discord.Game(name="d!help", type=0))


client.loop.create_task(print_servers())
client.run(TOKEN)
