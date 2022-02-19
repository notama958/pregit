#!/usr/bin/env python3

import init
import add
import commit
import checkout
import log
import parser
import sys, os

# pregit main file

def Pregit(cmds):
    # parse the cli arguments
    pa=parser.Parser()
    cmd, args= pa.command(sys.argv[1:])
    # print(cmd)
    # print(args)
    if cmd == 'init':
        """create .pregit/ """
        i= init.Init(path=args)
    elif cmd == 'add':
        """staging files"""
        a=add.Add(files=args)
    elif cmd == 'commit':
        """commit files"""
        c=commit.Commit(msg=args)
    elif cmd == 'log':
        """show log"""
        l=log.Log(args=args)
    elif cmd == 'checkout':
        """checkout from commit and branch"""
        check=checkout.Checkout(args=args)
    else:
        print("Sorry still working on")


if __name__=="__main__":
    arguments= sys.argv[1:]
    Pregit(arguments)