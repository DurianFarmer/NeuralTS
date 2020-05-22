from data import Bandit
from learner import LinearTS, NeuralTS
import numpy as np
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Linear Thompson Sampling')
    parser.add_argument('--dataset', default='mushroom', metavar='DATASET', help='dataset used for training')
    parser.add_argument('--nu', type=float, default=1, metavar='v', help='nu for control variance')
    parser.add_argument('--lamdba', type=float, default=1, metavar='r', help='lambda for regularzation')
    parser.add_argument('--shuffle', type=bool, default=1, metavar='1 / 0', help='shuffle the data set or not')
    parser.add_argument('--seed', type=int, default=0, help='random seed for shuffle, 0 for None')
    parser.add_argument('--r', type=float, default=0.9, metavar='r', help='ratio for feature norm')
    args = parser.parse_args()
    seed = None if args.seed == 0 else args.seed
    b = Bandit(args.dataset, args.shuffle, args.seed, args.r)
    l = NeuralTS(b.dim, args.lamdba, args.nu)
    rewards = []
    cache = 0
    for t in range(b.size):
        context, arm = b.step()
        arm_select = l.select(context)
        if arm == arm_select:
            r = 1
        else:
            r = 0
        loss = l.train(context[arm_select], r)
        rewards.append(r)
        print('{}: {:.3f}, {:.3e}'.format(t, np.mean(rewards), loss))