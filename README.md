# MathBotWithSteps

MathBotWithSteps is a fork of [MathBot](https://github.com/DXsmiley/mathbot) that adds an additional command, `=steps` that will query Wolfram|Alpha **with step-by-step solutions**.

MathBot is a Discord bot that contains a number of features to help with mathematics.

It's primary features are:
- LaTeX rendering
- Querying Wolfram|Alpha
- A Turing complete calculator

## Links

- [Add MathBotWithSteps to your own server](https://denvercoder1.github.io/math-bot-with-steps/add.html)
- [DenverCoder1's Support Server](https://discord.gg/fPrdqh3Zfu)

<a href="https://denvercoder1.github.io/math-bot-with-steps/add.html" alt="Add bot" title="Add MathBotWithSteps to your server">
    <img src="https://custom-icon-badges.herokuapp.com/badge/-Add%20MathBotWithSteps-green?style=for-the-badge&logo=square-plus&logoColor=white"/></a>
<a href="https://discord.gg/fPrdqh3Zfu" alt="Discord" title="Dev Pro Tips Discussion & Support Server">
    <img src="https://img.shields.io/discord/819650821314052106?color=7289DA&logo=discord&logoColor=white&style=for-the-badge"/></a>

## Setup for use

```bash
git clone https://github.com/DenverCoderOne/math-bot-with-steps.git
cd math-bot-with-steps
cp mathbot/parameters_default.json mathbot/parameters.json
pipenv --python 3.9
pipenv install --skip-lock
```

Then open parameters.json and change `tokens` to the token of the bot used for development. Optionally change the other parameters.

It is *strongly* recommend that you setup an instance of Redis if you want to use the bot on even a moderate scale. The disk-based keystore is easy to setup but runs very slowly, and as such is only useful of a development tool.

Then navigate into the `mathbot` directory and run the bot with `python entrypoint.py parameters.json`.

## Setup for development

```bash
git clone https://github.com/DenverCoderOne/math-bot-with-steps.git
cd math-bot-with-steps
cp mathbot/parameters_default.json mathbot/parameters.json
pipenv --python 3.9
pipenv install --dev --skip-lock
```

Then open parameters.json and change `tokens` to the token of the bot. Change `release` to `development`. Optionally change the other parameters.

Then navigate into the `mathbot` directory and run the bot with `python entrypoint.py parameters.json`.

## Contributing guide

Feel free to fork the repo and make a pull request once you've made the changes.

## Setting up Wolfram|Alpha

1. [Grab yourself an API key](https://products.wolframalpha.com/api/)
2. Open parameters.json and change `wolfram > key`.

This should really only be used for development and personal use.

## Test Suite

Use the `test` script in side the `mathbot` folder to run the test suite.

Some of the tests require that a bot is running and connected to Discord. To enable them, use the `--run-automata` command line argument. In addition a file with the necessary tokens filled out needs to be provided to the `--parameter-file` argument. To get all tests running, the *token*, *automata* and *wolfram* parameters need to be filled out.

For the sake of example, I run my tests with the command `./test --run-automata --parameter-file=dev.json`. You should replace `dev.json` with a path to your own parameter file.

There are some additional tests that require a human to verify the bot's output. These can be enabled with `--run-automata-human`.

## Guide to `parameters.json`

- *release* : Release mode for the bot, one of `"development"`, `"beta"` or `"production"`
- *token* : Token to use for running the bot
- *wolfram*
	- *key* : API key for making Wolfram|Alpha queries
- *keystore*
	- *disk*
		- *filename* : The file to write read and write data to when in disk mode
	- *redis*
		- *url* : url used to access the redis server
		- *number* : the number of the database, should be a non-negative integer
	- *mode* : Either `"disk"` or `"redis"`, depending on which store you want to use. Disk mode is not recommended for deployment.
- *patrons* : list of patrons
	- Each *key* should be a Discord user ID.
	- Each *value* should be a string starting with one one of `"linear"`, `"quadratic"`, `"exponential"` or `"special"`. The string may contains additional information after this for human use, such as usernames or other notes.
- *analytics* : Keys used to post information to various bot listings.
	- *carbon*: Details for [carbonitex](http://carbonitex.net/)
	- *discord-bots*: API Key for [bots.discord.pw](https://bots.discord.pw/#g=1)
	- *bots-org*: API Key for [discordbots.org](https://discordbots.org/)
- *automata*
	- *token* : token to use for the automata bot
	- *target* : the username of the bot that the automata should target
	- *channel*: the ID of the channel that the tests should be run in
- *advertising*
	- *enable* : should be `true` or `false`. When `true`, the bot will occasionally mention the Patreon page when running queries.
	- *interval* : the number of queries between mentions of the Patreon page. This is measured on a per-channel basis.
	- *starting-amount* : Can be increased to lower the number of commands until the Patreon page is first mention.
- *error-reporting*
	- *channel*: ID of channel to send error reports to.
	- *webhook*: Webhook to send error reports to.
- *shards*
	- *total*: The total number of shards that the bot is running on.
	- *mine*: A list of integers (starting at `0`) specifying which shards should be run in this process.
