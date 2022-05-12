from discord.ext import commands



class ThrowsModule(commands.Cog):

	@commands.command()
	async def throw(self, context):
		raise Exception('I wonder what went wrong?')

async def setup(bot: commands.Bot):
	await bot.add_cog(ThrowsModule())
