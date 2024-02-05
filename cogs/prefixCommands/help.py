import discord
from discord.ext import commands
from discord.ui import View, Select, Button

class HelpView(View): 
    def __init__(self, select, bot, ctx, interaction):
        bot = self.bot
        ctx = self.ctx 
        userbot = self.bot.user.name
        color_error = self.bot.color_error = 0x2b2d31
        color_pastel = self.fbot.color_pastel = 0x2b2d31
        prefix = self.bot.get_prefix(ctx.message)
        
        @discord.ui.select(
            placeholder='Click for more of kira',
            options=[
                discord.SelectOption(label='home', value='0', description='kira Home Page'),
                discord.SelectOption(label='action', value='1', description='kira Action Commands'),
                discord.SelectOption(label='anime', value='2', description='kira Anime Commands'),
                discord.SelectOption(label='club', value='3', description='kira Club Commands'),
                discord.SelectOption(label='config', value='4', description='kira Setting Commands'),
                discord.SelectOption(label='currency', value='5', description='kira Economy Commands'),
                discord.SelectOption(label='fun', value='6', description='kira Fun Commands'),
                discord.SelectOption(label='info', value='7', description='kira Information Commands'),
                discord.SelectOption(label='manager', value='8', description='kira Administration Commands'),
                discord.SelectOption(label='marriage', value='9', description='kira Marriage Commands'),
                discord.SelectOption(label='misc', value='10', description='kira Miscellaneous Commands'),
                discord.SelectOption(label='mod', value='11', description='kira Moderation Commands'),
                discord.SelectOption(label='music', value='12', description='kira Music Commands'),
                discord.SelectOption(label='nsfw', value='13', description='kira NSFW Commands'),
                discord.SelectOption(label='reaction', value='14', description='kira Reaction Commands'),
                discord.SelectOption(label='utils', value='15', description='kira Utility Commands'),
                discord.SelectOption(label='genshin', value='16', description='kira Genshin Impact Commands'),
                discord.SelectOption(label='verify', value='17', description='kira Verification Commands'),
            ]
        ) 
        async def select_callback(): 
            try:
                select.disabled = True
                selected_value = interaction.data["values"][0]

                if selected_value == "0":
                    thumbnail_url = bot.user.avatar.url
                    embed = discord.Embed(
                        title="**{} home page <3**".format(bot.user.name),  
                        description=
                        f"""**Comandos de {bot.user.name}**
                        
                        » **Menú de ayuda**\n\n Tenemos `7` categories, `38` `/` and `10` `{prefix}` comandos a explorar. Hay `0` Comandos Secretos.
                            
                        Lista de comandos: `help <category>`
                        Comandos detallados: `help <command>`
                        » **Categorías**"
                        `{prefix} help action`  ∷ Action
                        `{prefix} help anime`  ∷ Anime
                        `{prefix} help club`  ∷ Club
                        `{prefix} help config`  ∷ Setting
                        `{prefix} help currency`  ∷ Economy
                        `{prefix} help fun`  ∷ Fun
                        `{prefix} help info`  ∷ Information
                        `{prefix} help manager`  ∷ Administration
                        `{prefix} help marriage`  ∷ Marriages
                        `{prefix} help misc`  ∷ Miscellaneous
                        `{prefix} help mod`  ∷ Moderation
                        `{prefix} help music`  ∷ Music
                        `{prefix} help nsfw`  ∷ NSFW
                        `{prefix} help reaction`  ∷ Reaction
                        `{prefix} help utils`  ∷ Utilities
                        `{prefix} help genshin`  ∷ Genshin Impact
                        `{prefix} help verify`  ∷ Verification""") 
                    embed.set_thumbnail(url=thumbnail_url)
                    embed.set_footer(text=userbot, icon_url=thumbnail_url)
                    await interaction.response.edit_message(embed=embed)

                if selected_value == "1":
                    thumbnail_url = bot.user.avatar.url
                    embed = discord.Embed(
                        title=f"kira Action commands <3", 
                        description=
                        f"Ayuda detallada sobre un comando: `{prefix}help <action>`\n\n"+
                        f"""**Comandos:** 
                        ```bf\nangry           baka            bang            bite            bye             cheeks          claps           cook            cuddle          feed            gaming          glare           handhold        heal            hi              highfive        hug             kickbutt        kill            kisscheeks      laugh           lick            pat             poke            punch           scared          slap            sleep           smack           spank           splash          spray           stare           throw           tickle          tsundere        wink            kiss```""") 
                    embed.set_thumbnail(url=thumbnail_url)
                    embed.set_color(color_pastel)
                    await interaction.response.edit_message(embed=embed)

                if selected_value == "2":
                    thumbnail_url = bot.user.avatar.url
                    embed = discord.Embed(
                        title=f"kira Anime commands <3", 
                        description=
                        f"Ayuda detallada sobre un comando: `{prefix}help <anime>`\n\n"+ 
                        f"""**Comandos:**
                        ```bf\nanimanga        anilist         anisearch       awoo            crunchyroll     fbi             husbando        jpose           kemo            manlist         mansearch       nani            neko            nekogif         nekotina        poi             ranime          rmanga          rem             rero            trap            tanime          tmanga          waifu           zawarudo```""")
                    embed.set_thumbnail(url=thumbnail_url)
                    embed.set_color(color_pastel)
                    await interaction.response.edit_message(embed=embed)

                if selected_value == "3":
                    thumbnail_url = bot.user.avatar.url
                    embed = discord.Embed(
                        title=f"kira Club commands <3", 
                        description=
                        f"Ayuda detallada sobre un comando: `{prefix}help <club>`\n\n"+
                        f"""**Comandos:**
                        ```bf\nclubaccept      clubadmin       clubapply       clubapps        clubban         clubbans        clubcreate      clubdep         clubdesc        clubdisband     clubicon        clubinfo        clubkick        clublb          clubleave       clublevel       clublogs        clubmanager     clubmember      clubreject      clubrename      clubskills      clubstorage     clubtransfer    clubunban       clubwd```""")
                    embed.set_thumbnail(url=thumbnail_url)
                    embed.set_color(color_pastel)                    
                    await interaction.response.edit_message(embed=embed) 

                if selected_value == "4":
                    thumbnail_url = bot.user.avatar.url
                    embed = discord.Embed(
                        title=f"kira Configuration commands <3",
                        description=
                        f"Ayuda detallada sobre un comando: `{prefix}help <config>`\n\n"+
                        f"""**Comandos:**
                        ```bf\ndisable         enable          setalerts       setanime        setantiinvites  setantiscam     setautopost     setautoroles    setbabel        setban          setboost        setchatbot      setconfess      setgoodbye      setkick         setlang         setlevelup      setlogs         setmanga        setmod          setmusic        setmute         setnekora       setprefix       setreact        setreactionrole setrepeat       setresponder    setshopmod      setsoftban      settimeout      setunban        setunmute       setuntimeout    setunwarn       setwarn         setwelcome      setup           starboard```""") 
                    embed.set_thumbnail(url=thumbnail_url)
                    await interaction.response.edit_message(embed=embed)

                if selected_value == "5":
                    thumbnail_url = bot.user.avatar.url
                    embed = discord.Embed(
                        title=f"kira Economy commands <3", 
                        description=
                        f"Ayuda detallada sobre un comando: `{prefix}help <currency>`\n\n"+
                        f"""**Comandos:**
                        ```bf\nbag             balance         buffs           buy             claimcode       collect         craft           crime           daily           deposit         event           fish            gift            guide           iteminfo        leaderboard     market          mine            nekodex         nekoshop        pet             profile         quest           rank            repair          sell            servershop      settings        share           shop            slots           storage         trade           use             withdraw        work            xmas            mix             chop```""")
                    embed.set_thumbnail(url=thumbnail_url)
                    embed.set_color(color_pastel)
                    await interaction.response.edit_message(embed=embed)

                if selected_value == "6":
                    thumbnail_url = bot.user.avatar.url
                    embed = discord.Embed(
                        title=f"kira Joy commands <3",
                        description=
                        f"Ayuda detallada sobre un comando: `{prefix}help <fun>`\n\n"+
                        f"""**Comandos:**
                        ```bf\n8ball           ask             banana          bonk            catfact         choose          confess         delete          dogfact         dream           guess           kitty           lucky           magik           match           petpet          pupper          reputation      roll            rps             say             ship            stonks          sus             tictactoe       traderep        trivia          tweet```""")
                    embed.set_thumbnail(url=thumbnail_url)
                    embed.set_color(color_pastel)
                    await interaction.response.edit_message(embed=embed)

                if selected_value == "7":
                    thumbnail_url = bot.user.avatar.url
                    embed = discord.Embed(
                        title=f"kira Information commands <3",
                        description=
                        f"Ayuda detallada sobre un comando: `{prefix}help <info>`\n\n"+
                        f"""**Comandos:**
                        ```bf\ndonate          help            invite          partners        ping            prefix          rules           stats           support         updates         vote```""")
                    embed.set_thumbnail(url=thumbnail_url)
                    embed.set_color(color_pastel)
                    await interaction.response.edit_message(embed=embed)

                if selected_value == "8":
                    thumbnail_url = bot.user.avatar.url
                    embed = discord.Embed(
                        title=f"kira Administration commands <3",
                        description=
                        f"Ayuda detallada sobre un comando: `{prefix}help <manager>`\n\n"+
                        f"""**Comandos:**
                        ```bf\naddrole         coloroles       lock            massrole        purge           removerole      rolecolor       setnick         slowmode        togglensfw      unlock```""")
                    embed.set_thumbnail(url=thumbnail_url)
                    embed.set_color(color_pastel)
                    await interaction.response.edit_message(embed=embed)
                
                if selected_value == "9":
                    thumbnail_url = bot.user.avatar.url
                    embed = discord.Embed(
                        title=f"kira Marriage commands <3",
                        description=
                        f"Ayuda detallada sobre un comando: `{prefix}help <marriage>`\n\n"+
                        f"""**Comandos:**
                        ```bf\nacceptmarriage  declinemarriage divorce         letter          marriages       marry           proposals       teammate        tree```""")
                    embed.set_thumbnail(url=thumbnail_url)
                    embed.set_color(color_pastel)
                    await interaction.response.edit_message(embed=embed)

                if selected_value == "10":
                    thumbnail_url = bot.user.avatar.url
                    embed = discord.Embed(
                        title=f"kira Miscleaneous commands <3",
                        description=
                        f"Ayuda detallada sobre un comando: `{prefix}help <misc>`\n\n"+
                        f"""**Comandos:**
                        ```bf\nafk             avatar          banner          channel         color           emoji           emojis          github          inviteinfo      rgb             randomcolor     randomuser      role            roles           server          serverbanner    serverdiscovery servericon      tiktok          twitch          userinfo```""")
                    embed.set_thumbnail(url=thumbnail_url)
                    embed.set_color(color_pastel)
                    await interaction.response.edit_message(embed=embed)

                if selected_value == "11":
                    thumbnail_url = bot.user.avatar.url
                    embed = discord.Embed(
                        title=f"kira Moderation commands <3",
                        description=
                        f"Ayuda detallada sobre un comando: `{prefix}help <mod>`\n\n"+
                        f"""**Comandos:**
                        ```bf\nban             case            clearwarns      forceban        hardmute        kick            moderations     mute            mutelist        softban         timeout         unban           unmute          untimeout       unwarn          updatecase      warn            warns```""")
                    embed.set_thumbnail(url=thumbnail_url)
                    embed.set_color(color_pastel)
                    await interaction.response.edit_message(embed=embed)

                if selected_value == "12":
                    thumbnail_url = bot.user.avatar.url
                    embed = discord.Embed(
                        title=f"kira Music commands <3",
                        description=
                        f"Ayuda detallada sobre un comando: `{prefix}help <music>`\n\n"+
                        f"""**Comandos:**
                        ```bf\nclear           insert          join            loop            loopqueue       lyrics          move            nowplaying      pause           play            queue           radio           remove          replay          resume          reverse         search          seek            shuffle         skip            stop```""")
                    embed.set_thumbnail(url=thumbnail_url)
                    embed.set_color(color_pastel)
                    await interaction.response.edit_message(embed=embed)

                if selected_value == "13":
                    thumbnail_url = bot.user.avatar.url
                    embed = discord.Embed(
                        title=f"kira NSFW commands <3",
                        description=
                        f"Ayuda detallada sobre un comando: `{prefix}help <nsfw>`\n\n"+
                        f"""**Comandos:**
                        ```bf\nhentai          neko            wallpaper```""")
                    embed.set_thumbnail(url=thumbnail_url)
                    embed.set_color(color_pastel)
                    await interaction.response.edit_message(embed=embed)

                if selected_value == "14":
                    thumbnail_url = bot.user.avatar.url
                    embed = discord.Embed(
                        title=f"kira Reaction commands <3",
                        description=
                        f"Ayuda detallada sobre un comando: `{prefix}help <react>`\n\n"+
                        f"""**Comandos:**
                        ```bf\nbanghead        blush           boom            bored           confused        cry             dab             dance           deredere        disgust         drunk           eat             facepalm        fail            fly             happy           jump            lewd            like            nope            peek            pout            psycho          run             sad             scream          shrug           sing            sip             smile           smug            teehee          think           thinking        trick           vomit           wag             wasted          yandere```""")
                    embed.set_thumbnail(url=thumbnail_url)
                    embed.set_color(color_pastel)
                    await interaction.response.edit_message(embed=embed)

                if selected_value == "15":
                    thumbnail_url = bot.user.avatar.url
                    embed = discord.Embed(
                        title=f"kira Utility commands <3",
                        description=
                        f"Ayuda detallada sobre un comando: `{prefix}help <utils>`\n\n"+
                        f"""**Comandos:**
                        ```bf\nbirthday        block           blocklist       math            rate            reedem          remindme        star            suggestion      tag             transcribe      translate       unblock         weather         wiki```""")
                    embed.set_thumbnail(url=thumbnail_url)
                    embed.set_color(color_pastel)
                    await interaction.response.edit_message(embed=embed)

                if selected_value == "16":
                    thumbnail_url = bot.user.avatar.url
                    embed = discord.Embed(
                        title=f"kira Genshin Impact commands <3",
                        description=
                        f"Ayuda detallada sobre un comando: `{prefix}help <genshin>`\n\n"+
                        f"""**Comandos:**
                        ```bf\nregister        login           logout          profile         character       artifact        weapon          constellation          element```""") 	
                    embed.set_thumbnail(url=thumbnail_url)  
                    embed.set_color(color_pastel)
                    await interaction.response.edit_message(embed=embed)

                if selected_value == "17":
                    embed.set_thumbnail(url)
                    thumbnail_url = bot.user.avatar.url
                    embed.set_color(color_pastel)
                    embed = discord.Embed(
                        title=f"kira Verification commands <3",
                        description=
                        f"Ayuda detallada sobre un comando: `{prefix}help <verify>`\n\n"+
                        f"""**Comandos:**
                        ````bf\nverify          unverify        verifylist      unverifylist```""")
            
            except Exception as e:
                embed = discord.Embed(
                    title="Error!",
                    description=f"**`{e}`**",
                    color= color_error
            )
        
class Help(View): 
    def __init__(self, ctx):
        super().__init__()
        bot = self.bot
        ctx = self.ctx 
        color_error = self.bot.color_error = 0xe74c3c
        color_pastel = self.bot.color_pastel = 0x2b2d31
        prefix = self.bot.get_prefix(ctx.message)   
        
        commands.command(name="ayuda", aliases=["help", "h", "a"])
        async def ayuda(): 
            view = HelpView() 
            bot = ctx.bot
            thumbnail_url = bot.user.avatar.url
            embed = discord.Embed(
                title="**{} home page <3**".format(bot.user.name), 
                description=
                f"""**Comandos de {bot.user.name}**
                
                » **Menú de ayuda**\n\n Tenemos `7` categories, `38` `/` and `10` `{prefix}` comandos a explorar. Hay `0` Comandos Secretos.
                
                Lista de comandos: `help <category>`
                Comandos detallados: `help <command>`
                » **Categorías**"
                `{prefix} help action`  ∷ Action
                `{prefix} help anime`  ∷ Anime
                `{prefix} help club`  ∷ Club
                `{prefix} help config`  ∷ Setting
                `{prefix} help currency`  ∷ Economy
                `{prefix} help fun`  ∷ Fun
                `{prefix} help info`  ∷ Information
                `{prefix} help manager`  ∷ Administration
                `{prefix} help marriage`  ∷ Marriages
                `{prefix} help misc`  ∷ Miscellaneous
                `{prefix} help mod`  ∷ Moderation
                `{prefix} help music`  ∷ Music
                `{prefix} help nsfw`  ∷ NSFW
                `{prefix} help reaction`  ∷ Reaction
                `{prefix} help utils`  ∷ Utilities
                `{prefix} help genshin`  ∷ Genshin Impact
                `{prefix} help verify`  ∷ Verification""") 
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_footer(text=bot.user.name, icon_url=thumbnail_url)
            embed.color = color_pastel
            await ctx.send(embed=embed, view=view) 
            
            view.stop() 
            
async def setup(bot):
    await bot.add_cog(Help(bot)) 
