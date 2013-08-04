#!/usr/bin/env python
import sys
import argparse

sys.path.append('/gravel/pkg/gravel-common')
sys.path.append('/gravel/pkg/gravel-master')

import gravel_master
import users
import cmd_util

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

def action_custom():
    parser = argparse.ArgumentParser()
    parser.add_argument('uid', type=int)
    parser.add_argument('customname', default='list')
    args = parser.parse_args()

    comment = 'Editing %s custom config for %d.' % (args.customname, args.uid)

    user = users.User(args.uid)
    user.data.custom[args.customname] = cmd_util.run_yaml_editor(
        comment,
        user.data.custom.get(args.customname, {}))
    user.save_custom()
    user.save()

if __name__ == '__main__':
    cmd_util.main_multiple_action(globals())
