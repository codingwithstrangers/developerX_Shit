import json
from operator import length_hint
import random
from twitchio.ext import commands, routines
from clientshit import access_token
import os

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
      
        #this will add the user to dic and count 
        # list of users to exclude
        exclude_users = ['Nightbot', 'user1', 'user2']

        if message.author.name not in exclude_users:
            if message.author.name not in self.points_by_chatter.keys():
                self.points_by_chatter[message.author.name]=0
                # rest of the code
        else:
            self.points_by_chatter[message.author.name] += 1
        
        #minus point from user for infractions
        # wight one bad word they wont get any point.

        for i in message.content.split():
            bad_words = ["strainbreh", "fun", "easy", "blender with strangers", "art with strangers", "mod", "my wife is black", "racing game"
                         ,"blm" ]
            if i.lower() in bad_words:   
                if len(message.content) == 1:
                    self.points_by_chatter[message.author.name] -= 0.5  
                else:
                    self.points_by_chatter[message.author.name] -= 1.5
             
        

        #check if user is subscriber or not
        #if they use a channel emote "channel emote and are subbed" they are getting .5 point
        subbed_chatters = ["coding32Thinkmybrother", "coding32Trunks", "coding32Whatmybrother", "coding32Zemi", "coding32Goten", "coding32Heart", "coding32Outofsewer"
                           , "coding32sewer", "coding32Suscoding", "coding32Donny", "coding32What"]
        for x in message.content.split():
            if x in subbed_chatters and message.author.is_subscriber == 1:
                self.points_by_chatter[message.author.name] += .5
                break    
        print(self.points_by_chatter)
        if message.author.is_subscriber:
            print("🌟")
        else:
            print("🌘")
        

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    
    async def perfectstranger(self, ctx: commands.Context):
        if ctx.author.is_broadcaster or ctx.author.is_mod:
            
            sorted_points_chatter = dict(sorted(self.points_by_chatter.items(), key=lambda x: x[1], reverse=True)
            )
            top_three = dict(list(sorted_points_chatter.items())[:3])
            # Here we have a command hello, we can invoke our command with our prefix and command name
            # e.g ?perfectstranger
            # We can also give our commands aliases (different names) to invoke with.

            # Send a hello back!
            # Sending a reply back to the channel is easy... Below is an example.
            

            Ranking_message = await self.leaderboard_snap(sorted_points_chatter)
            await ctx.send(f'{Ranking_message}')



    @commands.command()
    async def addpoints(self, ctx: commands.Context, user, points: int):
        if points > 0:
            if user.id in self.points_by_chatter:
                self.points_by_chatter[user.id] += points
            else:
                self.points_by_chatter[user.id] = points

    def __init__(self):
        
        self.points_by_chatter = {}  # dictionary to store points by user
        self.ranks_by_chatter = {}  # dictionary to store ranks by user
        self.load_data()  # load data from file on initialization

    def load_data(self):
        try:
            with open("leaderboard_data.json", "r") as f:
                data = json.load(f)
                self.points_by_chatter = data["points"]
                self.ranks_by_chatter = data["ranks"]
        except FileNotFoundError:
            print("No leaderboard data found, starting from scratch.")

    def save_data(self):
        data = {"points": self.points_by_chatter, "ranks": self.ranks_by_chatter}
        with open("leaderboard_data.json", "w") as f:
            json.dump(data, f)

    async def finalleaderboard(self, ctx: commands.Context):
        sorted_points_chatter = dict(sorted(self.points_by_chatter.items(), key=lambda x: x[1], reverse=True))

        # Write leaderboard data to file
        with open("leaderboard_data.json", "w") as f:
            json.dump(sorted_points_chatter, f)

        top_three = dict(list(sorted_points_chatter.items())[:3])

        if ctx.author.is_broadcaster:
            # Write top three users to text files
            for t, user in enumerate(top_three.items()):
                with open(f"user{t+1}.txt", "w") as f:
                    f.write(user[0])

        Ranking_message = await self.final_Leaderboard(sorted_points_chatter)
        await ctx.send(f'{Ranking_message}')

    async def leaderboard_snap(self, sorted_chatters):
        Ranking_message = ""
        sorted_points_chatter = dict(sorted(self.points_by_chatter.items(), key=lambda x: x[1], reverse=True))
        
        # Write leaderboard data to file
        with open("leaderboard_data.json", "w") as f:
            json.dump(sorted_points_chatter, f)
            
        top_three = dict(list(sorted_points_chatter.items())[:3])
        for y, (name, points) in enumerate(top_three.items()):
            if y == 0:
                Ranking_message += f"***1st Place: {name} with {points} points is leading the way!***\n"
            elif y == 1:
                Ranking_message += f"2nd Place: {name} with {points} points is not far behind.\n"
            elif y == 2:
                Ranking_message += f"3rd Place: {name} with {points} points will not be ignored.\n"

        '''This will send message to specified channel every 10 seconds for 5 times,
        remove iteration as it will stop after 5 times
        you can send the updated leaderboard here or print it out to console periodically
        '''
        Ranking_message += await self.random_chatter(sorted_points_chatter)
        return Ranking_message


    @routines.routine(hours=1.0, iterations=5)
    async def send_leaderboard(self):
        sorted_points_chatter = dict(sorted(self.points_by_chatter.items(), key=lambda x: x[1], reverse=True))

        # Write leaderboard data to file
        with open("leaderboard_data.json", "w") as f:
            json.dump(sorted_points_chatter, f)
        
        top_three = dict(list(sorted_points_chatter.items())[:3])
        # all_chatters = sorted_points_chatter
        # # Pick a random user and point from the points_by_chatter dictionary
        # random_user, random_points = random.choice(list(self.points_by_chatter.items()))

        Ranking_message = ""
        for y, (name,points) in enumerate(top_three.items()):
            if y == 0:
                Ranking_message+= f"***1st Place: {name} With {points} points is Leading The way coding32Zemi***\n"
            elif y == 1:
                Ranking_message+= f"2nd Place: {name} With {points} points is Not Far Behind coding32Valor***\n"
            elif y == 2:
                Ranking_message+= f"3rd Place: {name} With {points} points Will Not Be Ignored coding32Key***\n"

        '''This will send message to specified channel every 10 seconds for 5 times, 
        remove iteration as it will stop after 5 times
        you can send the updated leaderboard here or print it out to console periodically
        ''' 
        Ranking_message+= await self.random_chatter(sorted_points_chatter)
        

        await self.get_channel("codingwithstrangers").send(Ranking_message)

    async def random_chatter (self, all_chatters):
        #we need all members after the 3rd member
        #We need error checking to confirm our dict has at least 4 members
        #If we have less than 4 members we will return a custom string to show this
        if len(all_chatters)> 3:
            remaining_members = list(all_chatters.keys())[3:]
            
            return f"{random.choice(remaining_members)}, Is in the back but we see you"       
        else:
            return "coding32Suscoding Come on Stranger I know you ain't Stalking and not Talking \n"
            
bot = Bot()
bot.run()
