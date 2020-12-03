import discord
import json
from discord.ext import commands, tasks
import random
import os
from itertools import cycle


#if you are using the below 'client' then you have name your decorator client. Eg: @client.event
#if you are using the variable bot in below then you hae to name your decorator @bot.event
client = commands.Bot(command_prefix=".")
status = cycle(['Status 1', 'Status 2'])

@client.event
async def on_ready():
    print("Bot is ready!")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used.')

@client.command()
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete')

@client.event
async def status():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Hello there!'))

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_member_join(member,ctx):
    await ctx.send(f'{member} has joined the server.')


#test the paratheses if it is private or public 
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def users(ctx, member):
    await ctx.send(f'Members: {member.count}')

@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
@commands.has_permissions(manage_messages=True)
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason=reason)

@client.command()
@commands.has_permissions(manage_messages=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.name}#{member.mention}')

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

#use this command if you want specifc person to access it

# def is_it_me(ctx):
#     return ctx.author.id == #id of the user 

# @client.command()
# @commands.check(is_it_me)
# async def example(ctx):
#     await ctx.send(f'Hi i am {ctx.author}')

@client.event
async def on_member_update(before, after, message):
    if message.content == "!online":
        if str(before.status) == "online":
            if str(after.status) == "offline":
                print("{} has gone {}.".format(after.name, after.status))

@client.command(alias=["help"])
async def displayembed(ctx):
        embed = discord.Embed(title="Commands on SuperBot", description="Some usedful commands", color=discord.Color.light_blue())
        embed.set_footer(text="This is a footer")
        embed.add_field(name=".ping", value="Shows your ping")
        embed.add_field(name=".8ball", value="Its a game, Just type .8ball and your question on the same line")
        embed.add_field(name=".clear", value="Clears messages")
        embed.add_field(name=".ban", value="It bans a specfic user. Only works when used by the owner")
        embed.add_field(name=".kick", value="It kicks the user. Only works when used by the owner")
        # await client.say(embed=embed)

@client.command(alias=['user','info'])
@commands.has_permissions(kick_members=True)
async def whois(ctx, member : discord.Member):
    embed = discord.Embed(title=member.name, description=member.mention, color=discord.Color.blue())
    embed.add_field(name="ID", value=member.id, inline=True)
    await ctx.send(embed=embed)

client.run("NzgzMzA3MzI3MTU5MTQwMzcz.X8Y1yw.pCR1tyzk19sLlEOwA_E1PCXie8g")