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
bot = discord.Bot(case_insensitive = True, intents = intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="payout", description="Realize a payout with normal taxes!")
async def payout(
    ctx: discord.ApplicationContext,
    nb: discord.Option(int, description="The number of people to involve in the"),
    ammount: discord.Option(float, description="The estimated value of the inventory."), 
    repair: discord.Option(float, description="The cost of the repair.")
):

    view = View()

    members = await getplayers(ctx)
    emojis_animals = "🐵🐻🐼🐭🐮🐯🐰🐱🐲🐳🐴🐶🐷🐸🐹🐺🐑🐗🐘🐙🐛🐜🐝🐞🐠🐡🐢🐣🐥🐌🐍🐎🐒🐔🐩🐫🐧🐬🐿🕷🦁🦄🦃🦀🦂🦇🦊🦌🦍🦏🐀🐁🐂🐃🐄🐅🐆🐇🐈🐉🐊🐋🐏🐐🐓🐕🐖🐤🐨🐪🦆🦛🦡🦢🐟🐦🐽🦅🦈🦉🦎🦓🦒🦔🦕🦗🕊🦝🦜🦚🦧🦮🦥🦨🦦🦩"
    count = 1

    async def create_view(count, selected = [], messages = []):
        if count >= nb:
            return
        
        view = View()

        select = Select(
            placeholder = "Select participants...",
            min_values = 1,
            max_values = 1,
            options=[
            discord.SelectOption(label="New participant", emoji="✏", description="Add a participant..."),
        ])
        
        for member in members:
            if str(member.id) not in selected:
                select.options.append(
                    discord.SelectOption(
                        label = member.nick if member.nick is not None else member.name, 
                        description=str(member), 
                        emoji = emojis_animals[random.randint(0,len(emojis_animals)-1)], 
                        value = str(member.id)
                        )
                )
        
        async def callback(interaction):
            await interaction.response.send_message("Please wait...")
            await interaction.delete_original_response()
            if select.values[0] == "New participant":
                await add_player(ctx)
                return await create_view(count, selected)
            else:
                selected.append(select.values[0])
                select.disabled = True
                return await create_view(count + 1, selected) 


        select.callback = callback
        view.add_item(select)

        await ctx.respond(f"Select {misc.ordinal(count)} payout participant :", view = view, ephemeral = True)

    await create_view(count)


@bot.slash_command(name="payout-premium", description="Realize a payout with premium taxes!")
async def payout_premium(
    ctx: discord.ApplicationContext,
    nb: discord.Option(int, description="The number of people to involve in the"),
    ammount: discord.Option(float, description="The estimated value of the inventory."),
    repair: discord.Option(float, description="The cost of the repair.")
):
    await ctx.respond(getplayers(ctx))
    await ctx.respond(str(calc.payout_premium(nb, ammount, repair)))

@bot.slash_command(name="add-player")
async def add_player(
    ctx: discord.ApplicationContext
):
    await ctx.respond("Ping the name of the player you want to add", ephemeral = True)
    while True:
        try:
            message = await bot.wait_for('message', timeout = 15)
            message = await ctx.fetch_message(message.id)

            tagged = ctx.guild.get_member(int(message.content[2:-1]))
            await tagged.add_roles(await getrole(ctx))
            await ctx.respond("The player has been added to the list 👍", ephemeral = True)
            await message.delete()
            return

        except TimeoutError:
            await ctx.respond("Too late...", ephemeral = True)
            return



        
        

    
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