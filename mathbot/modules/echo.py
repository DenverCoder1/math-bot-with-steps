# Has a command which echoes whatever text was given to it.
# Used only for testing purposes.

from discord.ext import commands




class EchoModule(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def echo(self, context, *, text: str):
		await context.send(text)


async def setup(bot: commands.Bot):
	await bot.add_cog(EchoModule(bot))
