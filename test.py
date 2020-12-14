from source import reactionBalance

'''this tests evaluates the effectiveness of the class'''
reaction1 = reactionBalance("2.0","1.0","500.0")
print("Reaction1")
reaction1.saveData()
print("Reaction2")
reaction2 = reactionBalance(2.0,1.0,500.0)
reaction2.saveData()