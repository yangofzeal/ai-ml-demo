#!/usr/bin/env python
# coding:utf-8
"""Solve for the symbolic solution of a pde

author: Michael S. Yang

"""
from sympy.solvers import pdsolve
from sympy.abc import x, y, a, b, c
from sympy import Function, pprint

f = Function('f')
G = Function('G')
u = f(x,y)
ux = u.diff(x)
uy = u.diff(y)
genform = a*ux + b*uy + c*u - G(x,y)
pprint(genform)
print()
pprint(pdsolve(genform, hint='1st_linear_constant_coeff_Integral'))


##
##
## msyang(~/tmp/decision_machine/solve_pde)
## jobs:1 $ ./symbolic.py
##   ∂               ∂
## a⋅──(f(x, y)) + b⋅──(f(x, y)) + c⋅f(x, y) - G(x, y)
##   ∂x              ∂y
################################################################
##
##  d               d
##a*--(f(x, y)) + b*--(f(x, y)) + c*f(x, y) - G(x, y)
##  dx              dy
##>>> pprint(pdsolve(genform, hint='1st_linear_constant_coeff_Integral'))
##          //          a*x + b*y                                             \
##          ||              /                                                 |
##          ||             |                                                  |
##          ||             |                                       c*xi       |
##          ||             |                                     -------      |
##          ||             |                                      2    2      |
##          ||             |      /a*xi + b*eta  -a*eta + b*xi\  a  + b       |
##          ||             |     G|------------, -------------|*e        d(xi)|
##          ||             |      |   2    2         2    2   |               |
##          ||             |      \  a  + b         a  + b    /               |
##          ||             |                                                  |
##          ||            /                                                   |
##          ||                                                                |
##f(x, y) = ||F(eta) + -------------------------------------------------------|*
##          ||                                  2    2                        |
##          \\                                 a  + b                         /
##
##        \|
##        ||
##        ||
##        ||
##        ||
##        ||
##        ||
##        ||
##        ||
##  -c*xi ||
## -------||
##  2    2||
## a  + b ||
##e       ||
##        ||
##        /|eta=-a*y + b*x, xi=a*x + b*y
