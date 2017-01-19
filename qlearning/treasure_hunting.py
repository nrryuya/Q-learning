from qlearning import QLearning
import sys
import os
sys.path.append(os.pardir)

# 状態、報酬、行動は辞書型(本門の場合は状態を整数で表せるので一次元のリストでも可能)


class Treasure_Hunting(QLearning):

    def __init__(self, states, rewards, actlist, init, terminals, arfa, gamma):
        super().__init__(states, rewards, actlist, init, terminals, arfa, gamma)

    def init_q(self):
        self.q = {}
        for state in self.states:
            self.q[state] = []
            if state in self.terminals:
                self.q[state] = [None]
            else:
                for action in range(len(self.actions(state))):
                    self.q[state].append(1)

    def Q(self, state, action):
        return self.q[state][action]

    def update_q(self, state, action, new_value):
        self.q[state][action] = new_value

    def R(self, state):
        return self.rewards[state]

    def actions(self, state):
        if state in self.terminals:
            return [None]
        else:
            return self.actlist[state]


states = range(1, 6)
rewards = {1: -10, 2: 0, 3: 0, 4: 0, 5: 10}
actlist = {1: [None], 2: [1, 3], 3: [2, 4], 4: [3, 5], 5: [None]}
init = 3
terminals = [1, 5]
arfa = 0.8
gamma = 0.5

# なぜかQの初期値を全て0にすると上手くいかなかった。
t = Treasure_Hunting(states, rewards, actlist, init, terminals, arfa, gamma)
print(t.learn(30, 30))
