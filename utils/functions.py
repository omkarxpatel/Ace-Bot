import discord
from io import BytesIO

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