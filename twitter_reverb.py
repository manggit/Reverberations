#! /user/bin/env python
#user provides handle and corresponding tweet
#persistantly check for retweets of the provided input
#follow each retweeter and rank them accordingly

import tweepy
import getpass
import os.path


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


#depreciated function, will not work after Aug 16
def authenticate(usr='0', pswd='0'):
    if usr == '0':
        usr = raw_input("twitter username: ")
        pswd = getpass.getpass("password: ")
    auth = tweepy.BasicAuthHandler(usr, pswd)
    api = tweepy.API(auth)
    return api


#authenticate using OAuth
def Oauthenticate():
    auth = tweepy.OAuthHandler('XSlYVMJ9ebCXOfdOPolgDg', 'RQdQxOnPFRqKogfVqL0JdpGwadXZ6XawtXn7QpcQ')
    
    try:
        redirect_url = auth.get_authorization_url()
        print 'Please visit the following URL and allow access to Reverb.it:'
        print redirect_url
    except tweepy.TweepError:
        print 'Error! Failed to get request token.'

    verifier = raw_input('Please enter the pin code: ')
    
    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print 'Error! Failed to get access token.'


    #save tokens to file
    filename = 'token.txt'
    FILE = open(filename, "w")
    FILE.write(auth.access_token.key)
    FILE.write(auth.access_token.secret)
    FILE.close()
    
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
    print twt.text
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
                print 'caught error', idx_usr, len(lvl)
                idx_usr = idx_usr+1             #increment user list index
                continue
            
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
    if(os.path.isfile('token.txt')):
       print 'file exists'
       f = open('token.txt', 'r')
       key = f.readline()
       secret = f.readline()
       auth = tweepy.OAuthHandler('XSlYVMJ9ebCXOfdOPolgDg', 'RQdQxOnPFRqKogfVqL0JdpGwadXZ6XawtXn7QpcQ')
       auth.set_access_token(key, secret)
       api = tweepy.API(auth)
       
    else:
        api = Oauthenticate()

    try:
        tree = calulate_Rank(20065671636, api)
    except tweepy.TweepError:
        print 'token invalid'
        api = Oauthenticate()
        tree = calulate_Rank(20065671636, api)

    for s in tree:
        print s.twid, s.lvl, s.rank, s.sn.screen_name

        

if __name__ == "__main__":
    main()
