"""
MIT License
Copyright (c) 2021 lucaso60
Copyright (c) 2021 LEL Studios
Copyright (c) 2015-2021 Rapptz
Copyright (c) 2021-present Pycord Development
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import discord
from discord.ext import commands
from discord.commands import slash_command, Option

import asyncio
import aiohttp

from modules.functions import time_now

# Functions
# Get the current crypto price from cryptocompare.com


async def get_price(symbol):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://min-api.cryptocompare.com/data/price?fsym={symbol}&tsyms=USD") as response:
            data = await response.json()
    return data

# Get crypto news from cryptocompare.com


async def get_news():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://min-api.cryptocompare.com/data/v2/news/?categories=General,Misc&lang=EN") as response:
            data = await response.json()
    return data


# Cog


class crypto(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    cryptocompare_error = discord.Embed(
        title="Error - CryptoCompare", description="An error has occured with the CryptoCompare API. Please try again later.", color=discord.Color.red())
    cryptocompare_error.add_field(
        name="Information", value="If this error persists, try to replace the parameters if you can or contact the developer.")
    cryptocompare_error.add_field(
        name="Parameters", value="If you can pass in parameters, CryptoCompare may not have the data you requested.")
    cryptocompare_error.set_thumbnail(
        url="https://www.cryptocompare.com/media/35264254/72_horizontal_fullcolour_darkblueflashgreen.png")
    cryptocompare_error.set_footer(text="Error Message")

    @slash_command(name="cryptonews")
    async def cryptonews(self, ctx: commands.Context):
        try:
            data = await get_news()
            embed = discord.Embed(
                title="Crypto News",
                color=0x00ff00
            )
            embed.set_thumbnail(url=data['Data'][0]['imageurl'])
            embed.add_field(
                name=data['Data'][0]['title'],
                value=data['Data'][0]['body'],
                inline=False
            )
            embed.set_footer(text=f"Source: min-api.cryptocompare.com")
            await ctx.send(embed=embed)
        except:
            await ctx.send(embed=self.cryptocompare_error)

    @slash_command(name="cryptoprice")
    async def cryptoprice(self, ctx: commands.Context, *, symbol: str):
        try:
            data = await get_price(symbol)
            embed = discord.Embed(title="Crypto Price", color=0x00ff00)
            embed.add_field(name=f"{symbol} Price", value=f"${data['USD']}")
            embed.set_thumbnail(
                url="https://www.cryptocompare.com/media/35264254/72_horizontal_fullcolour_darkblueflashgreen.png")
            embed.set_footer(text=f"Source: min-api.cryptocompare.com")
            await ctx.send(embed=embed)
        except:
            await ctx.send(embed=self.cryptocompare_error)


def setup(bot: commands.Bot):
    bot.add_cog(crypto(bot))
