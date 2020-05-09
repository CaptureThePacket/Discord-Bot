"""
 _____             _                    _   _           ______          _        _
/  __ \           | |                  | | | |          | ___ \        | |      | |
| /  \/ __ _ _ __ | |_ _   _ _ __ ___  | |_| |__   ___  | |_/ /_ _  ___| | _____| |_
| |    / _` | '_ \| __| | | | '__/ _ \ | __| '_ \ / _ \ |  __/ _` |/ __| |/ / _ \ __|
| \__/\ (_| | |_) | |_| |_| | | |  __/ | |_| | | |  __/ | | | (_| | (__|   <  __/ |_
 \____/\__,_| .__/ \__|\__,_|_|  \___|  \__|_| |_|\___| \_|  \__,_|\___|_|\_\___|\__|
			| |
			|_|
=====================================================================================
						Copyright 2020 - Jordan Maxwell
						GNU General Public License v3.0
                      Written by Jordan Maxwell 05/09/2020
"""

import logging
import json
import sys
import os

from discord.ext import commands

def load_config_file(name: str) -> dict:
    """
    Loads a configuration file from the config directory
    """

    data = {}
    with open('config%s%s.json' % (os.sep, name), 'r') as f:
        data = json.load(f)

    return data

config = load_config_file('config')
secure = load_config_file('secure')
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(config['prefix']),
    description='Official Discord bot for the futuristic retro shooter Capture the Packet')
bot.loaded_cogs = []
bot.unloaded_cogs = []
logging.basicConfig(level=logging.INFO)

def check_if_dirs_exist() -> None:
    """
    Creates the "cogs" directory if it doesn't exist already
    """

    os.makedirs('cogs', exist_ok=True)

def load_autoload_cogs():
    """
    Loads all .py files in the cogs subdirectory that are in the config file as "autoload_cogs" as cogs into the bot. 
    If your cogs need to reside in subfolders (ie. for config files) create a wrapper file in the cogs 
    directory to load the cog.
    """

    for entry in os.listdir('cogs'):
        if entry.endswith('.py') and os.path.isfile('cogs/{}'.format(entry)) and entry[:-3] in config['autoload_cogs']:
            try:
                bot.load_extension("cogs.{}".format(entry[:-3]))
                bot.loaded_cogs.append(entry[:-3])
            except Exception as e:
                logging.error(e)
            else:
                logging.info('Succesfully loaded cog {}'.format(entry))

def get_names_of_unloaded_cogs() -> None:
    """
    Creates an easy loadable list of cogs.
    If your cogs need to reside in subfolders (ie. for config files) create a wrapper file in the auto_cogs
    directory to load the cog.
    """

    for entry in os.listdir('cogs'):
        if entry.endswith('.py') and os.path.isfile('cogs/{}'.format(entry)) and entry[:-3] not in bot.loaded_cogs:
            bot.unloaded_cogs.append(entry[:-3])

check_if_dirs_exist()
load_autoload_cogs()
get_names_of_unloaded_cogs()

@bot.command()
async def list_cogs(ctx: object) -> None:
    """
    Lists all cogs and their status of loading.
    """

    cog_list = commands.Paginator(prefix='', suffix='')
    cog_list.add_line('**✅ Succesfully loaded:**')
    for cog in bot.loaded_cogs:
        cog_list.add_line('- ' + cog)
    cog_list.add_line('**❌ Not loaded:**')
    for cog in bot.unloaded_cogs:
        cog_list.add_line('- ' + cog)
    
    for page in cog_list.pages:
        await ctx.send(page)

@bot.command()
async def load(ctx, cog):
    """
    Tries to load the selected cog.
    """

    if cog not in bot.unloaded_cogs:
        await ctx.send('⚠ WARNING: Cog appears not to be found in the available cogs list. Will try loading anyway.')
    if cog in bot.loaded_cogs:
        return await ctx.send('Cog already loaded.')
    try:
        bot.load_extension('cogs.{}'.format(cog))
    except Exception as e:
        await ctx.send('**💢 Could not load cog: An exception was raised. For your convenience, the exception will be printed below:**')
        await ctx.send('```{}\n{}```'.format(type(e).__name__, e))
    else:
        bot.loaded_cogs.append(cog)
        bot.unloaded_cogs.remove(cog)
        await ctx.send('✅ Cog succesfully loaded.')

@bot.command()
async def unload(ctx: object, cog: str) -> None:
    """
    Unloads the selected cog from the Discord bot
    """

    if cog not in bot.loaded_cogs:
        return await ctx.send('💢 Cog not loaded.')
    
    bot.unload_extension('cogs.{}'.format((cog)))
    bot.loaded_cogs.remove(cog)
    bot.unloaded_cogs.append(cog)
    await ctx.send('✅ Cog succesfully unloaded.')

@bot.event
async def on_ready() -> None:
    """
    Called on Discord bot ready.
    """

    logging.info('----------')
    logging.info('Logged in as:')
    logging.info(bot.user.name)
    logging.info(bot.user.id)
    logging.info('----------')


def start_bot() -> int:
    """
    """

    bot.run(secure["token"])

    return 0