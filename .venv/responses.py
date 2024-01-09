import random
import discord
import discord.ui
import time
import pandas as pd
import traceback
import sys
import time



## Create seperate functions to keep command list cleaner
async def chat_commands(ctx):
    if ctx.content.startswith('!balance'):
        await  ctx.channel.send(GetBalance(ctx))
    if ctx.content.startswith('!allin'):
        await ctx.channel.send(AllIn(ctx))
    if ctx.content.startswith('!register'):
        await ctx.channel.send(Register(ctx))
    if ctx.content.startswith('!roulette '):
        await ctx.channel.send(Roulette(ctx))
    if ctx.content.startswith('!roulettehelp'):
        await ctx.channel.send(RouletteHelp)
    if ctx.content.startswith('!help') or ctx.content.startswith('!commands'):
        await ctx.channel.send(Help)

## TODO: Move all functions into a different py file.

## GetRowArray is seperate because it is used in pretty much every command function
def GetRowArray(ctx):
    df = pd.read_csv('userinfo.csv')
    check = df['user_id'].eq(str(ctx.author)).any()
    row = df.loc[df['user_id'] == str(ctx.author)]
    row_string = row.to_string(header=None, index=False)
    row_array = row_string.split()
    return row_array

## Simply gets balance.  Also checks if player is registered, and if not, registers them with a starting balance of 500
def GetBalance(ctx):
    df = pd.read_csv('userinfo.csv')
    check = df['user_id'].eq(str(ctx.author)).any()
    if check:
        row_array = GetRowArray(ctx)
        return (row_array[0] + " your balance is: " + row_array[1])
    else:
        update = {'user_id': [str(ctx.author)], 'balance': [500]}
        update = pd.DataFrame(update)
        update.to_csv('userinfo.csv', mode='a', index=False, header=False)
        return ("Congratulations!  You are now registered.  Your current balance is: 500")

## A 50/50 chance at doubling current balance
def AllIn(ctx):
    df = pd.read_csv('userinfo.csv')
    check = df['user_id'].eq(str(ctx.author)).any()
    if check:
        row_array = GetRowArray(ctx)
        row_index = df.index.get_loc(df.loc[df['user_id'] == str(ctx.author)].index[0])
        bal = int(row_array[1])
        randchoice = random.randint(0,1)
        if randchoice == 0:
            bal = 500
            df.loc[row_index] = [ctx.author, bal]
            response = ("You lose!  New balance: 500 (Balances that fall below 500 will be raised to 500 out of pity)")
            df.to_csv('userinfo.csv', index=False)
        if randchoice == 1:
            bal = bal * 2
            df.loc[row_index] = [ctx.author, bal]
            response = ("You win! New balance: " + str(bal))
            df.to_csv('userinfo.csv', index=False)
        return response

## Pretty much just GetBalance with responses that make more sense for the context
def Register(ctx):
    df = pd.read_csv('userinfo.csv')
    check = df['user_id'].eq(str(ctx.author)).any()
    if check:
        row_array = GetRowArray(ctx)
        return ("You are already registered, your current balance is: " + row_array[1])
    else:
        update = {'user_id': [str(ctx.author)], 'balance': [500]}
        update = pd.DataFrame(update)
        update.to_csv('userinfo.csv', mode='a', index=False, header=False)
        return ("Congratulations!  You are now registered.  Your current balance is: 500")

## TODO: simplify the code in the roulette command, I should be able to pass the actual factoring into a different function and return a payout amount.

RouletteHelp = ("The roulette command needs to be formatted (!roulette [amount you wish to wager] [either a number 0-36 or red/black/green] \nThis command currently only supports single-spot or color bets.")

Help = "!register: Creates your profile.\n\n!balance: Checks your current balance.\n\n!allin: Wagers your entire balance on a 50/50 coinflip.\n\n!roulette [wager] [bet]: Bets on your selected roulette spot.\n\n!roulettehelp: More info on the roulette command."

def Roulette(ctx):
    message_array = ReturnMessageArray(ctx)
    roulette_id = RouletteType(message_array)
    response = "something went wrong"
    result = random.randint(0, 36)
    df = pd.read_csv('userinfo.csv')
    check = df['user_id'].eq(str(ctx.author)).any()
    row_array = GetRowArray(ctx)
    row_index = df.index.get_loc(df.loc[df['user_id'] == str(ctx.author)].index[0])
    wager = int(message_array[1])
    bal = int(row_array[1])
    payout_id = 2
    if check:
        if int(row_array[1]) >= wager >= 0:
            enough_money = True
        else:
            enough_money = False
        if enough_money:
            match roulette_id:
                case 0:
                    if 0 < result <= 16:
                        response = 'Success!'
                        payout_id = 0
                    else:
                        response = 'Failure!'
                case 1:
                    if result == 0:
                        response = 'Success!'
                        payout_id = 1
                    else:
                        response = 'Failure!'
                case 2:
                    response = "Exception caught in RouletteType function.  This may be because you improperly formatted the command.  Use !roulettehelp for more info."
            payout = PayoutMaster(wager, payout_id) - wager
            df.loc[row_index] = [ctx.author, bal + payout]
            df.to_csv('userinfo.csv', index=False)
            response = response + " Your new balance is: " + str(bal + payout)
        if not enough_money:
            response = "You do not have enough money for this wager"
    if not check:
        response = "You are not yet registered.  Please use !register"
    return response

def ReturnMessageArray(ctx):
    message = ctx.content.lower()
    message_array = message.split()
    return message_array

def RouletteType(message_array):
    try:
        if message_array[2] == 'red' or message_array[2] == 'black':
            roulette_id = 0
        elif message_array[2] == 'green':
            roulette_id = 1
        elif 0 < int(message_array[2]) <= 36:
            roulette_id = 1
        else:
            roulette_id = 2
    except Exception:
        roulette_id = 2
    return roulette_id

def PayoutMaster(bet, payout_id):
    match payout_id:
        case 0:
            bet = bet * 2
        case 1:
            bet = bet * 36
        case 2:
            bet = 0
    return bet



