import weakref

class Team:
    Instance_Arr = []
    
    # Teams start with a Score of 200.
    Initial_Score = 200

    # Penalty of 10 points for wrong submisisons.
    Penalty = -10
    
    def __init__(self, Name, Token):
        # Each Team is given a private Token to authenticate their submissions.
        self.__class__.Instance_Arr.append(weakref.proxy(self))

        self.Name = Name
        self.Score = Team.Initial_Score
        self.Joker = None
        self.Token  = Token
        self.Submission_History = set([])

    def Pick_Joker(self, ID):
        # Teams can Pick one of the Tasks to coint double.
        # This choice can only be made once.
        
        if self.Joker is None:
            self.Joker = int(ID)
            return True
        else:
            return False

    def Submit(self, ID, Submission):

        # Check, if Submission was seen before        
        if (ID,Submission) in self.Submission_History:
            return 0
        else:
            self.Submission_History.add((ID,Submission))
        
        # Check Solution
        if Submission == Task[ID].Solution :
            # Success. Get Points.
            multiplier = 2 if ID == self.Joker else 1             
            points = Task[ID].get_current_value() * multiplier
            
            self.Score = self.Score + points
            Task[ID].Number_of_Solutions = Task[ID].Number_of_Solutions + 1
            
            return points

        else:
            # Nope. Receive Penalty.
            self.Score = self.Score + Team.Penalty if self.Score + Team.Penalty >= 0 else 0
            return Team.Penalty

        
    def __class_getitem__(cls, name):
        return Team.Instance_Arr[ID-1]
            
    def __repr__(self):
        return f'{self.Name}'
        
    def get_Team(Token):
        for T in Team.Instance_Arr:
            if T.Token == Token:
                return T
        return None
