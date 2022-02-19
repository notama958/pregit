import os,sys

from objects import Tree
from objects import Commit as CommitObject
from others import read_zlib
class Commit():
    def __init__(self,msg):
        """"""
        commit=CommitObject(data=msg)
        commit.write()


