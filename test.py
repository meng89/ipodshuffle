#!/usr/bin/env python3


class A:

    def __init__(self):
        self._log = {
            '1': {
                'text': 'text',
                'extra': {}
            }
        }

    def get_extra(self):
        return self._log['1']['extra']

    def p(self):
        print(self._log)



a = A()

extra = a.get_extra()

extra['jbm'] = 'jm'

a.p()