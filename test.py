import argparse
import os.path
from PIL import Image
import time

s= time.time()
im = Image.open("static/share_images/e.jpg")
w_h = float(im.height) / im.width
im = im.resize((200, int(200 * w_h)),resample=Image.LANCZOS)
im.save("static/share_images/e2.jpg")
print(time.time() - s)
# a = 1
# b = 2
# c = 5
# d = 1
# tree = (('a', '+', 'b'), '*', ('c', '+', 'd'))
# print(tree)
#
#
# def parse(tree):
#     if isinstance(tree, (str, int, float)):
#         return tree
#     if isinstance(tree[0], (int, float)) and isinstance(tree[2], (int, float)):
#         return eval(' '.join(tree))
#     if not (isinstance(tree[0], tuple) or isinstance(tree[2], tuple)):
#         return tree
#     if isinstance(tree[0], tuple):
#         tree[0] = parse(tree[0])
#     if isinstance(tree[0], tuple):
#         tree[2] = parse(tree[2])
#
#
# def simpify(tree1, tree2, operation):
#     if isinstance(tree1, tuple) and isinstance(tree2, tuple):
#         if tree1[1] in ['-', '+'] and tree2[1] in ['-', '+']:
#             if operation == '*':
#                 exp = [tree1[0] + tree2[0], tree2[1] + tree1[0] + tree2[2],
#                        tree1[1] + tree1[2] + tree2[1],
#                        _p_(tree1[1], tree2[1]) + tree1[2] + tree2[2]]
#
#
# class Exp(object):
#     def __init__(self):
#         self.exp = ()
#
#
# class NoExp(object):
#     def __init__(self, exp):
#         self.exp = exp
#
# def _process(exp):
#
# def _p_(op1, op2):
#     if op1 != op2:
#         return '-'
#     else:
#         return '+'
