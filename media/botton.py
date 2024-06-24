import discord

from discord.ext import commands


intents = discord.Intents.all()

client = commands.Bot(command_prefix=".", intents=intents)



class Buttons(discord.ui.View):

    def __init__(self, *, timeout=180):

        super().__init__(timeout=timeout)


    @discord.ui.button(label="Button", style=discord.ButtonStyle.gray)

    async def blurple_button(self, button: discord.ui.Button, interaction: discord.Interaction):

        button.style = discord.ButtonStyle.green

        await button.response.edit_message(content=f"This is an edited button response!", view=self)



@client.command()

async def button(ctx):

    await ctx.send("This message has buttons!", view=Buttons())


TOKEN = ""

client.run(TOKEN)