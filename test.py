#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class A:
    def __init__(self):
        self.s = [1, 2]

        class B:
            def __init__(cls):
                cls.s = self.s
        self.b = B()


a = A()
b = A()
a.b.s.append(3)
print(a.s)
print(b.s)