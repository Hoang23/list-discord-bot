import discord
from discord.ext import commands
import pandas as pd

client = commands.Bot(command_prefix = 'r!')

savedListInDic = {}
currentPassword = "abc123"

@client.event 
async def on_ready(): # when the bot is ready (has all the info from discord)
    #await Bot.change_presence(activity=discord.Game(name='Type !help for usage')) #- new
    await client.change_presence(activity=discord.Game(name='Type !help for usage'))
    print('Bot is ready.')

@client.command(brief="Outputs 'Pong!' and the ping. This is for testing purposes. ")
async def ping(ctx): # context?
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(brief="Create a list and add entries")
async def createList(ctx, title, entries):
    title = title.strip()
    if len(savedListInDic) == 50:
        await ctx.send("Sorry 50 lists is the max limit, try deleting a list before creating a new one") 
        return
    rankingList = entries.split(",") # automatically splits string to a list
    #print(rankingList)
    #await ctx.send(rankingList) 
    savedListInDic[title] = rankingList # save it to the global dictionary

    embed = discord.Embed(
        title = title,
    )
  
    for el, entry in enumerate(savedListInDic[title]):
        embed.add_field(name = el + 1, value = entry, inline = False) # false means they will stack on top of each other

    await ctx.send(embed=embed)

@client.command(brief="Delete a list")
async def deleteList(ctx, listName):
    if listName in savedListInDic:
        del savedListInDic[listName]
        await ctx.send("List successfully deleted")
    else:
        await ctx.send("List does not exist") 

@client.command(brief="view all the lists and their corresponding ranking")
async def lists(ctx):
    # for k, v in savedListInDic.items():
    #     print(k)
    #     await ctx.send(k)

    embed = discord.Embed(
        title = "List names",
    )
  
    for k, v in  savedListInDic.items():
        
        # output = '\n'.join(v)
        output = ", ".join(v)
        embed.add_field(name = k, value = output, inline = False) # false means they will stack on top of each other

    await ctx.send(embed=embed)

@client.command(brief="view specific list")
async def viewList(ctx, listName):
    #print(savedListInDic[listName])
    #await ctx.send(savedListInDic[listName]) 
    if listName in savedListInDic:
        embed = discord.Embed(
            title = listName,
        )
    
        for el, entry in enumerate(savedListInDic[listName]):
            embed.add_field(name = el + 1, value = entry, inline = False) # false means they will stack on top of each other

        await ctx.send(embed=embed)
    else:
        await ctx.send("Error, try again")

@client.command(brief="delete an entry")
async def removeEntry(ctx, listName, entry):
    if listName in savedListInDic and entry in savedListInDic[listName]: 
        savedListInDic[listName].remove(entry)
        await ctx.send("Entry deleted") 
    else:
        await ctx.send("Error, try again") 

# something wrong
@client.command(brief="insert an entry")
async def insertEntry(ctx, listName, position, entry):
    position = int(position)
    savedListInDic[listName].insert(position-1, entry)
    await ctx.send("Successfully inserted") 


@client.command(brief="create csv attachment")
async def generate(ctx):
    # saving to csv
    df=pd.DataFrame.from_dict(savedListInDic,orient='index').transpose()
    df.to_csv("lists.csv", encoding='utf-8', index=False)
    
    # embedding file to discord
    file = discord.File("lists.csv", filename="lists.csv")
    await ctx.send("lists.csv", file=file)

@client.command(brief="set a password")
async def password(ctx, existingPassword, newPassword):
    global currentPassword
    if existingPassword == currentPassword:
        currentPassword = newPassword
        await ctx.send("Password changed successfully")
    else:
        await ctx.send("Error, please try again")
        
@client.command(brief="killswitch - destroys the database")
async def kill(ctx, password):
    global currentPassword # able to passin global variable from at top
    if password == currentPassword:
        global savedListInDic
        del savedListInDic # this probably isnt needed
        savedListInDic = {}
        await ctx.send("All the lists have been deleted") 
        
import os
discord_token = os.environ.get('DISCORD_TOKEN')
client.run(discord_token)
