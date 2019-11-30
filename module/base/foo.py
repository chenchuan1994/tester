class Gizmo:

    def __init__(self):
        print('Gizmo id: %d' % id(self))

x = Gizmo()

print(dir())

charles = {'name':'Charles L. Dodgson', 'born':1832}
lewis = charles
print(lewis is charles)
print(id(charles), id(lewis))
lewis['balance'] = 950
print(charles)

alex = {'name':'Charles L. Dodgson', 'born':1832}
print(id(alex))

l1 = [3, [66, 55, 44], (7, 8, 9)]
l2 = list(l1) # ➊
l1.append(100) # ➋
l1[1].remove(55) # ➌
print('l1:', l1)
print('l2:', l2)
l2[1] += [33, 22] # ➍
l2[2] += (10, 11) # ➎
print('l1:', l1)
print('l2:', l2)

print(id(l1), id(l2))

class HauntedBus:
    """备受幽灵乘客折磨的校车"""
    def __init__(self, passengers=[]): 
        self.passengers = passengers
    def pick(self, name):
        self.passengers.append(name) 
    def drop(self, name):
        self.passengers.remove(name)