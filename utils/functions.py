import discord
from io import BytesIO
import re
from typing import List
from youtubesearchpython import VideosSearch

def get_all(content: str) -> dict:
    videosSearch = VideosSearch(content, limit = 10)
    return videosSearch.result()

async def get_links(bot, content: str) -> List[str]:
    loop = bot.loop
    result = await loop.run_in_executor(None, get_all, content)
    list_construct = [[creator['title'], creator['channel']['name'], creator['link']] for creator in result['result']]
    return list_construct
    


async def get_graph(bot, *args):
      og_dict = {
       "type":"line",
       "data":{
          "labels":[],
          "datasets":[
             {
                "label":"Statistics",
                "data":[],
            "backgroundColor":"rgb(255, 99, 132)",
            "borderColor":"rgb(255, 99, 132)",
            "fill":'false'
               }
            ]
         }
      }
      label1 = list(range(1, len(args)+1))
      print(label1)
      data = [x for x in args]
      og_dict['data']['labels'] = label1
      og_dict['data']['datasets'][0]['data'] = data
      param = {"c": str(og_dict)}
      url = "https://quickchart.io/chart"
      s = await bot.session.get(url, params=param)
      ob = BytesIO(await s.read())
      return discord.File(fp=ob, filename="plot.png")

class Spotify:
      def __init__(self, *, bot, member) -> None:
        self.member = member
        self.bot = bot
        self.embed = discord.Embed(title=f"{member.display_name} is Listening to Spotify", color = discord.Color.green())
        self.regex = "(https\:\/\/open\.spotify\.com\/artist\/[a-zA-Z0-9]+)"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

      @staticmethod
      async def fetch_from_api(bot, activity: discord.Spotify):
         act = activity
         base_url = "https://api.jeyy.xyz/discord/spotify"
         params = {'title': act.album, 'cover_url': act.album_cover_url, 'artists': act.artists, 'duration_seconds': act.duration.seconds, 'start_timestamp': act.start.timestamp()}
         s = await bot.session.get(base_url, params=params)
         buffer = BytesIO(await s.read())
         return discord.File(fp=buffer, filename="spotify.png")
 

      async def get_embed(self):  
          activity = discord.utils.find(lambda activity: isinstance(activity, discord.Spotify), self.member.activities)
          if not activity:
              return False
          url = activity.track_url
          result = await self.bot.session.get(activity.track_url, headers=self.headers)
          text = await result.text()
          my_list = re.findall(self.regex, text)
          artists = activity.artists
          final = sorted(set(my_list), key=my_list.index)
          total = len(artists)
          final_total = final[0:total]
          string = ""
          for x in final_total:
              string += f"[{artists[final_total.index(x)]}]({x}), "
          final_string = string[:-2]
          image = await self.fetch_from_api(self.bot, activity)
          self.embed.description = f"**Artists**: {final_string}\n**Album**: [{activity.album}]({url})"
          self.embed.set_image(url="attachment://spotify.png")
          return self.embed, image