#!/usr/bin/env python2.7
import sys
import argparse

sys.path.append('/gravel/pkg/gravel-common')
sys.path.append('/gravel/pkg/gravel-master')

import cmd_util
import gravel_master
import users

target_node = gravel_master.get_node()

for user in users.User.all():
    if user.data.host == target_node.name:
        user.save_custom()
