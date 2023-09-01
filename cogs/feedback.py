import discord, time, datetime
from discord.ext import commands
from dislash import slash_commands, Option, OptionChoice, Type

prefix = "?"

Bot = commands.Bot(command_prefix=prefix, help_command=None)
slash = slash_commands.SlashClient(Bot)


class Feedback(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @slash.command(
        name="feedback",
        description="Use this command to communicate with the developer!",
        options=[
            Option("message", "Whatever you want to say!", Type.STRING, True),
            Option("feedback_type",
                   "Type of your feedback!",
                   Type.STRING,
                   choices=[
                       OptionChoice("Feedback", "Feedback"),
                       OptionChoice("Bug Report", "Bug Report"),
                       OptionChoice("Feature Advice", "Feature Advice")
                   ])
        ])
    async def feedback(self, inter, message, feedback_type: str = "Feedback"):
        feedback_text = f'Username: "{inter.author.name}#{inter.author.discriminator}", ID:"{inter.author.id}"\nFeedback Type: "{feedback_type}", Feedback Date:f"{time.time()}"\nFeedback: "{message}"\n\n'

        feedback_file = open("feedbacks.txt", "a")
        feedback_file.write(feedback_text)
        feedback_file.close()

        feedback_embed = discord.Embed(
            title="Success",
            description=f"**Your {feedback_type} delivered successfully!**",
            color=discord.Color.from_rgb(63, 231, 255),
            timestamp=datetime.datetime.utcnow())
        feedback_embed.set_footer(text="Requested in")
        feedback_embed.set_author(
            name=f"{inter.author.name}#{inter.author.discriminator}",
            icon_url=inter.author.avatar_url)
        await inter.reply(embed=feedback_embed)


def setup(Bot):
    Bot.add_cog(Feedback(Bot))
