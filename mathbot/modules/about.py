import datetime
import discord
import psutil
import os
import asyncio
import aiohttp
import datetime
import core.help
from discord.ext import commands



BOT_COLOUR = 0x19BAE5
STARTUP_TIME = datetime.datetime.now()


STATS_MESSAGE = """\
Servers: {}
Uptime: {} days {} hours {} minutes {} seconds
"""


core.help.load_from_file('./help/help.md', topics = [''])
core.help.load_from_file('./help/about.md')
core.help.load_from_file('./help/management.md')
core.help.load_from_file('./help/commands.md')


async def get_bot_total_servers(id):
	async with aiohttp.ClientSession() as session:
		url = 'https://discordbots.org/api/bots/{}/stats'.format(id)
		async with session.get(url) as response:
			jdata = await response.json()
			return jdata.get('server_count')


class AboutModule(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot
		print('About module loaded')

	# Send a message detailing the shard number, server count,
	# uptime and and memory using of this shard
	@commands.command()
	async def stats(self, ctx: commands.Context[commands.Bot]):
		embed = discord.Embed(title='MathBot Stats', colour=BOT_COLOUR)
		embed.add_field(
			name='Total Servers',
			# MathBot's ID, hard coded for proper testing.
			value=await get_bot_total_servers('134073775925886976'),
			inline=True
		)
		embed.add_field(
			name='Visible Servers',
			value=len(ctx.bot.guilds),
			inline=True
		)
		embed.add_field(
			name='Shard IDs',
			value=', '.join([str(i + 1) for i in ctx.bot.shard_ids]),
			inline=True
		)
		embed.add_field(
			name='Uptime',
			value=get_uptime(),
			inline=True
		)
		embed.add_field(
			name='Memory Usage',
			value='{} MB'.format(get_memory_usage()),
			inline=True
		)
		embed.set_footer(text='Time is in hh:mm')
		await ctx.send(embed=embed)

	@commands.command()
	async def ping(self, ctx: commands.Context[commands.Bot]):
		await ctx.send(f'Pong! Latency {ctx.bot.latency}.')

	# Aliases for the help command
	@commands.command()
	async def about(self, ctx: commands.Context[commands.Bot]):
		cmd = ctx.bot.get_command('help')
		await ctx.invoke(cmd, topic='about')

	@commands.command()
	@commands.is_owner()
	async def sync(self, ctx: commands.Context[commands.Bot]):
		msg = await ctx.send('Syncing commands...')
		await ctx.bot.tree.sync()
		await msg.edit(content='Synced commands!')


def get_uptime():
	''' Returns a string representing how long the bot has been running for '''
	cur_time = datetime.datetime.now()
	up_time = cur_time - STARTUP_TIME
	up_hours = up_time.seconds // (60 * 60) + (up_time.days * 24)
	up_minutes = (up_time.seconds // 60) % 60
	return '{:02d}:{:02d}'.format(up_hours, up_minutes)


def get_memory_usage():
	''' Returns the amount of memory the bot is using, in MB '''
	proc = psutil.Process(os.getpid())
	mem = proc.memory_info().rss
	return mem // (1024 * 1024)


async def setup(bot: commands.Bot):
	await bot.add_cog(AboutModule(bot))
