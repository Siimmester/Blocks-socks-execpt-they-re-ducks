from mojangApi import get_skin
import tokens
import discord
from discord.ext import commands
import requests
import io
import os
from PIL import Image

client = commands.Bot(command_prefix='$', intents=discord.Intents.all())


# once the bot boots up, it will print in to the console and the bot will start playing the game "/socks + ign for cool
# skin"
@client.event
async def on_ready():
    await client.tree.sync()
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Game("/socks + ign for cool skin :D"))


@client.tree.command(name="socks", description='Get yourself a cool pair of socks on your minecraft skin')
async def socks(interaction: discord.Interaction, ign: str):
    await interaction.response.send_message(f"Your skin is being generated... ETA: 2s ")

    src_image = Image.open("duck_socks_sorce.png")

    profile = get_skin(ign)
    url = profile[0]
    skin_mode = profile[1]
    response = requests.get(url)
    dst_image = Image.open(io.BytesIO(response.content))

    if not dst_image.size == (64, 64):
        await interaction.channel.send("Your skin is not 64x64 resolution")
    elif skin_mode == 0:
        await interaction.channel.send("No user by that name")
    else:

        four_rectangles = [[8, 16, 12, 20],
                           [0, 26, 16, 32],
                           [24, 48, 28, 52],
                           [15, 58, 32, 64]]

        for i, rectangle in enumerate(four_rectangles):
            left = rectangle[0]
            top = rectangle[1]
            right = rectangle[2]
            bottom = rectangle[3]

            pixels = src_image.crop((left, top, right, bottom))
            dst_image.paste(pixels, (left, top))
        dst_image.save("modified_image.png")
        await interaction.channel.send(file=discord.File("modified_image.png"))
        os.remove("modified_image.png")


client.run(tokens.discord_token)
