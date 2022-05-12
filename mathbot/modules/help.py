''' Module used to send help documents to users. '''

import core.help
import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands



SERVER_LINK = 'https://discord.gg/fPrdqh3Zfu'
PREFIX_MEMORY_EXPIRE = 60 * 60 * 24 * 3 # 3 days


def doubleformat(string, **replacements):
	''' Acts a but like format, but works on things wrapped in *two* curly braces. '''
	for key, value in replacements.items():
		string = string.replace('{{' + key + '}}', value)
	return string


class HelpModule(commands.Cog):
	''' Module that serves help pages. '''

	@commands.command()
	async def support(self, ctx: commands.Context[commands.Bot]):
		await ctx.send(f'Mathbot support server: {SERVER_LINK}')

	@commands.command()
	async def invite(self, ctx: commands.Context[commands.Bot]):
		await ctx.send('Add mathbot to your server: https://denvercoder1.github.io/math-bot-with-steps/add.html')

	@commands.hybrid_command()
	@app_commands.choices(topic=[Choice(name=topic, value=topic) for topic in core.help.listing()])
	async def help(self, ctx: commands.Context[commands.Bot], *, topic='help'):
		''' Help command itself.
			Help is sent via DM, but a small message is also sent in the public chat.
			Specifying a non-existent topic will show an error and display a list
			of topics that the user could have meant.

			Arguments:
				topic: The topic to get help with.
		'''
		if topic in ['topics', 'topic', 'list']:
			return await self._send_topic_list(ctx)

		found_doc = core.help.get(topic)
		if found_doc is None:
			await ctx.send(self._suggest_topics(topic))
			return

		# Display the default prefix if the user is in DMs and uses no prefix.
		prefix = ctx.prefix if ctx.prefix and ctx.prefix != '/' else '='

		print(prefix, ctx.bot.user.id)
		if prefix.strip() in [f'<@{ctx.bot.user.id}>', f'<@!{ctx.bot.user.id}>']:
			prefix = '@MathBot '
		
		try:
			for index, page in enumerate(found_doc):
				page = doubleformat(
					page,
					prefix=prefix,
					mention=ctx.bot.user.mention,
					add_link='https://denvercoder1.github.io/math-bot-with-steps/add.html',
					server_link=SERVER_LINK,
					patreon_listing=await ctx.bot.get_patron_listing()
				)
				await ctx.message.author.send(page)
		except discord.Forbidden:
			await ctx.send(embed=discord.Embed(
				title='The bot was unable to slide into your DMs',
				description=f'Please try modifying your privacy settings to allow DMs from server members. If you are still experiencing problems, contact the developer at the mathbot server: {SERVER_LINK}',
				colour=discord.Colour.red()
			))
		else:
			if ctx.interaction:
				await ctx.interaction.response.send_message("Help has been sent to your DMs.", ephemeral=True)

	async def _send_topic_list(self, ctx: commands.Context[commands.Bot]):
		topics = core.help.listing()
		column_width = max(map(len, topics))
		columns = 3
		reply = 'The following help topics exist:\n```\n'
		for i, t in enumerate(topics):
			reply += t.ljust(column_width)
			reply += '\n' if (i + 1) % columns == 0 else '  ';
		reply += '```\n'
		await ctx.send(reply)

	def _suggest_topics(self, typo):
		suggestions = core.help.get_similar(typo)
		if not suggestions:
			return f"That help topic does not exist."
		elif len(suggestions) == 1:
			return f"That help topic does not exist.\nMaybe you meant `{suggestions[0]}`?"
		return f"That help topic does not exist.\nMaybe you meant one of: {', '.join(map('`{}`'.format, suggestions))}?"

async def setup(bot: commands.Bot):
	await bot.add_cog(HelpModule())
