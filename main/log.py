import sys, os
import time
from others import pregitExist
from others import listofCommits

# View commit log
class Log():
    path=None
    def __init__(self,args) :
        self.path=pregitExist()
        if self.path is not None:
            """"""
            # check current commit
            f=open(self.path+"/HEAD","r+")
            path=f.read().split(" ")
            ref=path[1].split("/")
            commit= ref[len(ref)-1]
            # get list of commits
            self.stack=listofCommits(commit)
            # format view like in git
            if args.get('oneline'):
                self.oneline()
            else:
                self.default()

        else:
            print("Please reinstall pregit")

    def default(self):
        """Log all commits made"""
        for i in reversed(self.stack):
            print("Commit: {}".format(i.get('commit')))
            print("Author: {} - {}".format(i.get('author'),i.get('email')))
            print("Date: {}".format(time.ctime(float(i.get('date')))))
            print("\n\t{}".format(i.get('commit_msg')))
            print("========================================")
    def oneline(self):
        """The same structure with git log --oneline"""
        for i in reversed(self.stack):
            print("{} - {}".format(i.get('commit')[:6],i.get('commit_msg').split(":")[1]))