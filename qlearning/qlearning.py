# import numpy as np
import random

# 要はstatesの形式により諸々のアクセスの仕方が変わっているだけなので、アクセスの仕方をメソッドとして場合分けするだけでいい気がする

# actlistが確率的なときは、actionとdestinationを対応させるメソッドを書き、actlistはそれで表現する。
# Q値の更新や、最大のQ値をとるアクションとかは、期待値でやる？


class QLearning:

    def __init__(self, states, rewards, actlist, init, terminals, arfa, gamma):  # 状態集合は具象クラスで作る。
        self.states = states  # 辞書型またはn次元行列を表現するリスト型
        self.rewards = rewards
        self.actlist = actlist
        self.init = init
        self.terminals = terminals
        if not (0 <= gamma < 1):
            raise ValueError("An MDP must have 0 <= gamma < 1")
        self.arfa = arfa
        self.gamma = gamma

    # Q値に初期値を与えるメソッド
    def init_q(self):
        pass

    # ある状態のある行動のQ値を数値型で返すメソッド。ある状態に対するQ値のリストは、actionをインデックスとするリスト型である。
    def Q(self, state, action):
        return None

    # Q値を更新するメソッド
    def update_q(self, state, action, new_value):
        pass

    # ある状態の報酬を数値型で返すメソッド
    def R(self, destination):
        return None

    # ある状態においてとれる行動の集合をリスト型で返すメソッド。このリストのインデックスが行動の名前、要素が目的地を表す。
    def actions(self, state):
        return [None]

    # ある状態においてとれる行動それぞれのQ値をリスト型(インデックスは行動リストのインデックスと同じ)で返すメソッド。
    def q_list(self, state):
        q_list = []
        for action in range(len(self.actions(state))):
            q_list.append(self.Q(state, action))
        return q_list

    # ある状態においてQ値が最大となる行動のインデックスとQ値をリスト型で返す。行先が確率的に決まる場合は期待値が最大なアクションを返す。
    def max_q(self, state):
        if state in self.terminals:
            max_action = None
            max_q = 0
        else:
            max_action = self.q_list(state).index(
                max(self.q_list(state)))  # 最大が二つある場合は小さい方のインデックスを返す←OK?
            max_q = max(self.q_list(state))
        return [max_action, max_q]

    # ε-greedy法で行動を決定する。
    def e_greedy(self, state, epsilon=0.0001):
        if random.random() > epsilon:  # Q値が最大な行動を選ぶ
            action = self.max_q(state)[0]
            destination = self.actions(state)[action]
        else:  # 探索
            action = random.randrange(len(self.actions(state)))
            destination = self.actions(state)[action]

        return [action, destination]

    def learn(self, t_max, n_round):  # t_max回の推移を1ラウンドとして、nラウンド繰り返す。行動選択はε-greedy法

        # Q値を初期化
        self.init_q()

        # 反復の準備
        n = 0
        t = 0
        # 反復
        while n < n_round:
            state = self.init
            while t < t_max:
                # terminalsに来たら初めからにする
                if state in self.terminals:
                    break
                else:
                    # ε-greedyで行動決定
                    action = self.e_greedy(state)[0]
                    destination = self.e_greedy(state)[1]

                    # Q値を更新。行動と行先が確率的に決まる場合、actionを決めたときに更新するのか？行先が決まってから更新するのか？
                    new_value = self.Q(state, action) + self.arfa * (self.R(state) +
                                                                     self.gamma * self.max_q(destination)[1] - self.Q(state, action))
                    self.update_q(state, action, new_value)

                    state = destination  # 状態推移
                    t += 1
            n += 1

        return self.q


# 要素が数値0のm×n行列を生成するメソッド
def make_matrix(m, n):
    matrix = []
    for i in range(m):
        matrix.append([])
        for j in range(n):
            matrix[i].append(0)
    return matrix

# 要素がリストのm×n行列を生成するメソッド


def make_matrix_list(m, n):
    matrix = []
    for i in range(m):
        matrix.append([])  # 要素がリストな行をm行追加
        for j in range(n):
            matrix[i].append([])
    return matrix


# 状態を表現する行列を生成するメソッド
def make_states(m, n):
    states = make_matrix(m, n)
    for i in range(m):
        for j in range(n):
            states[i][j] = [i, j]
    return states

# 偶奇でかんがえればすぐわかるが、stateのうちのありえない状態がたくさん書かれている。
# m×n行列で表せる状態集合上で上下左右斜めに動けるときの行動の集合


def make_actlist(m, n):
    actlist = make_matrix(m, n)
    for i in range(m):
        for j in range(n):
            actlist[i][j] = []
            for p in [-1, 0, 1]:
                for q in [-1, 0, 1]:
                    k = i + p
                    l = j + q
                    if p == 0 & q == 0:  # その場に留まることは無いとする
                        pass
                    elif not(k == -1 or k == m or l == -1 or l == n):  # not(上下左右どちらかハミ出てしまったとき)
                        actlist[i][j].append([k, l])  # actlist[i][j]の何番目かにリスト型の要素が追加された。

    return actlist
