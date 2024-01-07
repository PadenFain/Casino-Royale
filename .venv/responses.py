import random
import discord
import discord.ui
import time
import pandas as pd



## Create seperate functions to keep command list clearner
async def chat_commands(ctx):
    if ctx.content.startswith('!balance'):
        await  ctx.channel.send(GetBalance(ctx))
    if ctx.content.startswith('!allin'):
        await ctx.channel.send(AllIn(ctx))
    if ctx.content.startswith('!register'):
        await ctx.channel.send(Register(ctx))

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
        randlist = [0, 1]
        randchoice = random.choice(randlist)
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









