import discord, asyncio, fourline, tictactoe, ttcIA
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.all() 
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=["TR-", "tr-"], intents=intents)

#Inicial Status
@bot.event
async def on_ready():
	guild_count = 0

	for guild in bot.guilds:
		print(f"- {guild.id} (name: {guild.name})")
		guild_count = guild_count + 1

	print("Tubérculosauros-Rex is in " + str(guild_count) + " server(s).")

#Jogo da Velha
#----------------------------------------------------------------------------------------------------------------------
bot.add_command(tictactoe.tictactoe)
bot.add_command(tictactoe.place)
#----------------------------------------------------------------------------------------------------------------------

#Jogo da Velha vs IA
#----------------------------------------------------------------------------------------------------------------------
bot.add_command(ttcIA.joga)
#----------------------------------------------------------------------------------------------------------------------

#4 Em Linha
#----------------------------------------------------------------------------------------------------------------------
bot.add_command(fourline.fourline)
bot.add_command(fourline.column) 
#----------------------------------------------------------------------------------------------------------------------

bot.run("Token")