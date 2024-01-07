import random
import discord
import discord.ui
import time
import pandas as pd



## Create seperate functions to keep command list clearner
async def chat_commands(ctx):
    if ctx.content.startswith('!balance '):
        await  ctx.channel.send(GetBalance(ctx))
    if ctx.content.startswith('!allin '):
        await ctx.channel.send(AllIn(ctx))
    if ctx.content.startswith('!register '):
        await ctx.channel.send(Register(ctx))
    if ctx.content.startswith('!roulette '):
        await ctx.channel.send(Roulette(ctx))
    if ctx.content.startswith('!roulettehelp'):
        await ctx.channel.send(RouletteHelp)

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

def Roulette(ctx):
    message = ctx.content.lower()
    message_array = message.split()
    df = pd.read_csv('userinfo.csv')
    check = df['user_id'].eq(str(ctx.author)).any()
    if check:
        row_array = GetRowArray(ctx)
        row_index = df.index.get_loc(df.loc[df['user_id'] == str(ctx.author)].index[0])
        wager = int(message_array[1])
        bet = message_array[2]
        bal = int(row_array[1])
        result = random.randint(0, 36)

        ## sets bools for what type of bet this is
        try:
            if int(row_array[1]) >= wager:
                enough_money = True
            elif int(row_array[1]) < wager:
                enough_money = False
            if message_array[2] == 'black' or message_array[2] == 'red' or message_array[2] == 'green':
                colors = True
            else:
                colors = False

            ## checks bools and runs bet
            if enough_money and colors and message_array[2] != 'green':
                if result >= 17:
                    response = 'success'
                    bal = bal + wager
                else:
                    response = 'failure'
                    bal = bal - wager
            if enough_money and colors and message_array[2] == 'green':
                if result == 0:
                    response = 'success'
                    bal = bal + (wager * 35) - wager
                else:
                    response = 'failure'
                    bal = bal - wager
            if enough_money and not colors:
                    if result == int(message_array[2]):
                        response = 'success'
                        bal = bal + (wager * 35) - wager
                    else:
                        response = 'failure'
                        bal = bal - wage
            if not enough_money:
                response = "You don't have enough money for this wager!"
            df.loc[row_index] = [ctx.author, bal]
            df.to_csv('userinfo.csv', index=False)
        except Exception:
            response = "Exception caught.  This is likely a formatting error on your part.  Please use !roulettehelp for more info"
    if not check:
        response = Register(ctx)
    return response

RouletteHelp = ("The roulette command needs to be formatted (!roulette [amount you wish to wager] [either a number 0-36 or red/black/green] \nThis command currently only supports single-spot or color bets."
                "")










