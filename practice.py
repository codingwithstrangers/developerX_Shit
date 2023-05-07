
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
        if message.author.name not in self.points_by_chatter.keys():
            self.points_by_chatter[message.author.name]=0
            '''for optimization the code will only add 1 pt regarless if emote is used with the .5 mult
            need to see if we can add more logic to make it check if emote is being used''' 
        # elif:
        #     #check to see if the user is a subscriber if so and they use subbed_chatter word they get 1.5pt
        #     subbed_chatters and message.author.is_subscriber == 0
        else:
            self.points_by_chatter[message.author.name] += 1
        
        #minus point from user for infractions
        # wight one bad word they wont get any point.

        for i in message.content.split():
            bad_words = ["strainbreh", "fun", "easy", "blender with strangers", "art with strangers", "mod", "my wife is black", "racing game" ]
            if i.lower() in bad_words:   
                if len(message.content) == 1:
                    self.points_by_chatter[message.author.name] -= 0.5  
                else:
                    self.points_by_chatter[message.author.name] -= 1.5
             
        

        #check if user is subscriber or not
        #if they use a channel emote "channel emote and are subbed" they are getting .5 point
        subbed_chatters = ["coding32Thinkmybrother", "coding32Trunks", "coding32Whatmybrother", "coding32Zemi", "coding32Goten", "coding32Heart", "coding32Outofsewer"
                           , "coding32sewer"]
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
    
    async def finalleaderboard(self, ctx: commands.Context):
        def __init__ (self):
            # Initialize a dictionary to store points by chatter, and a dictionary to store ranks by chatter
            self.points_by_chatter = {}
            self.ranks_by_chatter = {}
            # Initialize a dictionary to store rankings for each rank (1st, 2nd, 3rd)
            self.rankings = {1:{}, 2:{}, 3:{}}
        
        async def update_score (self, chatter, points):
            # If the chatter is not in the points dictionary, add them with a score of 0 and an empty rank dictionary
            if chatter not in self.points_by_chatter:
                self.points_by_chatter[chatter] = 0
                self.ranks_by_chatter[chatter] = {}
            # Add the points to the chatter's score
            self.points_by_chatter[chatter] += points

            # Get the rank of the chatter
            rank = self.get_rank(chatter)
            # If the chatter has a rank, update their rank dictionary with the number of times they achieved the rank and their total points
            if rank is not None:
                if rank in self.ranks_by_chatter[chatter]:
                    self.ranks_by_chatter[chatter][rank][0] += 1 
                    self.ranks_by_chatter[chatter][rank][1] += points
                else:
                    self.ranks_by_chatter[chatter][rank] = [points, 1]
            #come back and see this shit
        
        def get_rank(self, chatter):
            #sort the chatters in order by decending order
            sorted_chatters = sorted(self.points_by_chatter.items(), key=lambda x: x[1], reverse=True)
            rank = None

            # Loop through the sorted chatters, find the rank of the given chatter, and return it
            for i, c in enumerate(sorted_chatters):
                if c[0] == chatter:
                    rank = i + 1
                    break
                return rank 
            
        async def final_leaderboard(self, ctx: commands.Context):
            # Sort the points by chatter in descending order
            sorted_points_chatter = dict(sorted(self.points_by_chatter.items(), key=lambda x: x[1], reverse=True))
            # Get the top three chatters
            top_three = dict(list(sorted_points_chatter.items())[:3])
            # If the caller is a broadcaster, write the top three chatters to text files
            if ctx.author.is_broadcaster:
                for t, user in enumerate(top_three.items()):
                    with open(f"user{t+1}.txt", "w") as f:
                        f.write(user[0])
            # Get the final leaderboard message and send it
            ranking_message = await self.final_leaderboard_message(sorted_points_chatter)
            await ctx.send(f'{ranking_message}')
                 
        async def final_Leaderboard_message (self, sorted_points_chatter):
              # Initialize a list of messages to build the final message
            messages = []
            # Loop through the rankings
            for rank, chatters in self.rankings.items():
                messages.append(f"\n{rank}st: ")
                #Loop through chatters in ranking and add their info for the message
                for chatter, data in chatters.items():
                    frequency = data[0]
                    points = data[1]
                    messages.append(f"{chatter} ({frequency} x {rank} {points} points), ")
            # Join the messages together and return the final message
            return ''.join(messages)
        

        # sorted_points_chatter = dict(sorted(self.points_by_chatter.items(), key=lambda x: x[1], reverse=True)
        # )
        # top_three = dict(list(sorted_points_chatter.items())[:3])
        # if ctx.author.is_broadcaster:
                    
        #     #Write top three users to text files
        #     for t, user in enumerate(top_three.items()):
        #         with open(f"user{t+1}.txt", "w") as f:
        #             f.write(user[0])

        
        # Ranking_message = await self.final_Leaderboard(sorted_points_chatter)
        # await ctx.send(f'{Ranking_message}')



    async def leaderboard_snap (self, sorted_chatters):
        
        Ranking_message = ""
        sorted_points_chatter = dict(sorted(self.points_by_chatter.items(), key=lambda x: x[1], reverse=True)
        )
        top_three = dict(list(sorted_points_chatter.items())[:3])
        for y, (name,points) in enumerate(top_three.items()):
            if y == 0:
                Ranking_message+= f"***1st Place: {name} With {points} points is Leading The way coding32Zemi *** \n"
            elif y == 1:
                Ranking_message+= f"2nd Place: {name} With {points} points is Not Far Behind coding32Valor *** \n"
            elif y == 2:
                Ranking_message+= f"3rd Place: {name} With {points} points Will Not Be Ignored coding32Key *** \n"

        '''This will send message to specified channel every 10 seconds for 5 times, 
           remove iteration as it will stop after 5 times
           you can send the updated leaderboard here or print it out to console periodically
        ''' 
        Ranking_message += await self.random_chatter(sorted_points_chatter)
        return Ranking_message    
        
    
# ******************
    @routines.routine(hours=1.0, iterations=5)
    async def send_leaderboard(self):
        sorted_points_chatter = dict(sorted(self.points_by_chatter.items(), key=lambda x: x[1], reverse=True)
        )
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
            return "coding32Thinkmybrother Come on Stranger I know you ain't Stalking and not Talking \n"
            
bot = Bot()
bot.run()
