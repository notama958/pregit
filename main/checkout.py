import sys, os
from others import pregitExist
from others import read_zlib
from others import listofCommits
from others import wipeOff
from others import listofBranch
import glob

# create commits from staged files
# add commit objects to  .pregit/objects/


class Checkout():
    path=None
    isBranch=False
    def __init__(self,args) :
        self.path= pregitExist()

        if self.path is not None:
            # if checkout from branch
            if args.get('branch') is not None:
                self.checkoutBranch(args.get('branch'))
            else:
                self.checkoutCommit(args.get('sha1'))
        else:
            print("Fatal: Please reinstall pregit")

    def checkoutBranch(self,branch):
        """"""
        # change reference at HEAD

        if branch in listofBranch():
            self.isBranch=True
            # update the HEAD to this branch's latest commit
            f=open(self.path+"/HEAD","w+")
            path=f.read().split(" ")
            path="ref: refs/heads/{}".format(branch)
            print(path)
            f.write(path)
            # call checkout from latest commit of the branch
            f=open(self.path+"/"+path.split(" ")[1],"r+")
            latest_cmt=f.read()
            self.checkoutCommit(latest_cmt)
            f.close()
        else:
            # non existing branch
            print("Fatal: Branch doesn't exist")

    def checkoutCommit(self,commit):
        """Checkout from commit"""
        self.readFromCommit(commit)

    def readFromCommit(self,sha1):
        """"""
        objectExist=self.findCommit(sha1)
        if objectExist is None:
            print("Fatal: Commit invalid")
        else:
            """"""
            type, content,size=read_zlib(objectExist)
            if type=="commit":
                # wipe all files
                wipeOff(os.getcwd())
                # get array of previous commit
                arr=listofCommits(sha1)
                # loop over each
                for i in arr:
                    # parse each commit
                    self.parseCommit(i.get('commit'))
                print("checkout from commit: {}".format(sha1))
                # update HEAD
                f=open(self.path+"/HEAD","r+")
                path=f.read().split(" ")
                ref=path[1]
                # extract the current branch
                branches=listofBranch()
                curr_branch=""
                for branch in branches:
                    if branch in ref:
                        curr_branch=branch
                        break
                # update HEAD build new path
                if self.isBranch == False:
                    path=path[0]+" "+"refs/heads/"+curr_branch+"/"+sha1
                    f=open(self.path+"/HEAD","w+")
                    f.write(path)
                    f.close()
            else:
                print("Fatal: cannot checkout from this sha1")
    def readTree(self,tree_sha1):
        """read blob and update the snapshot from the tree """
        tree_type, tree_content, tree_size=read_zlib(self.path+"/objects/"+tree_sha1[:2]+"/"+tree_sha1[2:])
        hasTree=None
        lines=tree_content.split("\n")
        # loop over content of a tree
        for line in lines:
            if line != '':
                type= line.split(" ")[1]
                sha1= line.split(" ")[2]
                filepath= line.split(" ")[3]
                # check if any subtree
                if type == 'tree':
                    hasTree=sha1 # notify there is subtree next increment will parse this subtree
                # for normal blob
                else:
                    # read from blob
                    btype,bcontent,bsize=read_zlib(self.path+"/objects/"+sha1[:2]+"/"+sha1[2:])
                    f=open(os.getcwd()+"/"+filepath,"w+")
                    f.write(bcontent.replace("\x00","")) # update this snapshot to the file

        return hasTree

    def parseTree(self,tree_sha1):
        """extract the tree and get blobs + return subtrees sha1 if have"""
        # ret to contain subtree hashed
        ret=None
        ret=self.readTree(tree_sha1)
        return ret

    def parseCommit(self,sha):
        """extract tree sha1 from commit """
        # parse the commit
        path=self.path+"/objects/"+sha[:2]+"/"+sha[2:]
        type, content,size= read_zlib(path)
        arr=content.split("\n")
        # tree sha1 is the first line
        tree_commit=arr[0].strip()
        # get the sha1
        tree_sha1=tree_commit.split(" ")[1]
        # recursively read  till there no subtree in the a tree
        while tree_sha1 is not  None:
            tree_sha1=self.parseTree(tree_sha1) # return None or sub tree sha


    def findCommit(self,sha1):
        """Find the exact path of commit"""
        objectsPath=self.path+"/objects/"
        listObjects=glob.glob(objectsPath+"*/*", recursive = True)
        for object in listObjects:
            adjustedObj=object.replace(objectsPath,"")
            arr=adjustedObj.split("/")
            if sha1[:2]== arr[0]:
                if sha1[2:] in arr[1]:
                    return object # return path to object file
        return None
