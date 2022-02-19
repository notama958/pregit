#!/usr/bin/env python3

import os, sys
import re
import argparse

# Parser do the command line parsing arguments
# route to corresponding pregit function
class Parser():
    def __init__(self):
        self.parser=argparse.ArgumentParser(description="Pregit")
        self.subparser=self.parser.add_subparsers(dest="command")
        self.p_init()
        self.p_add()
        self.p_commit()
        self.p_checkout()
        self.p_log()

    def p_init(self):
        """pregit init command"""
        init=self.subparser.add_parser("init",help="init directory")
        init.add_argument("--path","-p",help="path to create directory")

    def p_add(self):
        """pregit init command"""
        init=self.subparser.add_parser("add",help="Stage files")
        init.add_argument("--file","-f",nargs="+",help="list of files or . for all files in current directory")

    def p_commit(self):
        """pregit commit command"""
        commit=self.subparser.add_parser("commit",help="Commit files")
        commit.add_argument("--message","-m",help="commit message")

    def p_checkout(self):
        """pregit commit command"""
        commit=self.subparser.add_parser("checkout",help="Checkout to branch or other commit")
        commit.add_argument("--branch","-b",help="branch name")
        commit.add_argument("--sha1",help="commit sha1")

    def p_log(self):
        """pregit log command"""
        commit=self.subparser.add_parser("log",help="Log commits")
        commit.add_argument("--oneline",help="logging tree commit one line",action="store_true")


    def command(self,argv):
        try:
            args= self.parser.parse_args(argv)
            if args.command== 'init':
                return 'init',args.path
            elif args.command=='add':
                return 'add',args.file
            elif args.command=='commit':
                return 'commit',args.message
            elif args.command=='checkout':
                if args.branch is None:
                    return 'checkout' , dict({'sha1':args.sha1})
                return 'checkout',dict({'branch':args.branch})
            elif args.command=='log':
                return 'log', dict({"oneline":args.oneline})
        except Exception as e:
            print(e)
if __name__=='__main__':
    # main()
    parser=Parser()
    print(sys.argv[1:])
    cmd, args= parser.command(sys.argv[1:])
    print(cmd)
    print(args)