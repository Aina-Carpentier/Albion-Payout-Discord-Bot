import os
import dotenv
import discord
import payout

dotenv.load_dotenv()
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="payout", description="Réalise un payout !")
async def payout(ctx: discord.ApplicationContext):
    await ctx.respond("Hey!")

bot.run(os.getenv('TOKEN'))