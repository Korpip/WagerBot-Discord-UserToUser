from OAuth2Info import *
from discord.ext import commands
# test data
openwagers = {'<@698664004322852904>': {'<@698664004322852904>': '600', '<@115644712135688193>': '600'}}
confirmedwagers = {}
wagersloss = {}
wagerswon = {}
settings = {
  "userlimit": 0,  # 0 = Everyone can play, 1 = subscribed only, 2 = only mods can play
  "minbet": "20",
  "currency": "USD"
}
description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='!', description=description)
# print some log data on bot creation in server
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    #print(bot.user.id)
    print('------')

#log data in terminal
@bot.event
async def event_message(ctx):
    if ctx.author.name.lower() == bot.user.name:
        return
    print(f'{ctx.channel} - {ctx.author.name}: {ctx.content}')

#when a user types !wager then do stuff.
#wager cat 500
#!wager command/name amount
#if amount is there then command/name is name
#if no amount is there then command/name is command
@bot.command(name='wager')
async def wager(ctx, *args):
    global openwagers
    global confirmedwagers
    global settings # not used yet
    player2 = ""
    amount = ""
    command = ""
    player1 = "<@"+str(ctx.author.id)+">".strip('!')
    countargs = len(args)
    if countargs == 2 and args[0].startswith('<@') and args[0].endswith('>'):
        work = args[0].strip('<@!>')
        player2 = '<@'+ work +'>'
        amount = args[1]
    elif countargs == 2 and not args[0].isdigit():
        command = args[0]
        work = args[1].strip('<@!>')
        player2 = '<@'+ work +'>'
    elif countargs == 1:
        command = args[0]
    #Lets print out this data for testing
    print("player1 is "+ player1)
    print("player2 is "+ player2)
    print("command is "+ command)
    # If name is a name and amount is a number
    if amount.isdigit() and player2 != "":
        if player1 in openwagers and player2 in openwagers[player1]:
            #does person have bets?
            openwagers[player1][player2] = int(openwagers[player1][player2]) + int(amount)
            await ctx.channel.send(
            f"{player1} adding another {amount} to their open wager for a total of {openwagers[player1]} ! If this is too much for you please use the !wager remove command.")
        else:
            if player1 in openwagers:
                #start bets for anount with user
                await ctx.channel.send(f"{player1} wants to wager {player2} for {amount}!")
                thingTo = {player2: amount}
                openwagers[player1].update(thingTo)
            else:
                await ctx.channel.send(f"{player1} wants to wager {player2} for {amount}!")
                openwagers[player1] = {player2 : amount}
    #Remove your open wager to someone
    elif player2 != "" and command == 'remove':
        del openwagers[player1][player2]
        await ctx.channel.send(f"{player1} removed their wager with {player2}!")
    #Confirm your open wager to someone
    elif player2 != "" and command == 'confirm':
        #is there already a confirmed wager?
        if player1 in confirmedwagers and player2 in confirmedwagers[player1]:
            confirmedwagers[player1][player2] = int(confirmedwagers[player1][player2]) + int(openwagers[player2][player1])
            await ctx.channel.send(
            f"{player1} adding another {amount} to their open wager for a total of {openwagers[player1]} ! If this is too much for you please use the !wager remove command.")
        #If no then make one
        else:
            bet = openwagers[player2][player1]
            confirmedwagers[player1] = {player2 : bet}
            del openwagers[player2][player1]
            await ctx.channel.send(f"Hey {player2}, {player1} confirmed their wager!")
    elif player2 != "" and command == 'pay':
        #is there already a confirmed wager then pay out if you loss
        if player1 in confirmedwagers and player2 in confirmedwagers[player1]:
            del confirmedwagers[player1][player2]
            await ctx.channel.send(f"Hey {player2}, {player1} paid out their loss wager - That needs additional API!")
        elif player2 in confirmedwagers and player1 in confirmedwagers[player2]:
            del confirmedwagers[player2][player1]
            await ctx.channel.send(f"Hey {player2}, {player1} paid out their loss wager - That needs additional API!")
        #If none alert user
        else:
            await ctx.channel.send(f"Hey {player1} you don't have a wager confirmed with {player2}")
    #Show wagers
    elif command == 'show':
        print("Open")
        print(openwagers)
        print("Confirmed")
        print(confirmedwagers)
        await ctx.channel.send(f"Openwagers {openwagers} confirmedwagers {confirmedwagers}")
    #Finally just show how to use the wager command when no other conditionals are met
    else:
        await ctx.channel.send(
            f"{player1} to use this bot you need to use the format !wager command/name amount.  Amount is not always needed and not putting a command/name in shows you this help info.  Commands are show/remove/confirm/pay.")


bot.run(OTOKEN)
