#!/usr/bin/env python
import sys
import argparse

sys.path.append('/gravel/pkg/gravel-common')
sys.path.append('/gravel/pkg/gravel-master')

import gravel_master
import users

def action_add():
    parser = argparse.ArgumentParser()
    parser.add_argument('uid', type=int)
    args = parser.parse_args()

    users.add(args.uid)

def action_sethost():
    parser = argparse.ArgumentParser()
    parser.add_argument('uid', type=int)
    parser.add_argument('node')
    args = parser.parse_args()

    users.User(args.uid).set_host(gravel_master.get_one_node(args.node))

if __name__ == '__main__':
    actions = ['add', 'sethost']
    if len(sys.argv) < 2 or sys.argv[1] not in actions:
        sys.exit('Usage: {} {} ...'.format(sys.argv[0], '|'.join(actions)))
    action = sys.argv[1]
    del sys.argv[1:2]
    sys.argv[0] += ' ' + action
    globals()['action_' + action]()
