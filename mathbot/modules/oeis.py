import aiohttp
from discord.ext import commands
from core.settings import command_allowed
import core
from utils import run_typing

core.help.load_from_file('./help/oeis.md')

class OEIS(commands.Cog):

	@commands.hybrid_command()
	@command_allowed('c-oeis')
	async def oeis(self, ctx, *, query=''):
		'''Search the Online Encyclopedia of Integer Sequences.
		
		Arguments:
			query: The sequence to search for, for example, `1, 1, 2, 3, 5` or `fibonacci sequence`.
		'''
		if query == '':
			await ctx.send(f'The `{ctx.prefix}oeis` command is used to query the Online Encyclopedia of Integer Sequences. See `{ctx.prefix}help oeis` for details.')
			return
		await run_typing(ctx, self.send_oeis_data(ctx, query))

	async def send_oeis_data(self, ctx: commands.Context[commands.Bot], query: str):
		async with aiohttp.ClientSession() as session:
			params = {
				'q': query,
				'start': 0,
				'fmt': 'json'
			}
			async with session.get('https://oeis.org/search', params=params, timeout=10) as req:
				j = await req.json()
				# print(json.dumps(j, indent=4))
				count = j.get('count', 0)
				res = j.get('results', None)
				if count == 0:
					await ctx.send('No sequences were found.')
				elif res is None:
					await ctx.send(f'There are {count} relevant sequences. Please be more specific.')
				else:
					name = res[0]['name']
					number = res[0]['number']
					digits = res[0]['data'].replace(',', ', ').strip()
					match_text = (
						f'There were {count} relevant sequences. Here is one:'
						if count > 1
						else 'There was 1 relevant sequence:'
					)
					m = f'{match_text}\n\n**{name}**\nhttps://oeis.org/A{number}\n\n{digits}\n'
					await ctx.send(m)


async def setup(bot: commands.Bot):
	await bot.add_cog(OEIS())
