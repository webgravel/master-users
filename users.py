import sys

import gravelrpc
import graveldb
import gravel_master
import cmd_util
import random

PATH = '/gravel/system/master'

MIN_UID = 10000
MAX_UID = 99999

class User(graveldb.Table('users', PATH)):
    default = dict(nick=None, host=None, ready=False,
                   custom={})
    autocreate = False

    def validate(self):
        if self.uid < MIN_UID:
            raise ValueError('uid too small')
        if not self.data.nick:
            self.data.nick = 'u%d' % self.uid

    @property
    def uid(self):
        return self.name

    def set_host(self, target):
        assert isinstance(target, gravel_master.Node)
        if self.data.host:
            self.migrate_out()

        with self:
            if self.data.host:
                raise graveldb.RaceConditionError()
            self.data.host = target.name
            self.save()

        self.save_custom()
        self.data.ready = True
        self.save()

    def save_custom(self):
        '''
        I'll update custom settings on user's host.
        '''
        if self.data.host:
            target = gravel_master.Node(self.data.host)
            target.call('user', 'take', str(self.uid),
                        func=cmd_util.call_with_stdin,
                        stdin_data=gravelrpc.bson.dumps(self.data.custom))

    def migrate_out(self):
        '''
        I'll ask user's host to stop being host and then save the fact
        to db.
        '''
        self.data.ready = False
        self.save()

        target = gravel_master.Node(self.data.host)
        target.call('user', 'return', str(self.uid))

        self.data.host = None
        self.save()

def add(uid=-1):
    '''
    I will create user with given uid and return uid of created user.
    If uid == -1, I'll find free one.
    '''
    find_uid = uid == -1
    if find_uid:
        uid = random.randrange(MIN_UID, MAX_UID)
    with User.table:
        user = User(uid, autocreate=True)
        if not user.exists:
            user.save()
            return uid
        else:
            if find_uid:
                # collision - try again
                return add(uid=-1)
            else:
                raise KeyError(uid)
