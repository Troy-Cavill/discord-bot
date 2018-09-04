#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      troyc
#
# Created:     01/09/2018
# Copyright:   (c) troyc 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from discord.ext.commands import Bot
import discord
import random

BOT_PREFIX = "d!"
client = Bot(command_prefix=BOT_PREFIX)


@client.command(name = "8ball",
                description = "Answers a yes or no question",
                brief = "d!8ball",
                aliases = ["eightball", "eight ball", "8 ball"],
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
async def clearChannel(context, channel: discord.Channel, *leftOvers):
    if str(channel) == "testing-in-private":
        await client.send_message(context.message.channel, "That is unsupported")
        return
    if (context.message.author.permissions_in(context.message.channel).administrator):
            await client.send_message(context.message.channel, "Clearing messages...")
            async for msg in client.logs_from(channel):
                await client.delete_message(msg)

@client.command(name = "roll dice",
                description = "Rolls a dice",
                brief = "d!rolldice [number of sides]",
                aliases = ["rolldice"], 
                pass_context = True)
async def diceRoll(context, numOfSides, *rubbish):
    randomNumber = random.choice(range(int(numOfSides)))
    await client.send_message(str(context.message.channel) + str(randomNumber) + ", is your lucky number")


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name="d!help", type=0))



client.run("NDU4MTQ3Mzc3MTQwODU4ODkw.Dm9E_g.sPRmqq6142p7-I0bfUdflRh-U2c")
