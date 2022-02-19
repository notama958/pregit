#!/usr/bin/env python3

import os, sys
import re
import shutil

# create .pregit/

class Init():
    def __init__(self,*args,**kwargs):
        """create Pregit directory"""
        self.path= kwargs.get("path")
        root_dire=os.getcwd().split("/")[1]
        if self.path[0]== "~":
            self.path="/"+root_dire+self.path[1:]
        if self.path is not None:
            path_exist= os.path.exists(self.path)
            dire_exist= os.path.isdir(self.path)
            try:
                if path_exist == False:
                    raise FileNotFoundError("Path not found")
                if dire_exist == False:
                    raise FileNotFoundError("Directory not found")
                self.createDire(self.direExist)
            except FileNotFoundError as e:
                print(str(e))
                pass
    @property
    def direExist(self):
        """Check if pregit is existed"""
        self.pregit= self.path+"/"+".pregit"
        if os.path.exists(self.pregit) and  os.path.isdir(self.pregit):
            return True
        return False

    def createDire(self,status):
        """Create or Recreate based on pregit existence status"""
        if status:
            """reinitialize"""
            shutil.rmtree(self.pregit)
            self.createFolder()
            print("Reinitialize pregit directory")
        else:
            """Initilize"""
            self.createFolder()
            print("Successfully initialize pregit directory")

    def createFolder(self):
        """Create directory and files"""
        os.mkdir(self.pregit)
        os.mkdir(self.pregit+"/objects")
        os.mkdir(self.pregit+"/logs")
        os.mkdir(self.pregit+"/logs/refs/")
        os.mkdir(self.pregit+"/logs/refs/heads")
        os.mkdir(self.pregit+"/refs")
        os.mkdir(self.pregit+"/refs/heads")

        # create files
        f=open(self.pregit+"/HEAD","w")
        f.write("ref: refs/heads/master") # original pointer at master branch
        f=open(self.pregit+"/logs/HEAD","x")
        f=open(self.pregit+"/config","x")
        f.write("username yourname\n")
        f.write("email yourname@email.com\n")
        f.close()

if __name__=="__main__":
    init = Init(path="~/Desktop/pregit/")







