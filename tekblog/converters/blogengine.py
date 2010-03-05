#!/usr/bin/env python
import os, glob, sys
from os import path
from xml.dom.minidom import parse, parseString
from tekblog.models import Entry, User
from datetime import datetime

def getNodeValue(node):
    val = node.childNodes[0].nodeValue
    if val:
        return val

def getValidNode(node):
    if hasattr(node, 'tagName'):
        return node
    return None

if sys.argv[1]:
    for f in glob.glob(path.join(sys.argv[1], "*.xml")): 
        ds = open(f)
        dom = parse(ds) 

        e = Entry()
        e.markup = 'none'

        for node in dom.childNodes[0].childNodes:
            if getValidNode(node):
                ignore = ['owner', 'description', 'notifications', 'tags', 'categories']
                if not node.tagName in ignore:
                    val = getNodeValue(node)
                    if node.tagName == 'author':
                        owner = User.objects.filter(username=val)[0]
                        if owner:
                            e.owner = owner
                        else:
                            e.owner = User.objects.filter(pk=1)[0]
                    elif hasattr(e, node.tagName):
                        setattr(e, node.tagName,val)

                elif node.tagName == 'tags':
                    for node2 in node.childNodes:
                        if getValidNode(node2):
                            if node2.tagName == 'tag':
                                getNodeValue(node2)
                print e.owner
                
        e.save()

