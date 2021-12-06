import discord
from io import BytesIO
import re
import base64
from typing import List
import urllib
import datetime
from datetime import datetime as dt
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
        self.counter = 0

    async def request_pass(self, *, track_id: str):
        try:
            if not self.bot.spotify_session or dt.utcnow() > self.bot.spotify_session[1]:
                resp = await self.bot.session.post("https://accounts.spotify.com/api/token", params={"grant_type": "client_credentials"}, headers={"Authorization": f'Basic {base64.urlsafe_b64encode(f"{self.bot.spotify_client_id}:{self.bot.spotify_client_secret}".encode()).decode()}', "Content-Type": "application/x-www-form-urlencoded",},)
                auth_js = await resp.json()
                timenow = dt.utcnow() + datetime.timedelta(seconds=auth_js['expires_in'])
                type_token = auth_js['token_type']
                token = auth_js['access_token']
                auth_token = f"{type_token} {token}"
                self.bot.spotify_session = (f"{type_token} {token}", timenow)
                print('Generated new Token')
            else:
                auth_token = self.bot.spotify_session[0]
                print('Using previous token')
        except Exception:
            return False
        else:
            try:
                resp = await self.bot.session.get(f"https://api.spotify.com/v1/tracks/{urllib.parse.quote(track_id)}",
                        params={
                            "market": "US",
                        },
                        headers={
                            "Authorization": auth_token},
                )
                json = await resp.json()
                return json
            except Exception:
                if self.counter == 4:
                    return False
                else:
                    self.counter += 1
                    self.request_pass(track_id=track_id)

    @staticmethod
    async def fetch_from_api(bot, activity: discord.Spotify):
        act = activity
        base_url = "https://api.jeyy.xyz/discord/spotify"
        params = {'title': act.album, 'cover_url': act.album_cover_url, 'artists': act.artists[0], 'duration_seconds': act.duration.seconds, 'start_timestamp': int(act.start.timestamp())}
        connection = await bot.session.get(base_url, params=params)
        buffer = BytesIO(await connection.read())
        return discord.File(fp=buffer, filename="spotify.png")


    async def send_backup_artist_request(self, activity):
        artists = activity.artists
        url = activity.track_url
        result = await self.bot.session.get(url, headers=self.headers)
        text = await result.text()
        my_list = re.findall(self.regex, text)
        final = sorted(set(my_list), key=my_list.index)
        total = len(artists)
        final_total = final[0:total]
        final_string = ', '.join([f"[{artists[final_total.index(x)]}]({x})" for x in final_total])
        return final_string
 

    async def get_embed(self):  
        activity = discord.utils.find(lambda activity: isinstance(activity, discord.Spotify), self.member.activities)
        if not activity:
            return False
        try:
            result = await self.request_pass(track_id=activity.track_id)
            final_string = ', '.join([f"[{resp['name']}]({resp['external_urls']['spotify']})" for resp in result['artists']])
        except Exception:
            final_string = await self.send_backup_artist_request(activity)
        url = activity.track_url
        image = await self.fetch_from_api(self.bot, activity)
        self.embed.description = f"**Artists**: {final_string}\n**Album**: [{activity.album}]({url})"
        self.embed.set_image(url="attachment://spotify.png")
        return self.embed, image