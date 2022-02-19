import os,sys

from objects import Blob

# add files to staging area
# create blob files in .pregit/objects/
class Add():
    def __init__(self,files):
        """"""
        blob=Blob(data=files)
        blob.write()


