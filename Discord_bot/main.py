import json

import discord
from discord.ext import commands
import sqlite3
import string, json

from settings import TOKEN


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Hello world!")

    global base, cur
    base = sqlite3.connect("Gen.db")
    cur = base.cursor()

# arg - принимает произвольное число аргументов
# async def инфо(ctx, *, arg):
#     await ctx.send(arg)
@bot.command()
async def инфо(ctx, arg=None):
    author = ctx.message.author
    if arg == None:
        await ctx.send(f"{author.mention} <Некая информация>")
    elif arg == "secret":
        await ctx.send(f"{author.mention} Пссс, это секрет")
    else:
        await ctx.send(f"{arg} - неизвестный параметр")
@bot.command()
async def статус(ctx):
    base.execute(f'CREATE TABLE IF NOT EXIST {ctx.message.guild.name}(userid INT, count INT)')
    base.commit()
    warning = cur.execute("SELECT * FROM {} WHERE userid == ?".format(ctx.message.guild.name), (ctx.message.author.id, )).fetchone()
    if warning is None:
        await ctx.send(f"{ctx.message.author.mention} У вас нету предупреждений")
@bot.even
async def on_message(message):
    with open('list.json', "r", encoding='utf-8') as file:
        unset = set(json.load(file))
    # if "дела" in message.content.lower():
    #     await message.channel.send("Норм")
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.content.split(" ")} \
            .intersection(unset) != set():
        await message.channel.send(f"{message.author.mention}, маты запрещены!!!")
        await message.delete()

        name = message.guild.name
        base.execute(f'CREATE TABLE IF NOT EXIST {name}(userid INT, count INT)')
        base.commit()

        warning = cur.execute("SELECT * FROM {} WHERE userid == ?".format(name), (message.author.id, )).fetchone()
        if warning == None:
            cur.execute("INSERT INTO {} VALUES(?, ?)".format(name), (message.author.id, 1))
            base.commit()
            await message.channel.send(f"{message.author.mention}, первое предупреждение")
        elif warning[1] == 1:
            cur.execute(f"UPDATE {name} SET count == ? WHERE userid == ?", (2, message.author.id))
            base.commit()
            await message.channel.send(f"{message.author.mention}, второе предупреждение")
        elif warning[1] == 2:
            cur.execute(f"UPDATE {name} SET count == ? WHERE userid == ?", (3, message.author.id))
            base.commit()
            await message.channel.send(f"{message.author.mention}, забанен за мат в чате")
            await message.author.ban(reason="Мат")
    #Чтобы события шло дальше на обработку
    await bot.process_commands(message)


bot.run(token=TOKEN)

