import random
from time import perf_counter
import time 
GAME_BOARD = 23

class Player:
    '''player1 = Player(1, 'aman108')
        print(player1)
        print(player1.move(31))'''
    def __init__(self, num, name):        
        self.num = num
        self.name = name
        self.moved = 0
        self.position = 0
        self.wins = 0
            
    def __str__(self):
        return 'Player {num}: {name}'.format(num = self.num, name = self.name)
    
    __repr__ = __str__
    
    def move(self, position):
        self.moved = position
        self.position += position
        return 'Player {num} moved to {position}'.format(num = self.num, position = self.position)
        
class Cop(Player):
    def __init__(self, num, name):
        super().__init__(num, name)        
        self.position = self.__set_position   
        self.arrests = 0
        self.money_recovered = 0
    
    def __str__(self):
        return 'Cop {num}: {name}'.format(num = self.num, name = self.name)
    
    __repr__ = __str__     
    
    @property
    def __set_position(self):
        return random.randint(0, GAME_BOARD)
    
    def move(self):
        position = self.__set_position     
        self.moved = position 
        self.position += position   
        print('Cop {num} moved to {position}'.format(num = self.num, position = self.position))
    
    def culpritCaught(self, culprit):
        if 0 <= abs(self.position - culprit.position) <= 1:
            self.arrests += 1
            self.money_recovered = 0            
            return True    
    
class Robber(Player): 
    def __init__(self, num, name):       
        super().__init__(num, name)
        self.position = self.__set_position  
        self.robberies = 0
        self.money = 0               
    
    def __str__(self):
        return 'Robber {num}: {name}'.format(num = self.num, name = self.name)    
    
    __repr__ = __str__
    
    @property
    def __set_position(self):
        return random.randint(0, GAME_BOARD)
    
    def move(self):
        super().move(self.position)
        print('Robber {num} moved to {position}'.format(num = self.num, position = self.position))

    def steal(self, loot):
        if self.position == loot.position:
            self.robberies += 1
            self.money += loot.points
            return True
    
    def caught(self, loot):
        self.money -= loot.points
        self.is_caught =  True
        
class GameObject:
    def __init__(self, name, points_gained):
        self.id = self.__objectID
        self.name = name
        self.points_gained = points_gained
    
    def __str__(self):
        return "{id} {name} : {pts}".format(id = self.id,name = self.name, pts = self.points_gained)
    
    __repr__ = __str__ 
    
    @property
    def __objectID(self):
        return str(random.randint(0, 100))
    
    def setPointsGained(self, new_points):
        self.points_gained = new_points  
        
    def setLootPosition(self): 
        self.position = random.randint(0, GAME_BOARD)   

class Rounds:
    def __init__(self, num, length):
        self.num = num
        self.start_round = 0
        self.length = length
        
    def __str__(self):
        return '{num} rounds run for {length} seconds'.format(num = self.num, length = self.length)
    
    __repr__ = __str__    
    
class Game:
    def __init__(self, players, game_objects):
        self.players = {player.num : player for player in players}        
        self.game_objects = game_objects   
        self.current_round = 0   
    def __str__(self):
        return '{players} have to secure or steal {object} in this game!'.format(players = ', '.join([player.name for player in self.players.values()]), object = self.game_objects.name)
    __repr__ = __str__      

class CopsAndRobbers:
    def __init__(self, players):
        self.players = players        
        self.current_round = 0 
        self.rounds = self.setRounds()
        self.loot = self.setLoot()
        self.startTime = 0
        self.team_size = 0
            
    def setLoot(self, loot_name = "loot", loot_amount = 0):
        self.loot = GameObject(loot_name, loot_amount)        
    
    def setRounds(self, rounds = 1, round_length=60):
        self.rounds = Rounds(rounds, round_length)
    
    def timeRound(self):        
        return time.time()     
       
    def makeMeCop(self, player):
        return Cop(player.num, player.name) 
    
    def makeMeRobber(self, player):
        return Robber(player.num, player.name)
    
    def makeTeams(self, players):
                half = (len(players)//2) - 1
                self.team_size = half
                self.cops = [self.makeMeCop(player) for player in players[half:]]
                self.robbers = [self.makeMeRobber(player) for player in players[:half]]       
    
    def playRound(self):    
        self.startTime = self.timeRound()
        while self.timeRound() - self.startTime < self.rounds.length:                               
            for each in range(self.team_size):
                cop, robber = self.cops[each], self.robbers[each]                
                robber.move()
                cop.move()                
                
                if 1 < abs(cop.position - robber.position) < 5:
                    print("{cop} is getting closer to {robber}...watch out!".format(cop = cop.name, robber = robber.name))
                
                if cop.culpritCaught(robber):  
                    robber.caught()
                    cop.money_recovered = self.loot.points_gained                                      
                    return '{cop} has caught {robber} and recovered ${loot}!'.format(cop = cop.name, robber = robber.name, loot = self.loot.loot_amount)
                
                if robber.robberies(self.loot):
                    return 'Oh no! {robber} has stolen the {loot} worth ${amt}!'.format(robber = robber.name, loot = self.loot.name, amt = self.loot.loot_amount) 
        return 'Oh no, Team Robbers has escaped! Better luck next time.'
                
    def playGame(self):
        self.makeTeams(self.players)
        self.loot.setLootPosition()
        for round in range(self.rounds.num):
            self.current_round += 1           
            print(self.playRound())
        return self.results()
    
    def results(self):
        tie_messages = "It was a tie! Better luck next time Team Cops and Team Robbers."
        cops_wins = sum(cop.arrests for cop in self.cops)
        robbers_wins = sum(robber.robberies for robber in self.robbers)
        print(robbers_wins, cops_wins)
        if  cops_wins < robbers_wins:
            winner , winnings = "Robbers", abs(cops_wins - robbers_wins)
        elif  cops_wins > robbers_wins:
            winner , winnings = "Cops", abs(cops_wins - robbers_wins)
        else:
            return tie_messages
        return "{winner} won by {winnings}!".format(winner = winner, winnings = winnings)
    
            
'''                 
player1 = Player(1, "divya108")
player2 = Player(2, "aman108")
players = [player1, player2]

newGame = CopsAndRobbers(players)
newGame.setRounds(10, 3)
newGame.setLoot("Diamond Ring", 4000)
print(newGame.playGame())
'''