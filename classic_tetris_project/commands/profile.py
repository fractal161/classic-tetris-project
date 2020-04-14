from discord import Embed
from discord.utils import get

from ..discord import get_guild #our discord.
from .command import Command, CommandException
from ..countries import Country

from ..util.json_template import match_template
    
TEMPLATE = ("""
{{    
    "color": {color},   
    "author": {{
      "name": "{name}",
      "url": "https://github.com/professor-l/classic-tetris-project/",
      "icon_url": "{player_icon}"
    }},
    "fields": [
      {{
        "name": "Personal Bests",
        "value": "```NTSC: {ntsc_pb} \\nNTSC(19): {ntsc_pb_19}\\nPAL: {pal_pb}```\\n"
      }},
      {{
        "name": "Pronouns",
        "value": "{pronouns}",
        "inline": "True"
      }},
      {{
        "name": "Playstyle",
        "value": "{playstyle}",
        "inline": "True"
      }},
      {{
        "name": "Country",
        "value": "{country}",
        "inline": "True"
      }},
      {{
        "name": "Same Piece sets",
        "value": "{same_pieces}",
        "inline": "True"
      }},
      {{
        "name": "Twitch",
        "value": "{twitch_channel}"
      }}]
}}
""")

PLAYSTYLE_EMOJI = {
                   "das": "<:lovedas:602968808876933128>",
                   "hypertap": "<:lovetap:694400998914916412>",
                   "hybrid": "<:lovehyb:696135490776072212>"
                 }

TETRIS_X = "<:tetrisx:547170153301803009>"
TETRIS_CHECK = "<:tetrischeck:547169203963166760>"

PLAYER_ICON = "https://cdn.discordapp.com/avatars/{id}/{avatar}.jpg"

@Command.register_discord("profile",
                  usage="profile [username] (default username you)")
class ProfileCommand(Command):
    
    def execute(self, *username):
        username = username[0] if len(username) == 1 else self.context.args_string
        if username and not self.any_platform_user_from_username(username):
            raise CommandException("Specified user has no profile.")

        platform_user = (self.any_platform_user_from_username(username) if username
                         else self.context.platform_user)

        if not platform_user:
            raise CommandException("Invalid specified user.")

        user = platform_user.user
        name = self.context.display_name(platform_user)
                
        player_icon = self.get_player_icon(name, username)
        color = self.get_color(name, username)
        
        ntsc_pb = self.format_pb(user.get_pb("ntsc")).rjust(13)
        ntsc_pb_19 = self.format_pb(user.get_pb("ntsc", 19)).rjust(9)
        pal_pb = self.format_pb(user.get_pb("pal")).rjust(14)
        
        pronouns = user.get_pronouns_display() or "Not set"
        
        playstyle = self.get_playstyle(user)
        country = self.get_country(user)        
        same_pieces = self.get_same_pieces(user)        
        twitch_channel = self.get_twitch(user)       
        
        json_message = match_template(TEMPLATE,
                                      name=name,
                                      color=color,
                                      player_icon=player_icon,
                                      ntsc_pb=ntsc_pb,
                                      ntsc_pb_19=ntsc_pb_19,
                                      pal_pb=pal_pb,
                                      pronouns=pronouns,
                                      playstyle=playstyle,
                                      country=country,
                                      same_pieces=same_pieces,
                                      twitch_channel=twitch_channel)        

        e = Embed.from_dict(json_message)
        self.send_message_full(self.context.channel.id, embed=e)
    
    def format_pb(self, value):
        if value:
            return "{pb:,}".format(pb=value)
        else:
            return "Not set"

    def get_player_icon(self, name, username):
        guild = self.context.guild or get_guild()
        # search for multiple members...
        members = [guild.get_member_named(n) for n in [name,username]]
        for m in members:
            if m is not None and m.avatar is not None:
                return PLAYER_ICON.format(id=m.id, avatar=m.avatar)
        
        return ""

    def get_color(self, name, username):
        guild = self.context.guild or get_guild()  

        members = [guild.get_member_named(n) for n in [name,username]]
        for m in members:
            if m is not None and m.color is not None:
                return m.color.value
        
        return 0 # black

    def get_playstyle(self, user):        
        if user.playstyle:            
            ps_emoji = PLAYSTYLE_EMOJI[user.playstyle]            
            return ps_emoji + " " + user.get_playstyle_display()
        else:
            return "Not set"

    def get_country(self, user):
        if user.country is not None:
            country = Country.get_country(user.country)
            return country.get_flag() + " " + country.full_name
        return "Not set"

    def get_same_pieces(self, user):
        if user.same_piece_sets:
            return (TETRIS_CHECK + " Yes")
        else:            
            return (TETRIS_X + " No")

    def get_twitch(self, user):
        if hasattr(user, "twitch_user"):
            return f"https://www.twitch.tv/{user.twitch_user.username}"
        return "Not `!link`ed"
