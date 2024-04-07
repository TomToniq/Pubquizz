import weakref

class Task:
    Instance_Arr = []

    # Tasks are worth 20 points initially.
    Initial_Value = 20

    # First 3 Teams to solve a task Get the following bonus points.
    Bonus_Points = {
        0:15,
        1:10,
        2:5
    }
    
    def __init__(self, Text, Solution):
        self.__class__.Instance_Arr.append(weakref.proxy(self))
        
        self.ID = len(Task.Instance_Arr)
        self.Solution = Solution
        self.Text = Text
        self.Number_of_Solutions = 0
    
    def __class_getitem__(cls, ID):
        return Task.Instance_Arr[ID-1]
    
    def __repr__(self):
        return f'Task {self.ID:d} [{self.get_current_value():d}]: {self.Text}'


    def get_current_value(self):
        return Task.Initial_Value + Task.Bonus_Points[self.Number_of_Solutions]
    
