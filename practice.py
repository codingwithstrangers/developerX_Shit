#pull everything 
import time
import os
from twitchio.ext import commands
from clientshit import access_token

class Bot(commands.Bot):
    points_by_chatter = {}
    


    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        
        super().__init__(token= access_token , prefix='?', initial_channels=['codingwithstrangers'],
            nick = "Perfect_Stranger")

    async def event_ready(self):
       
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
    # Messages with echo set to True are messages sent by the bot...
    # For now we just want to ignore them...
        if message.echo:
            return

        # check if the message starts with the command prefix
        if message.content.startswith('?perfectstranger'):
            # run the send_leaderboard routine
            await self.send_leaderboard()
            return

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message.content.encode("utf-8"))
        print(message.author.name)
             
    
        

        #this will add theuser to dic and count 
        if message.author.name not in self.points_by_chatter.keys():
            self.points_by_chatter[message.author.name]=0
            
        else:
            self.points_by_chatter[message.author.name] += 1
        
        #minus point from user for infractions
        # wight one bad word they wont get any point.

        for i in message.content.split():
            bad_words = ["strainbreh", "fun", ]
            if i.lower() in bad_words:   
                if len(message.content) == 1:
                    self.points_by_chatter[message.author.name] -= 0.5  
                else:
                    self.points_by_chatter[message.author.name] -= 1.5
             
        

        #check if user is subscriber or not
        #if they use a channel emote "channel emote and are subbed" they are getting .5 point
        subbed_chatters = ["coding32Thinkmybrother", "coding32Trunks", "coding32Whatmybrother", "coding32Zemi", "coding32Goten"]
        for x in message.content.split():
            if x in subbed_chatters and message.author.is_subscriber == 1:
                self.points_by_chatter[message.author.name] += .5
                break    
        print(self.points_by_chatter)
        if message.author.is_subscriber:
            print("🌟")
        else:
            print("🌘 ")

        #this will sort and keep to a top 10
        sorted_points_by_chatter = dict(sorted(self.points_by_chatter.items(), key=lambda x: x[1], reverse=True))
        top_ten = dict(list(sorted_points_by_chatter.items())[:10])
        print(top_ten)


        #write this to a text file
        ## specify the directory
        directory = "F:\Coding with Strangers\Twitchbot\perfectstrangerbot"

        # create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # open a file in append mode
        with open(os.path.join(directory, 'points.txt'), 'a') as f:
            # get current time
            timestamp = time.time()

            # convert timestamp to readable format
            readable_time = time.ctime(timestamp)

            # write the timestamp and points to the file
            f.write(readable_time + '\n')
            for name, points in top_ten.items():
                f.write(name + ': ' + str(points) + '\n')

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f'Hello {ctx.author.name}!')


bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.