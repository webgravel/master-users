#!/usr/bin/env python
import sys
import argparse

def action_add():
    parser = argparse.ArgumentParser()
    parser.add_argument('uid', type=int)
    args = parser.parse_args()

if __name__ == '__main__':
    actions = ['add']
    if len(sys.argv) < 2 or sys.argv[1] not in actions:
        sys.exit('Usage: {} {} ...'.format(sys.argv[0], '|'.join(actions)))
    action = sys.argv[1]
    del sys.argv[1:2]
    sys.argv[0] += ' ' + action
    globals()['action_' + action]()
