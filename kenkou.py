import asyncio
from discord.ext import commands
import discord
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
CH_ID = 1261862110892396604

# Format of Profiles:
#  {
#      "name": "John Doe",
#      "Calories Burned Today": 0
#  }

with open ('passkey.txt', 'r') as f:
    BOT_TOKEN = f.read().strip()

print(BOT_TOKEN)
    
with open('ListProf.json') as f:
    profiles = json.load(f)

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

bot = commands.Bot(command_prefix= "k!", intents=discord.Intents.all())
session = Session()

@bot.event
async def on_ready():
    print("Hello! The bot is ready!")
    channel = bot.get_channel(CH_ID)
    await channel.send("Hello! Bot is ready!")
    
@bot.command()
async def addProf(ctx, name):
    author = ctx.message.author
    if any(profile["name"] == name for profile in profiles):
        await ctx.send("Profile already exists!")
    else:
        profile = {
            "name": name,
            "Calories Burned Today": 0
        }
        profiles.append(profile)
        with open('ListProf.json', 'w') as f:
            json.dump(profiles, f)
        await ctx.send(f"Profile created for {name}!")
    
@bot.command()
async def profile(ctx, name):
    author = ctx.message.author
    for profile in profiles:
        if profile["name"] == name:
            await ctx.send(f"Name: {profile['name']}\nCalories Burned Today: {profile['Calories Burned Today']}")
            return
        else:
            await ctx.send("Profile not found!")
            
@bot.command()
async def addCal(ctx, name, cal):
    author = ctx.message.author
    for profile in profiles:
        if profile["name"] == name:
            profile["Calories Burned Today"] += int(cal)
            with open('ListProf.json', 'w') as f:
                json.dump(profiles, f)
            await ctx.send(f"Calories added to {name}!")
            return
    await ctx.send("Profile not found!")
    
@bot.command()
async def resetCal(ctx, name):
    author = ctx.message.author
    for profile in profiles:
        if profile["name"] == name:
            profile["Calories Burned Today"] = 0
            with open('ListProf.json', 'w') as f:
                json.dump(profiles, f)
            await ctx.send(f"Calories reset for {name}!")
            return
    await ctx.send("Profile not found!")
    
@bot.command()
async def hello(ctx):
    await ctx.send("Yo yo!")
    
@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("Session is already active!")
        return
    
    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    PST_time = ctx.message.created_at - timedelta(hours=7)
    human_time = PST_time.strftime("%H:%M")
    await ctx.send(f"Workout session started at {human_time}")
    
@bot.command()
async def stop(ctx):
    if not session.is_active:
        await ctx.send("Session is not active!")
        return
    
    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    # human_readable_dur = str(timedelta(seconds=duration))
    human_readable_dur = str(timedelta(seconds=duration)).split(".")[0]
    await ctx.send(f"Workout session stopped! Duration: {human_readable_dur}.")
    
@bot.command()
async def tabata(ctx, on, off, rounds):
    if session.is_active:
        await ctx.send("Session is already active!")
        return
    
    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    PST_time = ctx.message.created_at - timedelta(hours=7)
    human_time = PST_time.strftime("%H:%M")
    await ctx.send(f"Tabata session started at {human_time}")
    
    for i in range(int(rounds)):
        await ctx.send(f"Round {i+1}: Work!")
        await asyncio.sleep(int(on))
        await ctx.send(f"Round {i+1}: Rest!")
        await asyncio.sleep(int(off))
    
    session.is_active = False
    await ctx.send(f"Tabata session stopped!")

bot.run(BOT_TOKEN)

