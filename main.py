import os
import dotenv
import random

import discord
from discord.ui import Select, View

import calc
import misc


intents = discord.Intents.default()  # Allow the use of custom intents
intents.members = True
dotenv.load_dotenv()
bot = discord.Bot(case_insensitive = True, intents = discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="payout", description="Realize a payout with normal taxes!")
async def payout(
    ctx: discord.ApplicationContext,
    nb: discord.Option(int, description="The number of people to involve in the payout"),
    ammount: discord.Option(float, description="The estimated value of the inventory (put 1000 for 1million and 1 for 1 tousand) "), 
    repair: discord.Option(float, description="The cost of the repair  (put 1000 for 1million and 1 for 1 tousand)")
):
    if nb < 2:
        return await ctx.respond("You must be at least 2 to do a payout !", ephemeral = True)
    
    if ammount < repair:
        return await ctx.respond("Repair costs must be cheaper than the estimated value...", ephemeral = True)
    
    
    members = await getplayers(ctx)
    count = 1

    await participant_view(ctx, nb, ammount, repair, members, count, [str(ctx.author.id)], calc.payout)




@bot.slash_command(name="payout-premium", description="Realize a payout with premium taxes!")
async def payout_premium(
    ctx: discord.ApplicationContext,
    nb: discord.Option(int, description="The number of people to involve in the payout"),
    ammount: discord.Option(float, description="The estimated value of the inventory (put 1000 for 1million and 1 for 1 tousand) "), 
    repair: discord.Option(float, description="The cost of the repair  (put 1000 for 1million and 1 for 1 tousand)")
):
    if nb < 2:
        return await ctx.respond("You must be at least 2 to do a payout !", ephemeral = True)
    
    if ammount < repair:
        return await ctx.respond("Repair costs must be cheaper than the estimated value...", ephemeral = True)
    
    
    members = await getplayers(ctx)
    count = 1

    await participant_view(ctx, nb, ammount, repair, members, count, [str(ctx.author.id)], calc.payout_premium)
    

@bot.slash_command(name="add-player")
async def add_player(
    ctx: discord.ApplicationContext
):
    await ctx.respond("Ping the name of the player you want to add", ephemeral = True)
    while True:
        try:
            message = await bot.wait_for('message',check=check_ping(ctx.author), timeout = 15)
            message = await ctx.fetch_message(message.id)

            tagged = ctx.guild.get_member(int(message.content[2:-1]))
            await tagged.add_roles(await getrole(ctx))
            await ctx.respond("The player has been added to the list 👍", ephemeral = True)
            await message.delete()
            return

        except TimeoutError:
            await ctx.respond("Too late...", ephemeral = True)
            return



async def participant_view(ctx, nb, ammount, repair, members, count, players, payout, messages = []):
        if count >= nb:
            return await embed_payout(ctx, players, payout, ammount, repair)
        
        emojis_animals = "🐵🐻🐼🐭🐮🐯🐰🐱🐲🐳🐴🐶🐷🐸🐹🐺🐑🐗🐘🐙🐛🐜🐝🐞🐠🐡🐢🐣🐥🐌🐍🐎🐒🐔🐩🐫🐧🐬🐿🕷🦁🦄🦃🦀🦂🦇🦊🦌🦍🦏🐀🐁🐂🐃🐄🐅🐆🐇🐈🐉🐊🐋🐏🐐🐓🐕🐖🐤🐨🐪🦆🦛🦡🦢🐟🐦🐽🦅🦈🦉🦎🦓🦒🦔🦕🦗🕊🦝🦜🦚🦧🦮🦥🦨🦦🦩"
        view = View(timeout = 120)
        

        select = Select(
            placeholder = "Select participants...",
            min_values = 1,
            max_values = 1,
            options=[
            discord.SelectOption(label="New participant", emoji="✏", description="Add a participant..."),
        ])
        
        for member in members:
            if str(member.id) not in players:
                select.options.append(
                    discord.SelectOption(
                        label = member.nick if member.nick is not None else member.name, 
                        description = str(member), 
                        emoji = emojis_animals[random.randint(0, len(emojis_animals) - 1)], 
                        value = str(member.id)
                        )
                )
        
        async def callback(interaction):
            await interaction.response.send_message("Please wait...")
            await interaction.delete_original_response()

            if select.values[0] == "New participant":
                await add_player(ctx)
                return await participant_view(ctx, nb, ammount, repair, members, count, players, payout)
            
            else:
                players.append(select.values[0])
                select.disabled = True
                return await participant_view(ctx, nb, ammount, repair, members, count + 1, players, payout) 


        select.callback = callback
        view.add_item(select)

        await ctx.respond(f"Select {misc.ordinal(count)} payout participant :", view = view, ephemeral = True)

        
async def embed_payout(ctx: discord.ApplicationContext, players: list, method, ammout: float, repair: float):
    await ctx.respond(f"Each players will have {method(len(players), ammout, repair)}k silvers.")



    
def check_ping(author):
    def inner_check(message):
        if message.author != author:
            return False

        content = message.content
        if content[0:2] != "<@" or content[-1] != ">":
            return False
        
        return True
    
    return inner_check


async def getplayers(ctx):
    role = await getrole(ctx)
    return [member for member in role.members if not member.bot] 

async def getrole(ctx):
    return discord.utils.get(ctx.guild.roles, name="Albion") or discord.utils.get(ctx.guild.roles, name="albion") or await ctx.guild.create_role(name="Albion") or discord.utils.get(ctx.guild.roles, name="Albion")


bot.run(os.getenv('TOKEN'))