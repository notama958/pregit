
import zlib
import hashlib
import os
import time
from others import pregitExist
from others import hash

# based on Git objects: Blob, Tree, Commit

class Object(object):
    type=None
    def __init__(self,data=None):
        self.data=data
        self.path=pregitExist()

    def write(self):
        """"""
        pass

# example .pregit/objects/8b/09xjdn0...
class Blob(Object):
    path=None
    def __init__(self,data):
        super(Blob,self).__init__(data)
        self.type=b'blob '
    def write(self):
        """ hash files and save into objects/"""
        files=self.check_files # list of file names
        for file in files:
            f=open(os.getcwd()+"/"+file,"rb")
            sha, bytes=hash(self.type,f.read())
            # write to objects/
            objectDire=self.path+"/objects"
            try:
                if os.path.exists(objectDire):

                    """ check sub hash folder exist"""
                    try:
                        os.mkdir(objectDire+"/"+sha[:2])
                    except FileExistsError as e:
                        pass
                    if os.path.exists(objectDire+"/"+sha[:2]+"/"+sha[2:]) == False:
                            # write to staging area
                            f_mode="w"
                            if os.path.exists(self.path+"/index"):
                                f_mode="a"
                            i_line="100644 blob {} {}\n".format(sha,file)
                            f_index=open(self.path+"/index",f_mode)
                            f_index.write(i_line)
                            # write to objects
                            f=open(objectDire+"/"+sha[:2]+"/"+sha[2:],"wb")
                            f.write(zlib.compress(bytes))
                            f.close()

                else:
                    raise FileNotFoundError("Error: Pregit folder is missing")
            except FileNotFoundError as e:
                print(e)
                print("Advice: please try to reinstall pregit")


    @property
    def check_files(self):
        """check files input and output data bytes"""
        if self.path is not None:
            files=[]
            if self.data[0] == '.':
                files=[f for f in os.listdir('.') if os.path.isfile(f)]
            else:
                for i in self.data:
                    filepath=os.getcwd()+"/"+i
                    if os.path.exists(filepath) and os.path.isfile(filepath):
                        files.append(i)
            return files


# create a tree for the blobs

class Tree(Object):
    def __init__(self,data):
        super(Tree,self).__init__(data)
        self.type=b'tree '
        self.sha=None
        self.write()

    def write(self):
        """copy from index file to tree file and hash it"""
        if self.path is not None:
            try:
                f=open(self.path+"/index","rb+")
                index=f.read()
                if len(index) <2:
                    # empty index
                    raise ValueError("Error: You should stage the files first")
                sha, bytes=hash(self.type,index)
                self.sha=sha # save this for commit
                objectDire=self.path+"/objects"
                if os.path.exists(objectDire):

                    """ check sub hash folder exist"""
                    try:
                        os.mkdir(objectDire+"/"+sha[:2])
                    except FileExistsError as e:
                        pass
                    if os.path.exists(objectDire+"/"+sha[:2]+"/"+sha[2:]) == False:
                            # write to objects
                            f=open(objectDire+"/"+sha[:2]+"/"+sha[2:],"wb")
                            f.write(zlib.compress(bytes))
                            f.close()
                else:
                    raise FileNotFoundError("Error: Pregit folder is missing")
            except ValueError as e:
                print(e)
            except FileNotFoundError as e:
                print(e)
                print("Advice: please try to reinstall pregit")


    @property
    def hash_tree(self):
        """Return sha1 for commit"""
        return self.sha

# commit by the tree
class Commit(Object):
    def __init__(self,data):
        super(Commit,self).__init__(data)
        self.msg=data
        self.type=b'commit '
        self.tree=Tree(data=None) # create tree first
    def parentCommit(self):
        """check parent commit """
        # read parent commit
        try:
            f= open(self.path+"/HEAD","r+")
            curr_branch=f.read()
            # extract the path only
            curr_branch=curr_branch[curr_branch.find(":")+1:].strip()
            f.close()
            if os.path.exists(self.path+"/"+curr_branch):
                  f=open(self.path+"/"+curr_branch,"r+")
                  parent_sha=f.read().strip()
                  f.close()
                  return parent_sha
            else:

                return None
        except FileExistsError as e:
            print("Please reinstall pregit")
            return None

    def getCurrentBranch(self):
        """get current branch"""
        f= open(self.path+"/HEAD","r+")
        curr_branch=f.read()
        # extract the path only
        curr_branch=curr_branch[curr_branch.find(":")+1:].strip()
        return curr_branch

    def writeParentCommit(self, sha1):
        """Pre assumption : refs/heads/<branch> exists"""
        try:
            curr_branch=self.getCurrentBranch()
            f=open(self.path+"/"+curr_branch,"w")
            f.write(sha1)
            f.close()
        except FileExistsError as e:
            print("Please reinstall pregit")
            return None

    def writeToLog(self,sha,data):
        """ write to log"""
        obj=dict()
        data=data.split("\n")
        for i in data:
            cursor=i.find(" ")
            if cursor >0:
                obj[i[:cursor]]=i[cursor+1:].strip()
        msg=data[len(data)-1].strip()
        log =""
        initial=True
        if obj.get('parent') == None:
            empty_arr=[0 for i in range(40)]
            log+="{} ".format(''.join(str(e) for e in empty_arr))
        else:
            initial=False
            log+="{} ".format(obj.get('parent'))

        log+="{} ".format(sha)

        if obj.get('author') is not None:
            log+="{} ".format(obj['author'])
        if initial:
            log+="commit(initial):{}\n".format(msg)
        else:
            log+="commit:{}\n".format(msg)
        # write to log file
        try:
            f=open(self.path+"/logs/"+self.getCurrentBranch(),"a+")
            f.write(log)
            f=open(self.path+"/logs/HEAD","a+")
            f.write(log)
            f.close()
        except FileNotFoundError as e:
            print(e)
            print("Please reinstall pregit")

    def write(self):
        """ hash files and save into objects/"""
        if self.path is not None:
            # read tree sha1
            if self.tree.hash_tree is not None:
                sha_tree=self.tree.hash_tree
                file_content="tree {}\n".format(sha_tree)
                # check parent commit
                parent_commit=self.parentCommit()
                if parent_commit is not None:
                    file_content+="parent {}\n".format(parent_commit)
                # read owner info
                if os.path.exists(self.path+"/config"):
                    """"""
                    f=open(self.path+"/config","r+")
                    lines=f.readlines()
                    userObject=dict()
                    for line in lines:
                        arr=line.split(" ")
                        userObject[arr[0]]=arr[1].rstrip("\n")
                    # record the commit time
                    seconds=time.time()
                    file_content+="author <{}> <{}> {}\n".format(userObject['username'],userObject['email'],seconds)
                    file_content+="commiter <{}> <{}> {}\n".format(userObject['username'],userObject['email'],seconds)
                file_content+="\n{}".format(self.msg)
                sha,bytes=hash(self.type,file_content.encode())
                # overwritten parent commit
                self.writeParentCommit(sha)
                # write to logs/
                self.writeToLog(sha,file_content)
                # write to objects/
                objectDire=self.path+"/objects"
                # clear staging area
                f=open(self.path+"/index","w").close()
                try:
                    if os.path.exists(objectDire):

                        """ check sub hash folder exist"""
                        try:
                            os.mkdir(objectDire+"/"+sha[:2])
                        except FileExistsError as e:
                            pass
                        if os.path.exists(objectDire+"/"+sha[:2]+"/"+sha[2:]) == False:
                                # write to objects
                                f=open(objectDire+"/"+sha[:2]+"/"+sha[2:],"wb")
                                f.write(zlib.compress(bytes))
                                f.close()
                                print("commit: {}".format(sha))

                    else:
                        raise FileNotFoundError("Fatal: Pregit folder is missing")
                except FileNotFoundError as e:
                    print(e)
                    print("Advice: please try to reinstall pregit")

