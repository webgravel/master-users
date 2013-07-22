import sys

import graveldb
import gravel_master

PATH = '/gravel/system/master'

MIN_UID = 10000

class User(graveldb.Table('users', PATH)):
    default = dict(nick=None, host=None, ready=False)
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

        target.call('user', 'take', str(self.uid))
        self.data.ready = True
        self.save()

    def migrate_out(self):
        self.data.ready = False
        self.save()

        target.call('user', 'return', str(self.uid))

        self.data.host = None
        self.save()

def add(uid):
    with User.table:
        user = User(uid, autocreate=True)
        if not user.exists:
            user.save()
        else:
            sys.exit('User not added - already exists.')
