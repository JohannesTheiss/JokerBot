#import matplotlib.pyplot as plt
import numpy as np
import sympy as sy
import inspect
import ast
import sys


class Integration:

    def getSymbolsFromString(self, s):
        symbols = ['x', 'y', 'z']
        res = []
        for c in s:
            if c in symbols:
                res.append(c)

        return res


    def parse(self, expression):
        operators = set('+-*/^')
        safe = False
        ex = expression.replace(" ", "")
        i = 0
        for c in ex:
            if safe:
                if c == ")":
                    pass
                elif c.isnumeric():
                    pass
                elif c in operators:
                    safe = not safe
                else:
                    return False
            else:
                # expect alpha or numeric but is "**"
                if c == "(":
                    pass
                elif c == "*" and ex[i-1] == "*" and ex[i-2] != "*":
                    pass
                elif c.isalpha() or c.isnumeric():
                    safe = not safe
                else:
                    return False

            i += 1
        return safe

    def integrateExp(self, expression):
        if not self.parse(expression):
            return -1
        symbolStr = self.getSymbolsFromString(expression)
        if len(symbolStr) == 0:
            return -1

        code = ast.parse(expression, mode='eval')
        code = compile(code, '', mode='eval')
        symbolStr = self.getSymbolsFromString(expression)

        symbols = []
        for s in symbolStr:
            symbols.append(sy.Symbol(s))

        f = lambda x, y=0, z=0: eval(code)

        inters = []
        for s in symbols:
            inters.append(("d{}".format(s), str(sy.integrate(f(*symbols), s))))

        return inters

