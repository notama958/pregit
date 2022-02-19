import os, sys
from queue import Queue
from typing import Set
import zlib
import hashlib
import shutil

# reusable functions

# list of branches at refs/heads/
def listofBranch():
    arr=os.listdir(os.getcwd()+"/.pregit/logs/refs/heads")
    # print(arr)
    return arr

# clean the files for git checkout
def wipeOff(path):
    """wipe off all files"""
    arr = os.listdir(path)
    for i in arr:
        if i != 'main' and i !='.pregit':
            if os.path.isfile(os.getcwd()+"/"+i):
                os.remove(i)
            elif os.path.isdir(os.getcwd()+"/"+i):
                shutil.rmtree(i)

# list of the commits from the checkout commit
def listofCommits(cmt=None):
    """get the array of commits"""
    path=pregitExist()
    if path is not None:
        f= open(path+"/HEAD","r+")
        curr_branch=f.read()
        # extract the path only
        curr_branch=curr_branch[curr_branch.find(":")+1:].strip()
        # build log path
        path_log=path+"/logs/"+curr_branch
        f=None
        # read log file
        if os.path.isfile(path_log):
            # current reference is the branch name
            f=open(path_log,"r+")
        else:
            try:
                # current reference is the commit name
                # get current branch
                branches=listofBranch()
                new_path=""
                for branch in branches:
                    if branch in path_log:
                        new_path=branch
                        break
                path_log=path+"/logs/refs/heads/"+new_path
                if os.path.isfile(path_log):
                    f=open(path_log,"r+")
                else:
                    raise Exception("You don't have any commit yet")
            except Exception as e:
                print(e)
                exit(-1)
        lines=f.readlines()
        f.close()
        stack=[]
        for line in lines:
            commit_msg=line[line.find("commit"):]
            prev_commit=line.split(" ")[0]
            curr_commit=line.split(" ")[1]
            author_date=line[line.find(curr_commit)+len(curr_commit):line.find("commit")].strip()
            author=author_date.split(" ")[0]
            author_email=author_date.split(" ")[1]
            date=author_date.split(" ")[2]
            stack.append({'commit':curr_commit,'author':author,'email':author_email,'date':date,'commit_msg':commit_msg})

        if cmt is not None:
            index=None
            for i in range(0,len(stack)):
                if stack[i].get('commit')==cmt:
                    index=i
            if index is not None:
                stack=stack[:index+1]
        return stack
    else:
        print("Please reinstall pregit")
        return None

# check if .pregit/ exist
def pregitExist():
    """check if current .pregit/ exists"""
    path=os.getcwd()
    path=path+"/.pregit"
    try:
        if os.path.exists(path) == False:
            raise FileNotFoundError("Not in the pregit directory")
        return path
    except FileNotFoundError as e:
        print(e)
        return None

# hash with sha1 following the structure of Git Object
def hash(btype, bdata):
    """SHA1 hash with byte type and byte data"""
    length=len(bdata)
    bytes=btype +str(length).encode() +b'\0'+bdata
    sha= hashlib.sha1(bytes).hexdigest()
    return sha, bytes

# decompress the sha1
def read_zlib(file):
    """decompress hashed data"""
    f=open(file,"rb")
    raw=zlib.decompress(f.read())
    # get type
    # print(raw)
    x=raw.find(b' ')
    type=raw[0:x].decode("ascii")
    y=raw.find(b'\x00',x)
    size=int(raw[x:y].decode("ascii"))
    content=str(raw[y:].decode("ascii"))
    return type, content, size
    # print("Type:{}\nSize: {}\nContent: {}".format(type,size,content))



if __name__=="__main__":
    """"""
    listofBranch()
    # print(os.getcwd())
    # wipeOff(os.getcwd())
    # listofCommits()
    # type,content,size=read_zlib("/root/Desktop/pregit/.pregit/objects/0b/b1749e597a60791daf871e233634e525d2d351")
    # type,content,size=read_zlib("/root/Desktop/pregit/.pregit/objects/2b/a0eb360c4326eaacb6d9aa35a0ddb9dfbaad94")
    # print(content)
    # read_zlib("/root/Desktop/pregit/.pregit/objects/c7/7f1f078b6bdbdd3df2a1c0c494a43983112a0d")
    # read_zlib("/root/Desktop/pregit/.pregit/objects/a8/2bd1659e5a6b420c4edfbdca82fed358397416")