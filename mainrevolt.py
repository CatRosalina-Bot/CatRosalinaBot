import voltage
from voltage.ext import commands
import random
import asyncio
import aiohttp
import requests

client = commands.CommandsClient("cr!")

@client.command(description="Get information about the bot")
async def botinfo(ctx):
    embed = discord.Embed(title="Cat Rosalina Bot", description="Servers used in: {len(client.servers)}\nInvite the bot: https://app.revolt.chat/bot/01GX4YZD7NZ73PSS4XVQZBPVF7\nSupport Server: https://rvlt.gg/cj0efsy8\nWebsite: https://erisdevelopment.glitch.me/rosalinabot.html\nSource Code: https://github.com/CatRosalina-Bot/CatRosalinaBot", color="#00C0FF")
    await ctx.send(embed=embed)

@client.command(description="Get information about your server")
async def serverinfo(ctx):
    embed = voltage.SendableEmbed(title="Server Information", description=f"Guild Name: {ctx.server.name}\nGuild ID: {ctx.server.id}\nServer Owner: {ctx.server.owner.name} (`{ctx.server.owner.id}`)\nServer Creation Date: {ctx.server.created_at}\n\nServer Description: {ctx.server.description}", media=ctx.server.icon, color="#00C0FF")
    await ctx.send(embed=embed)

@client.command(description="Get information about a user")
async def userinfo(ctx, member: voltage.Member = None):
    if member is None:
        member = ctx.author
    embed = voltage.SendableEmbed(title="User Information", description=f"USERNAME: {member.name}\nUSER ID: {member.id}\nRoles: {member.roles}", icon_url=member.display_avatar.url, color='#00C0FF')
    await ctx.send(embed=embed)

@client.command(description="Get an enlarged image of a users avatar")
async def useravatar(ctx, member: voltage.User = None):
    if member is None:
        member = ctx.author
    embed = voltage.SendableEmbed(title=f"{member.name} Avatar", media=member.display_avatar.url, color='#00C0FF')
    await ctx.send(embed=embed)

@client.command(description="Have me say whatever you want")
async def say(ctx, *, question):
    await ctx.send(f'{question}')
    await ctx.message.delete()

@client.command(description="Have me say whatever you want in an embed")
async def esay(ctx, *, question):
    embed = voltage.SendableEmbed(description=f'{question}', color="#00C0FF")
    await ctx.send(embed=embed)
    await ctx.message.delete()



client.run("REVOLTBOTTOKEN")
