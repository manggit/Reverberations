#! /user/bin/env python
#user provides handle and corresponding tweet
#persistantly check for retweets of the provided input
#follow each retweeter and rank them accordingly

import tweepy
import getpass


class Node:
    def __init__(self, sn, rank, lvl, ts, twid, parent_twid):
        self.sn = sn
        self.rank = rank
        self.lvl = lvl
        self.ts = ts
        self.twid = twid
        self.rtusr = parent_twid #parent twid, this is a retweet of rtuser
        
class parentNode:
    def __init__(self, parent, parent_twid, twid):
        self.parent = parent
        self.parent_twid = parent_twid
        self.twid = twid

def authenticate(usr='0', pswd='0'):
    if usr == '0':
        usr = raw_input("twitter username: ")
        pswd = getpass.getpass("password: ")
    auth = tweepy.BasicAuthHandler(usr, pswd)
    api = tweepy.API(auth)
    return api

def calulate_Rank(tweetID, auth):
    idx_lvl = 0
    idx_usr = 0
    lvl = []
    nxtlvl = []
    tree = []
    x = 1
    
    twt = auth.get_status(tweetID)             #get current tweet
    pnode = parentNode(twt.user, 'top', tweetID)
    lvl.append(pnode)                          #append rt id's to nxtlvl list


    #outer loop that keeps track of tree level
    while (x > 0):
        print 'length of lvl', len(lvl)
        #inner loop steps through users in given level
        while idx_usr < len(lvl):
            print 'in second loop'
            try:
                rt = auth.retweets(lvl[idx_usr].twid, 100)      #get retweets
                print 'hello'
                twt = auth.get_status(lvl[idx_usr].twid)        #get current tweet
                print'got tweet'
                for s in rt:                                     #step through retweets
                    pnode = parentNode(twt.user, twt.id, s.id)   #s.id is the tweet id of the retweet
                    nxtlvl.append(pnode)                         #append rt id's to nxtlvl list
                    print twt.user.screen_name, s.id
                print 'length of next level is', len(nxtlvl)

                node = Node(twt.user, len(nxtlvl),             #create new node for tree
                            idx_lvl, twt.created_at,
                            lvl[idx_usr].twid,
                            lvl[idx_usr].parent_twid)
                print twt.user.screen_name
                tree.append(node)               #append new node to tree list

                idx_usr = idx_usr+1             #increment user list index
            except tweepy.error.TweepError:
                print 'caught error'
                idx_usr = idx_usr+1             #increment user list index
                continue

#make sure to remove in the future before handing in
        if (not(x % 3)):
            auth = authenticate('SwiftTest', 'Pr3t3nt!0usWr1ting!')
            
        del lvl[:]
        lvl = list(nxtlvl)                        #assign nxtlvl to lvl
        x = len(lvl)
        print 'x is ', x
        del nxtlvl[:]                       #clear nxtlvl
        idx_lvl = idx_lvl+1                 #increment level counter
        idx_usr = 0                         #rest list index to 0
        print 'testing', len(lvl)
                
        
    return tree
    
    
def main():
    api = authenticate()
    tree = calulate_Rank(20065671636, api)

    for s in tree:
        print s.twid, s.lvl, s.rank, s.sn.screen_name

        

if __name__ == "__main__":
    main()
