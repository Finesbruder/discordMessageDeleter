import discord, os, datetime
from discord.ext import tasks
from dotenv import load_dotenv

class caesarBot:


   def __init__(self, daysUntilDelete=14, loopFrequency=1.0):
      self.client = discord.Client()
      self.daysUntilDelete = daysUntilDelete
      self.deleteFrequency = loopFrequency
      load_dotenv()
      self.token = os.getenv("DISCORD_TOKEN")

   def run(self):
      @self.client.event
      async def on_ready():
         self.deleteEveryOldMessage()

      @tasks.loop(hours=self.deleteFrequency)
      async def cleanHistory():
         try:
            textChannels = self.getEveryTextChannel()
            for channel in textChannels:
               self.deleteOldMessagesFromTextChannel(channel)
         except Exception as e:
            print(e.with_traceback())


      self.client.run(self.token)

   def deleteOldMessagesFromTextChannel(self, channel):
      if channel is None: return

      messages = await channel.history().flatten()
      for msg in messages:
         deletedAfter = datetime.timedelta(days=self.daysUntilDelete)
         if (datetime.datetime.now() - msg.created_at > deletedAfter):
            await msg.delete()

   def getEveryTextChannel(self):
      textChannels = []
      channels = self.client.get_all_channels()
      for channel in channels:
         if (channel.type == discord.ChannelType.text):
            textChannels.append(channel)
      return textChannels


if __name__ == '__main__':
   bot = caesarBot()
   bot.run()

