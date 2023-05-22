import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.help_message = """
```
Comandos del mejor bot de latinoamerica unida osiosi:

$ayuda o $help - Te muestra esta misma wea XD

Musica:

$ponerla, $p <link>- Te pone la cancion del yutun en el chat
$pausar - Te pausa la cancion po que mas va a hacer XD
$continuar, $c - Reanuda la cancioncita o ASMR de Springtrap que estes escuchando
$saltar, $s - Te salta la cancion como el Diego cuando anda nerviosito
$lista, $l - Muestra los videitos feitos que van a sonar despues
$limpiar, $li - Limpia toda la listita y te la para
$salir, $le - Saca a la persona mas divertida de la llamada

Fun:

$di, $d, $say <mensaje> - Repite lo que se lo poni
$decide, $de, $choose <mensaje> - Tu propio tomador de decisiones cuando no tienes iniciativa propia, separa las opciones por una coma
$aleatorio, $random, $al, $r <mensaje> - Te da un numero aleatorio entre 2 separados por una coma, no se me ocurrio nada chistoso NSJKSN
```
"""
    @commands.command(name='help', aliases=['ayuda'], help= 'Muestra todos los comandos que podi usar')
    async def help(self, ctx):
        await ctx.send(self.help_message)