from cgitb import text
from pydoc import describe
from unicodedata import name
import disnake
from disnake.ext import commands
from disnake import AllowedMentions, member, channel
import random
import json
from datetime import datetime
import aiohttp
from requests import request

class Chemistry(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='atom')
    async def atom(self, inter):
        pass

    @atom.sub_command(name='lookup', description="Provides some information on an element of periodic table.")
    async def lookup(self, inter, number: int):
        """
        "Provides some information on an element of periodic table."

        Parameters
        ----------
        number: The atomic number of element.
        """
        if 0 > number or number > 118 or number == 0:
            await inter.response.send_message("Number must be greater than 0 or less than 118.")
        else:
            async with aiohttp.ClientSession() as session:
                request = await session.get(f'https://neelpatel05.pythonanywhere.com/element/atomicnumber?atomicnumber={number}')
                data = await request.json()
            if data["atomicMass"] == "":
                data["atomicMass"] = "_ _"
            if data["atomicRadius"] == "":
                data["atomicRadius"] = "_ _"
            if data["boilingPoint"] == "":
                data["boilingPoint"] = "_ _"
            if data["bondingType"] == "":
                data["bondingType"] = "_ _"
            if data["density"] == "":
                data["density"] = "_ _"
            if data["electronAffinity"] == "":
                data["electronAffinity"] = "_ _"
            if data["electronegativity"] == "":
                data["electronegativity"] = "_ _"
            if data["ionRadius"] == "":
                data["ionRadius"] = "_ _"
            if data["ionizationEnergy"] == "":
                data["ionizationEnergy"] = "_ _"
            if data["meltingPoint"] == "":
                data["meltingPoint"] = "_ _"
            if data["oxidationStates"] == "":
                data["oxidationStates"] = "_ _"
            if data["standardState"] == "":
                data["standardState"] = "_ _"
            if data["vanDelWaalsRadius"] == "":
                data["vanDelWaalsRadius"] = "_ _"
            if data["yearDiscovered"] == "":
                data["yearDiscovered"] = "_ _"
            if data['cpkHexColor'] == "":
                embed = disnake.Embed(title=data["name"], color=0x000000)
                embed.add_field(name="Atomic mass:", value=data["atomicMass"])
                embed.add_field(name="Atomic number:", value=data["atomicNumber"])
                embed.add_field(name="Atomic radius:", value=data["atomicRadius"])
                embed.add_field(name="Boiling Point:", value=data["boilingPoint"])
                embed.add_field(name="Bonding type:", value=data["bondingType"])
                embed.add_field(name="CPK color:", value=data["cpkHexColor"])
                embed.add_field(name="Density:", value=data["density"])
                embed.add_field(name="Electron affinity:", value=data["electronAffinity"])
                embed.add_field(name="Electronegativity:", value=data["electronegativity"])
                embed.add_field(name="Electronic configuration:", value=data["electronicConfiguration"])
                embed.add_field(name="Group block:", value=data["groupBlock"])
                embed.add_field(name="Ion radius:", value=data["ionRadius"])
                embed.add_field(name="Ionization energy:", value=data["ionizationEnergy"])
                embed.add_field(name="Melting point:", value=data["meltingPoint"])
                embed.add_field(name="Oxidation states:", value=data["oxidationStates"])
                embed.add_field(name="Standard states:", value=data["standardState"])
                embed.add_field(name="Symbol:", value=data["symbol"])
                embed.add_field(name="Van del waals radius:", value=data["vanDelWaalsRadius"])
                embed.add_field(name="Year discovered:", value=data["yearDiscovered"])
                await inter.response.send_message(embed=embed)
            else:
                co = int(data['cpkHexColor'], 16)
                embed = disnake.Embed(title=data["name"], color=co)
                embed.add_field(name="Atomic mass:", value=data["atomicMass"])
                embed.add_field(name="Atomic number:", value=data["atomicNumber"])
                embed.add_field(name="Atomic radius:", value=data["atomicRadius"])
                embed.add_field(name="Boiling Point:", value=data["boilingPoint"])
                embed.add_field(name="Bonding type:", value=data["bondingType"])
                embed.add_field(name="CPK color:", value=data["cpkHexColor"])
                embed.add_field(name="Density:", value=data["density"])
                embed.add_field(name="Electron affinity:", value=data["electronAffinity"])
                embed.add_field(name="Electronegativity:", value=data["electronegativity"])
                embed.add_field(name="Electronic configuration:", value=data["electronicConfiguration"])
                embed.add_field(name="Group block:", value=data["groupBlock"])
                embed.add_field(name="Ion radius:", value=data["ionRadius"])
                embed.add_field(name="Ionization energy:", value=data["ionizationEnergy"])
                embed.add_field(name="Melting point:", value=data["meltingPoint"])
                embed.add_field(name="Oxidation states:", value=data["oxidationStates"])
                embed.add_field(name="Standard states:", value=data["standardState"])
                embed.add_field(name="Symbol:", value=data["symbol"])
                embed.add_field(name="Van del waals radius:", value=data["vanDelWaalsRadius"])
                embed.add_field(name="Year discovered:", value=data["yearDiscovered"])
                await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Chemistry(bot))
