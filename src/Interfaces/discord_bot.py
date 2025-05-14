import json
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv  # Import dotenv
from ..Core.dice_rolling import roll_dice_details
from fastapi.encoders import jsonable_encoder  # Import jsonable_encoder
import os
import statistics

# Load environment variables from the .env file
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN is not set in the environment or .env file.")

intents = discord.Intents.default()
intents.messages = True  # Enable message reading intent
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# @bot.tree.command(name="roll")
# @app_commands.describe(
#     sides="The number of sides on the dice (required).",
#     num_dice="The number of dice to roll (default is 1).",
#     modifier="A modifier to add to the total roll (default is 0)."
# )
async def roll(interaction: discord.Interaction, sides: int, num_dice: int = 1, modifier: int = 0):
    """
    Rolls dice based on the provided parameters and sends the result.
    """
    if sides < 1 or num_dice < 1:
        await interaction.response.send_message("Number of sides and dice must be at least 1.", ephemeral=True)
        return

    result = roll_dice_details(num_dice, sides, modifier)
    rolls = ", ".join(map(str, result["rolls"]))
    total = result["total"]
    modifier = result["modifier"]

    await interaction.response.send_message(
        f"🎲 You rolled: {rolls}\nModifier: {modifier}\n**Total: {total}**"
    )

# @bot.tree.command(name="analyze")
# @app_commands.describe(
#     roll_type="The roll type to search for (e.g., 'd1000')."
# )
async def analyze(interaction: discord.Interaction, roll_type: str):
    """
    Analyzes previous messages for a specific roll type and calculates statistics.
    """
    if not roll_type.startswith("d"):
        print(f"Invalid roll type provided: {roll_type}")
        await interaction.response.send_message("Please provide a valid roll type (e.g., 'd20').", ephemeral=True)
        return

    print(f"Starting analysis for roll type: {roll_type}")
    await interaction.response.defer()  # Defer response to allow time for processing

    channel = interaction.channel
    if not channel:
        print("Channel is not accessible.")
        await interaction.followup.send("Unable to access the channel.", ephemeral=True)
        return

    results = []
    async for message in channel.history(limit=50):  # Adjust limit as needed
        print(f"Checking message: {message.interaction_metadata}")
        print(f"Message author: {message.author.name}")
        print(f"Message timestamp: {message.created_at}")
        print(f"we")
        if roll_type in message.content or f"1{roll_type}" in message.content:
            try:
                # Extract the number after "Result: "
                result_str = message.content.split("Result: ")[1].split()[0]
                print(f"Found result: {result_str}")
                results.append(int(result_str))
            except (IndexError, ValueError) as e:
                print(f"Error parsing message: {message.content}, Error: {e}")
                continue

    if not results:
        print(f"No results found for roll type: {roll_type}")
        await interaction.followup.send(f"No results found for roll type '{roll_type}'.", ephemeral=True)
        return

    print(f"Results collected: {results}")
    avg = sum(results) / len(results)
    mean = statistics.mean(results)
    try:
        mode = statistics.mode(results)
    except statistics.StatisticsError:
        mode = "No unique mode"

    print(f"Analysis complete. Average: {avg}, Mean: {mean}, Mode: {mode}")
    await interaction.followup.send(
        f"📊 Analysis for roll type '{roll_type}':\n"
        f"Average: {avg:.2f}\n"
        f"Mean: {mean:.2f}\n"
        f"Mode: {mode}"
    )

bot.run(DISCORD_TOKEN)

