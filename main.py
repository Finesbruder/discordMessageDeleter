import discord
import os
import datetime
from dotenv import load_dotenv

class caesarBot:


   def __init__(self, daysUntilDelete=14):
      self.client = discord.Client()
      self.daysUntilDelete = daysUntilDelete
      load_dotenv()
      self.token = os.getenv()

   def run(self):
      @self.client.event
      async def on_ready():
         self.deleteEveryOldMessage()

      self.client.run(self.token)

   def deleteOldMessagesFromTextChannel(self, channel):
      messages = await channel.history().flatten()
      for msg in messages:
         deletedAfter = datetime.timedelta(days=self.daysUntilDelete)
         if (datetime.datetime.now() - msg.created_at > deletedAfter):
            await msg.delete()

   def deleteEveryOldMessage(self):
      while True:
         try:
            channels = self.client.get_all_channels()
            for channel in channels:
               if (channel.type == discord.ChannelType.text):
                  self.deleteOldMessagesFromTextChannel(channel)
         except Exception as e:
            print(e.with_traceback())


if __name__ == '__main__':
   bot = caesarBot()
   bot.run()

