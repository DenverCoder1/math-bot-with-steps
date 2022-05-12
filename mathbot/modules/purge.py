import core.help
import discord
import asyncio




from discord.ext import commands

USER_PERM_ERROR = '''\
You do not have the permissions required to perform that operation in this channel.
You need to have permission to *manage messages*.
'''

PRIVATE_ERROR = '''\
The `=purge` command cannot be used in a private channel.
See `=help purge` for more details.
'''

core.help.load_from_file('./help/purge.md')

class PurgeModule(commands.Cog):
	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(manage_messages=True)
	async def purge(self, ctx, number: int):
		if number > 0:
			number = min(200, number)
			async for message in ctx.channel.history(limit=200):
				if message.author.id == ctx.bot.user.id and number > 0:
					try:
						await message.delete()
						number -= 1
					except discord.errors.NotFound:
						pass
					await asyncio.sleep(1)

async def setup(bot: commands.Bot):
	await bot.add_cog(PurgeModule())
