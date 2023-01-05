#pull everything 
from twitchio.ext import commands, routines
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

        #this is how the routine starts
        self.send_leaderboard.start()
        


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
            print("🌕")
        

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

    '''
    Bot account need to be mod to work
    PARAMETERS
    seconds: The seconds to wait before the next iteration of the routine.
    minutes: The minutes to wait before the next iteration of the routine.
    hours: The hours to wait before the next iteration of the routine.
    time: A specific time to run this routine at. If a naive datetime is passed, your system local time will be used.
    iterations: The amount of iterations to run this routine before stopping. If set to None or 0, the routine will run indefinitely.
    wait_first: Whether to wait the specified time before running the first iteration. This has no effect when the time argument is used. Defaults to False.'''

    @routines.routine(seconds=10.0, iterations=5)
    async def send_leaderboard(self):
        sorted_points_chatter = dict(sorted(self.points_by_chatter.item(), key=lambda x: x[1], reverse=True)
        )
        top_three = dict(list(sorted_points_chatter.items())[:3])
        
        def ordinal(n):
	        return f"{n}{dict({1: 'st', 2: 'nd', 3: 'rd'}).get(4 if 10 <= n % 100 < 20 else n % 10, 'th')}"
        
        Ranking_message = ""
        for n, (name, point) in enumerate(top_three.items(), 1):
            Ranking_message += f"{ordinal(n)} Place: {name} With {point} Points"

        print(Ranking_message)

        '''This will send message to specified channel every 10 seconds for 5 times, 
           remove iteration as it will stop after 5 times
           you can send the updated leaderboard here or print it out to console periodically
        ''' 
        
        await self.get_channel("codingwithstrangers").send("Test")

bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.
