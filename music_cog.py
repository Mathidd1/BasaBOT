import discord
from discord.ext import commands
from random import choice, randint
from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}
    
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False
    
    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    await ctx.send('No me pude conectar al canal po aweonao')
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e:self.play_next())
        else:
            self.is_playing = False
    
    @commands.command(name= 'play', aliases=['p', 'ponerla'], help='Te pone la cancion del yutun en el chat')
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send('Conectate po sacowea')
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send('No te la pude poner, prueba otra palabrita clavesita')
            else:
                await ctx.send('Te la meti :3')
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music(ctx)
    
    @commands.command(name= 'pause', aliases=['pausar'], help='Te pausa la cancion po que mas va a hacer XD') 
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.vc.resume()

    @commands.command(name= 'resume', aliases=['c', 'continuar'], help='Reanuda la cancioncita o ASMR de Springtrap que estes escuchando') 
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name= 'skip', aliases=['s', 'saltar'], help='Te salta la cancion como el Diego cuando anda nerviosito') 
    async def skip(self, ctx, *args):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)
    
    @commands.command(name= 'queue', aliases=['l', 'lista'], help='Muestra los videitos feitos que van a sonar despues') 
    async def queue(self, ctx):
        retval = ''

        for i in range(0, len(self.music_queue)):
            if i > 4: break
            retval += self.music_queue[i][0]['title'] + '\n'

        if retval != '':
            await ctx.send(retval)
        else:
            await ctx.send('No has puesto niuna, y canciones tampoco')

    @commands.command(name= 'clear', aliases=['li', 'limpiar'], help='Limpia toda la listita y te la para')
    async def clear(self, ctx, *args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send('Te limpie la colita UWU')
    
    @commands.command(name= 'leave', aliases=['le', 'salir'], help='Saca a la persona mas divertida de la llamada')
    async def leave(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
    
    @commands.command(name= 'di', aliases=['d', "say"], help='Repite lo que se lo poni')
    async def say(self, ctx, *args):
        query = " ".join(args)
        if "@everyone" not in query:
            await ctx.send(query)

    @commands.command(name= 'decide', aliases=["de", "choose"], help='Tu propio tomador de decisiones cuando no tienes iniciativa propia, separa las opciones por una coma')
    async def decide(self, ctx, *args):
        query = " ".join(args)
        try:
            opciones = query.split(",")
            await ctx.send(choice(opciones))
        except:
            await ctx.send("Tienen que estar separados por una coma TONTO WEON")
    
    @commands.command(name= 'aleatorio', aliases=["random", "al", "r"], help="Te da un numero aleatorio entre 2 separados por una coma, no se me ocurrio nada chistoso NSJKSN")
    async def random(self, ctx, *args):
        query = " ".join(args)
        try:
            opciones = query.split(",")
            opciones[0] = opciones[0].strip()
            opciones[1] = opciones[1].strip()
            if int(opciones[0]) > int(opciones[1]):
                await ctx.send(randint(int(opciones[1]), int(opciones[0])))
            else:
                await ctx.send(randint(int(opciones[0]), int(opciones[1])))
        except:
            await ctx.send("Tienen que ser 2 numeros separados por una coma AWEONAO")