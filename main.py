import os
import dotenv
import discord
import calc
import random
from discord.ui import Select, View


intents = discord.Intents.default()  # Allow the use of custom intents
intents.members = True
dotenv.load_dotenv()
bot = discord.Bot(case_insensitive = True, intents = intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="payout", description="Réalise un payout !")
async def payout(
    ctx: discord.ApplicationContext,
    nb: discord.Option(int, description="The number of people to involve in the"),
    ammount: discord.Option(float, description="The estimated value of the inventory."), 
    repair: discord.Option(float, description="The cost of the repair.")
):
    members = await getplayers(ctx)
    emojis_animals = "🐵🐻🐼🐭🐮🐯🐰🐱🐲🐳🐴🐶🐷🐸🐹🐺🐑🐗🐘🐙🐛🐜🐝🐞🐠🐡🐢🐣🐥🐌🐍🐎🐒🐔🐩🐫🐧🐬🐿🕷🦁🦄🦃🦀🦂🦇🦊🦌🦍🦏🐀🐁🐂🐃🐄🐅🐆🐇🐈🐉🐊🐋🐏🐐🐓🐕🐖🐤🐨🐪🦆🦛🦡🦢🐟🐦🐽🦅🦈🦉🦎🦓🦒🦔🦕🦗🕊🦝🦜🦚🦧🦮🐕‍🦺🦥🦨🦦🦩"

    select = Select(
        placeholder = "Select participants...",
        min_values = nb - 1,
        max_values = nb - 1,
        options=[
        discord.SelectOption(label="Nouveau participant", emoji="✏", description="Ajouter un participant..."),
    ]) ##disable ?
    
    for member in members:
        print(member)
        select.options.append(
            discord.SelectOption(label = member.nick if member.nick is not None else member.name, description=str(member))
        )
    
    view = View()
    view.add_item(select)

    await ctx.respond("Select payout participants :",view=view)



@bot.slash_command(name="payout-premium", description="Réalise un payout avec le premium!")
async def payout_premium(
    ctx: discord.ApplicationContext,
    nb: discord.Option(int, description="The number of people to involve in the"),
    ammount: discord.Option(float, description="The estimated value of the inventory."),
    repair: discord.Option(float, description="The cost of the repair.")
):
    await ctx.respond(getplayers(ctx))
    await ctx.respond(str(calc.payout_premium(nb, ammount, repair)))



async def getplayers(ctx):
    if discord.utils.get(ctx.guild.roles, name="Albion") is None and discord.utils.get(ctx.guild.roles, name="albion") is None:
        await ctx.guild.create_role(name="Albion")
    role = discord.utils.get(ctx.guild.roles, name="Albion") if discord.utils.get(ctx.guild.roles, name="Albion") is not None else discord.utils.get(ctx.guild.roles, name="albion") 
    
    return [member for member in role.members if not member.bot] 


bot.run(os.getenv('TOKEN'))