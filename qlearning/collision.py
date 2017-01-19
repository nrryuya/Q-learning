from qlearning import QLearning
import sys
import os
import random
sys.path.append(os.pardir)


# 状態、報酬、行動は辞書型(キーはリスト型で、Aがi、Bがｊなら、[i,j]などと表す。)
# Bの動きが単純で、起こりうる状態が限られているが、そうでない場合は、Bの動きを記述するメソッドを書き、actionとdestinationを対応させればよい。
class Collision(QLearning):

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

    # 結果を分かりやすく表示するメソッド
    def result(self, t_max, n_round):
        q = self.learn(t_max, n_round)
        for state in self.states:
            for action in range(len(self.actions(state))):
                destination = self.actions(state)[action]
                print("状態[", state, "から", destination,
                      "のQ値は", self.Q(state, action))


# 予め状態集合が分からない場合はどうするのか？状態集合を広めに作っておき、その中に実際生じない状況があっても問題ないか？
def make_states():
    states = []
    for a in range(10):
        for b in range(10):
            states.append([a, b])
    return states
#     #Bが到着するまで。0~4番目の状態を想定。
#     for k in range(0,5):
#         state.append([k,4-k])
#         state.append([k+4,5-k])
#     #Bが0に着いて以降。5,6回目の行動。
#     for k in range(5,7):
#         state.append([k+4,5-k])


def make_rewards(states):
    rewards = {}
    # 一旦すべてに同じ値を与える
    for state in states:
        # 衝突の場合の報酬。報酬の初期値という設定は用いず、とりあえず-100でやってみる。また、問題次第ではi=j以外に「すれ違う」タイプの衝突もあり得る。
        if state[0] == state[1]:
            rewards[state] = -100
        else:
            rewards[state] = -5
    return rewards

# 一旦0~3,5~8に横移動を加えておいて、そのあとに他をやる、という手もある。


def make_actlist(states):  # AだけでなくBの変化も記述する。
    actlist = {}
    for state in states:
        a = state[0]
        b = state[1]
        actlist[state] = []
        # Aが0~3のとき
        if a in range(0, 4):
            if b == 0:
                actlist.append([a + 1, 0])
                actlist.append([a + 4, 0])
            else:
                actlist.append([a + 1, b - 1])
                actlist.append([a + 4, b - 1])
        # Aが5~8のとき。
        if a in range(5, 9):
            if b == 0:
                actlist.append([a + 1, 0])
            else:
                actlist.append([a + 1, b - 1])
        # Aが9のとき。問題設定上確実にBは0かつAは上に行くしかない。
        if a == 9:
            actlist.append([4, 0])

    return actlist


def make_terminals(states):
    terminals = []
    terminals.append([0, 4])
    for state in states:
        if state[0] == state[1]:
            terminals.append(state)
    return terminals


# stateが[x,y]→Aがxに、Bがyにいる。升目上の位置は0~9までの数字で表す。
states = make_states()
rewards = make_rewards(states)  # 各マスの報酬=-5
actlist = make_actlist(states)
terminals = make_terminals(states)

init = [0, 4]
arfa = 0.1
gamma = 0.9

c = Collision(states, rewards, actlist, init, terminals, arfa, gamma)
c.result(30, 30)
