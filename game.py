import copy
import random
import time
#using time.sleep method to differentiate the consecutive print method


suit=['H','S','D','C']
face=['J','Q','K','A']

#cards for shuffling and assigning randomly
shuffled_card=['HA', 'SK', 'DQ', 'CJ', 'H10', 'S9', 'D8', 'C7', 'H6', 'H5', 'H4', 'H3', 'H2', 'HK', 'SA', 'DJ', 'CQ', 'S10', 'D9', 'S8', 'S7', 'S6', 'S5', 'S4', 'S3', 'S2', 'HQ', 'SJ', 'DA', 'CK', 'C10', 'C9', 'C8', 'H7', 'C6', 'C5', 'C4', 'C3', 'C2', 'HJ', 'SQ', 'DK', 'CA', 'D10', 'H9', 'H8', 'D7', 'D6', 'D5', 'D4', 'D3', 'D2']

#distribution function
def cards_distribution(players):
    input_method=input("Want to enter distribution by input file (Y/N):")
    
    #file input method:
    if input_method=='Y':
        while(True):
            try:
                file_name=input("Enter file name in the format name.txt :")
                file=open(file_name,"r")
                card_string=file.readlines()
                file.close()
                break
            except:
                print("Enter the correct file name, ensure that it is saved in same directory")
        
    #random distribution:
    else: 
        random.shuffle(shuffled_card)

    #assigning cards
    for i in range(4):
        dist=[]
        if input_method=='Y':
            dist=card_string[i].split(",")
        else:
            dist=shuffled_card[i*13:(i+1)*13]
        
        #initialization:
        bot=players[i]
        for s in suit:
            bot[s]=[]
        
        #assigning cards
        for j in dist:
            try:
                bot[j[0]].append(int(j[1:]))
            except:
                bot[j[0]].append(11+face.index(j[1:]))
        for s in suit:
            bot[s].sort(reverse=True)
    return

#function calling bets for bots
def calls(bot):
    cnt=0
    for i in bot:
        for j in bot[i]:
            if j>10:
                cnt+=1
            else:
                break
    return cnt

#retriving next card for the given round of bots
def get_card(bot,os,ocd):
    ans=["",0]
    #for same suit
    if len(bot[os])>0:
        if bot[os][0]>ocd:
            ans[0]=os
            ans[1]=bot[os].pop(0)
        else:
            ans[0]=os
            ans[1]=bot[os].pop(len(bot[os])-1)
    else:
        #for different suit
        for s in suit:
            if len(bot[s])>0 and s!=os:
                if ans[0]=="" or ans[1]>bot[s][len(bot[s])-1]:
                    ans[0]=s
                    ans[1]=bot[s][len(bot[s])-1]
        bot[ans[0]].remove(ans[1])
    return ans

#Creating first card for bot
def first_card(bot):
    ans=["",0]
    for s in suit:
        if len(bot[s])>0 and (ans[0]=="" or bot[s][0]>ans[1]):
            ans[0]=s
            ans[1]=bot[s][0]
    bot[ans[0]].remove(ans[1])
    return ans

#changing cards intrinsic value into printing value
def facecard_change(s):
    l=[]
    l.append(s[0])
    try:
        l.append(int(s[1:]))
    except:
        l.append(11+face.index(s[1]))
    return l

#converting card struct to printing strings
def card_tostr(li):
    s=li[0]
    if li[1]>10:
        s+=face[li[1]-11]
    else:
        s+=str(li[1])
    return s

#showing available cards of the player for each round:
def disp_available_cards(player):
    print("\nAvailable Cards: ",end="")
    for i in player:
        for j in player[i]:
            if j>10:
                print(i+str(face[j-11])+", ",end="")
            else:
                print(i+str(j)+", ",end="")
    print('\n')


palyer_names=['bot1','bot2','bot3','player']
scores=[0]*4

### GAME ITERATION###
while(True):

    #Initailization for distribution
    bot1={}
    bot2={}
    bot3={}
    player={}

    #input/distribution of cards
    list_of_players=[bot1,bot2,bot3,player]
    cards_distribution(list_of_players)
    
    #calls
    disp_available_cards(player)
    print("\ncalls of players ",end="")
    player_calls=[calls(bot1),calls(bot2),calls(bot3)]
    
    #printing calls
    for i in range(4):
        if i==3:
            while(True):
                try:
                    player_calls.append(int(input("player-> ")))
                    break
                except:
                    print("Enter valid call!")
        else:
            print(palyer_names[i]+"->"+str(player_calls[i])+", ",end="")


    #printing order
    print("\ncyclic order bot1->bot2->player->bot3->bot1………\n\nstart form bot2\n")

    #count for each player's round win
    wincnt=[0]*4

    #playing order
    play=[bot1,bot2,player,bot3]
    name=["bot1","bot2","player","bot3"]
    
    cnt=1       #for number of rounds
    prevind=1   #index storing first turn for next round (starting from bot2)

    #game_rounds
    while(cnt<=13):

        #printing round number
        print("Round ", cnt)
        fcard=["",0]
        pcard=["",0]
        card={}

        #iteration for each turn in a round
        for i in range(4):
            cur=play[prevind%4]

            #first card
            if i==0:
                #for player
                if name[prevind%4]=="player":
                    disp_available_cards(player)
                    while(True):
                        try:
                            time.sleep(0.5)
                            s=input("Player-> ")
                            fcard=facecard_change(s)
                            player[fcard[0]].remove(fcard[1])
                            break
                        except:
                            print("Invalid card or not available, re-enter the card:")
                #for bot
                else:
                    fcard=first_card(cur)
                    time.sleep(0.5)
                    print(name[prevind%4]+"-> "+card_tostr(fcard))
                
                #card entry
                card[prevind%4]=fcard
            
            #rest cards
            else:
                #for player
                if name[prevind%4]=="player":
                    disp_available_cards(player)
                    while(True):
                        try:
                            time.sleep(0.5)
                            s=input("Player-> ")
                            pcard=facecard_change(s)
                            player[pcard[0]].remove(pcard[1])
                            break
                        except:
                            print("Invalid card or not available, re-enter the card:")
                #for bots
                else:
                    pcard=get_card(cur,fcard[0],fcard[1])
                    time.sleep(0.5)
                    print(name[prevind%4]+"-> "+card_tostr(pcard))
                
                #card entry
                card[prevind%4]=pcard

                #changing highest card
                if pcard[0]==fcard[0] and pcard[1]>fcard[1]:
                    fcard=copy.deepcopy(pcard)
            
            prevind+=1
        

        roundcard=[]    #round's highest card
        winind=-1       #round's winner index
        
        #checking winner
        for i in range(0,4):
            if card[i][0]==fcard[0] and (winind==-1 or card[i][1]>roundcard[1]):
                roundcard=card[i]
                winind=i
        time.sleep(0.5)
        print("\n"+name[winind]+" wins.\n") #printing winner of round
        
        #storing win counts of rounds for the players:
        if name[winind]!="player":
            wincnt[int(name[winind][-1])-1]+=1
        else:
            wincnt[3]+=1
        prevind=winind
        cnt+=1
        time.sleep(1)

    gamewin=-130    #game winning score as in 1 game 13 round and minimum score -10*x
    gamewinind=-1   #game winning player's index

    #score calculation
    print("\nscores:")
    for i in range(4):
        sc=0
        if player_calls[i]>wincnt[i]:
            sc=-10*player_calls[i]
        else:
            sc=10*player_calls[i]+(wincnt[i]-player_calls[i])
        if sc>gamewin:
            gamewin=sc
            gamewinind=i
        scores[i]+=sc
        print(palyer_names[i]+"="+str(sc))
    time.sleep(0.5)
    print(palyer_names[gamewinind]+" is the winner!!!!!!!!")
    
    #continuing game:
    ind=input("\nContinue(Y/N):")
    
    #on not continuing total score calculation along with series winner
    if ind=='N':
        print("\nTotal Scores:")
        for i in range(4):
            print(palyer_names[i]+"="+str(scores[i]))
        serieswinind=scores.index(max(scores))
        time.sleep(0.5)
        
        #printing series winner
        print("\n"+palyer_names[serieswinind]+" wins the series.")
        print("Exiting.....")
        break