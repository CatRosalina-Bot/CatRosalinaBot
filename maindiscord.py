import discord
import random
from discord.ext import commands
import asyncio
import sys
import aiohttp
from contextlib import redirect_stdout
from discord import app_commands
from discord.ui import Button, View

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix= commands.when_mentioned_or('cr!'), intents=intents)
client.remove_command("help")

@client.event
async def on_ready():
    print("Bot is Online and Ready")
    try:
        synced = await client.tree.sync()
        print(f"{len(synced)} Slash Commands successfully Synced")
    except Exception as e:
        print(e)



@client.command()
async def help(ctx):
    embed = discord.Embed(title="Rosalina Bot", description="Here are my commands", color=(49407))
    embed.add_field(name="CORE COMMANDS", value="cr!help - This message\ncr!ping - Checks my latency\ncr!botinfo - Get information about the bot", inline=False)
    embed.add_field(name="STATS COMMANDS", value="cr!serverinfo - Get information about your server\ncr!userinfo - Get information about a user.\ncr!emojiinfo - Get information about an emoji\ncr!membercount - Check how many members your server has\ncr!userstatus - See the Status of a user", inline=False)
    embed.add_field(name="UTILITY COMMANDS", value="cr!say\ncr!esay\ncr!useravatar - Get an enlarged image of a users avatar", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.send(f'My current latency is: {round(client.latency * 1000)}ms')

@client.command()
async def botinfo(ctx):
    embed = discord.Embed(title="Rosalina Bot", description="Here are my stats and information", color=(49407))
    embed.add_field(name="STATS", value="Servers used in: {len(client.guilds)}", inline=False)
    embed.add_field(name="LINKS", value="Invite the bot: https://discord.com/api/oauth2/authorize?client_id=1048877757226029086&permissions=0&scope=bot%20applications.commands\nSupport Server: https://discord.gg/zxxVhA5vXp\nWebsite: https://erisdevelopment.glitch.me/rosalinabot.html", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def serverinfo(ctx):
    format = "%a, %b %d %Y | %H:%M:%S %ZGMT"   
    nonbots = [user for user in ctx.guild.members if user.bot == False]
    embed = discord.Embed(title="SERVER INFORMATION", description="Here is some Information about this server", color=(49407))
    embed.add_field(name="Basic Information", value=f"Guild Name: {ctx.guild.name}\nMember Count: {ctx.guild.member_count}\nHumans Count: {len(nonbots)}\nGuild ID: {ctx.guild.id}\nServer Owner: {ctx.guild.owner}\nVerification Level: {ctx.guild.verification_level}\nServer Creation Date: {ctx.guild.created_at.strftime(format)}", inline=False)
    embed.add_field(name="Features", value=f"{', '.join(f'**{x}**' for x in ctx.guild.features)} \nSplash: {ctx.guild.splash}", inline=False)
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    categories = len(ctx.guild.categories)
    channels = text_channels + voice_channels
    embed.add_field(name="Channel Count", value=f"Categories; **{categories}**\nText Channels; **{text_channels}**\nVoice Channels; **{voice_channels}**\nTotal Channels: **{channels}**", inline=False)
    embed.set_thumbnail(url=ctx.guild.icon)
    await ctx.send(embed=embed)

@client.command()
async def userinfo(ctx, *, user: discord.Member = None):
    if user is None:
        user = ctx.author
    date_format = "%a, %b %d %Y %I:%M %p"
    embed = discord.Embed(title="USER INFORMATION/STATS", description=f"Here is some Information about this user", color=(49407))
    embed.add_field(name="BASIC INFO", value=f"USERNAME+DISCRIMINATOR: {user.name}#{user.discriminator}\nUSER ID: {user.id}\nRegistered at: {user.created_at.strftime(date_format)}", inline=False)
    embed.add_field(name="SERVER BASED INFO", value=f"Joined Server at: {user.joined_at.strftime(date_format)}", inline=False)
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="ROLES [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="USER PERMISSIONS FOR SERVER", value=perm_string, inline=False)
    embed.set_thumbnail(url=user.avatar)
    await ctx.send(embed=embed)

@client.command()
async def useravatar(ctx, *, user: discord.Member = None):
    if user is None:
        user = ctx.author
    embed = discord.Embed(description=f"{user.mention} Avatar", color=(49407))
    embed.set_image(url=user.avatar)
    await ctx.send(embed=embed)

@client.command()
async def membercount(ctx):
    nonbots = [user for user in ctx.guild.members if user.bot == False]
    embed = discord.Embed(title="Member Count", description=f"Humans: {len(nonbots)}\nTotal Members: {ctx.guild.member_count}", color=(49407))
    await ctx.send(embed=embed)

@client.command()
async def emojiinfo(ctx, emoji: discord.Emoji):
    embed = discord.Embed(title="Emoji Information", description=f"Emoji Name: {emoji.name}\nEmoji ID: {emoji.id}", color=(49407))
    await ctx.send(embed=embed)

@emojiinfo.error
async def emojiinfo_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("What emoji do you want to get information about?")
    else:
        raise error

@client.command()
async def say(ctx, *, question: commands.clean_content):
    await ctx.send(f'{question}')
    await ctx.message.delete()

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("What do you want me to say?")
    else:
        raise error

@client.command()
async def esay(ctx, *, question):
    embed = discord.Embed(description=f'{question}', color=(49407))
    await ctx.send(embed=embed)
    await ctx.message.delete()

@esay.error
async def esay_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("What do you want me to say?")
    else:
        raise error



@client.tree.command(name="serverinfo", description='See information about your server.')
async def _serverinfo(interaction: discord.Interaction):
    format = "%a, %b %d %Y | %H:%M:%S %ZGMT"   
    nonbots = [user for user in interaction.guild.members if user.bot == False]
    embed = discord.Embed(title="SERVER INFORMATION", description="Here is some Information about this server", color=(49407))
    embed.add_field(name="Basic Information", value=f"Guild Name: {interaction.guild.name}\nMember Count: {interaction.guild.member_count}\nHumans Count: {len(nonbots)}\nGuild ID: {interaction.guild.id}\nServer Owner: {interaction.guild.owner}\nVerification Level: {interaction.guild.verification_level}\nServer Creation Date: {interaction.guild.created_at.strftime(format)}", inline=False)
    embed.add_field(name="Features", value=f"{', '.join(f'**{x}**' for x in interaction.guild.features)} \nSplash: {interaction.guild.splash}", inline=False)
    text_channels = len(interaction.guild.text_channels)
    voice_channels = len(interaction.guild.voice_channels)
    categories = len(interaction.guild.categories)
    channels = text_channels + voice_channels
    embed.add_field(name="Channel Count", value=f"Categories; **{categories}**\nText Channels; **{text_channels}**\nVoice Channels; **{voice_channels}**\nTotal Channels: **{channels}**", inline=False)
    embed.set_thumbnail(url=interaction.guild.icon)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="userinfo", description='See information about a user')
async def _userinfo(interaction: discord.Interaction, user: discord.Member = None):
    if user is None:
        user = interaction.author
    date_format = "%a, %b %d %Y %I:%M %p"
    embed = discord.Embed(title="USER INFORMATION/STATS", description=f"Here is some Information about this user", color=(49407))
    embed.add_field(name="BASIC INFO", value=f"USERNAME+DISCRIMINATOR: {user.name}#{user.discriminator}\nUSER ID: {user.id}\nRegistered at: {user.created_at.strftime(date_format)}", inline=False)
    embed.add_field(name="SERVER BASED INFO", value=f"Joined Server at: {user.joined_at.strftime(date_format)}", inline=False)
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="ROLES [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="USER PERMISSIONS FOR SERVER", value=perm_string, inline=False)
    embed.set_thumbnail(url=user.avatar)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="useravatar", description='Get an Enlarged image of a users avatar')
async def _useravatar(interaction: discord.Interaction, user: discord.Member = None):
    if user is None:
        user = interaction.author
    embed = discord.Embed(description=f"{user.mention} Avatar", color=(49407))
    embed.set_image(url=user.avatar)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="membercount", description='See Human and Member Count')
async def _membercount(interaction: discord.Interaction):
    nonbots = [user for user in interaction.guild.members if user.bot == False]
    embed = discord.Embed(title="Member Count", description=f"Humans: {len(nonbots)}\nTotal Members: {interaction.guild.member_count}", color=(49407))
    await interaction.response.send_message(embed=embed)



client.run("DISCORDBOTTOKEN")
