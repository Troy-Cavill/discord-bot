from discord.ext.commands import Bot
import discord
import random
import requests
import os

BOT_PREFIX = "d!"
TOKEN = os.environ["BOT_TOKEN"]
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
async def diceRoll(context, numOfSides: int, *rubbish):
    if numOfSides > 9223372036854775807:
        await client.send_message(context.message.channel, ("Sorry we don't have the means to roll a die with " + str(numOfSides) + " sides"))
        return
    possibleResponses = [" is your lucky number", " is the number that has been rolled", " comes out on top"]
    randomNumber = random.choice(range(numOfSides))
    await client.send_message(context.message.channel, (str(randomNumber) + random.choice(possibleResponses)))


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name="d!help", type=0))
client.run(TOKEN)
