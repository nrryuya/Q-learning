from qlearning import QLearning, make_matrix, make_states, make_actlist
import sys
import os
import random
sys.path.append(os.pardir)

# 状態、報酬、行動はリストによる二次元の行列で与える。(辞書のキーにリスト型を使えないため)


class Shortest_Path(QLearning):

    def __init__(self, states, rewards, actlist, init, terminals, arfa, gamma):
        super().__init__(states, rewards, actlist, init, terminals, arfa, gamma)

    def init_q(self):  # Q値は、要素が行動のリストであるm×nの行列
        m = len(self.states)
        n = len(self.states[0])
        self.q = make_matrix(m, n)

        for i in range(m):
            for j in range(n):
                self.q[i][j] = []
                if [i, j] in self.terminals:
                    self.q[i][j] = [None]
                else:
                    for action in range(len(self.actions([i, j]))):
                        self.q[i][j].append(random.random())

    # self.qは行列のi行j列目の値としてQ値を返すが、状態を[i,j]という形式で読み込んで返せるようにしている。
    def Q(self, state, action):  # stateは[i,j]という形式で表現される。
        return self.q[state[0]][state[1]][action]

    def update_q(self, state, action, new_value):
        self.q[state[0]][state[1]][action] = new_value

    def R(self, state):
        return self.rewards[state[0]][state[1]]

    def actions(self, state):
        if state in self.terminals:
            return [None]
        else:
            return self.actlist[state[0]][state[1]]

    # 結果を分かりやすく表示するメソッド
    def result(self, t_max, n_round):
        q = self.learn(t_max, n_round)
        m = len(self.states)
        n = len(self.states[0])
        for i in range(m):
            for j in range(n):
                for action in range(len(self.actions([i, j]))):
                    destination = self.actions([i, j])[action]
                    print("位置[", i, ",", j, "]から", destination, "のQ値は", self.Q([i, j], action))


states = make_states(3, 3)

# リストの生成が面倒なのでstatesの値を変更することでrewardsを作る。
rewards = states

rewards[2][0] = -1
rewards[1][0] = -1
rewards[0][0] = -1
rewards[2][1] = -1
rewards[1][1] = -1
rewards[0][1] = -1
rewards[2][2] = -1
rewards[1][2] = -1
rewards[0][2] = 1

actlist = make_actlist(3, 3)
init = [2, 0]
terminals = [[0, 2]]
arfa = 0.8
gamma = 0.5

s = Shortest_Path(states, rewards, actlist, init, terminals, arfa, gamma)
s.result(30, 30)
