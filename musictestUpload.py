import pygame # Load the required library
import sys
from playsound import playsound
from os import listdir
import os
from os.path import isfile, join
from os import walk
from pygame import mixer
import random
import glob
import numpy as np
from random import choices
from mutagen.mp3 import MP3
import time
import musicPlay
from random import shuffle
import keyboard

f = [] # stores all the files in the specificed folder

mypath = "C:/Users/.../.../MusicFolder/" # path to songs

for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    break

songs = []
p = []
songProb = {}
songTypes = [".mp3"] # [".mp3",...]# allowed music links
for s in f:
    if(s[-4:] in songTypes): # checks if items in the list are playable songs (checks if last 4 charcters are .mp3)

        # s = s.replace("_", "")
        songs.append(s)
        songProb[s] = 1
        
        p.append(1)
print("Here is the list of songs: ")
justSong = []


# used to delete numbers before songs and the .mp3 at the end
# Reformat to needs, just return songName with no alteration to return the actual full name
def cleanSong(songName):
    # songName = songName[5:len(songName)-4] # deletes numbering from front of songs and .mp3 from end
    # songName = songName.replace("_", "") # deletes random _ that appear in the songs names
    return songName

for name in songs:
    justSong.append(cleanSong(name))
for n in justSong:
    print(n)
list_keys = [ k for k in songProb ]
list_values = [v for v in songProb.values()]

# This code changes the songs priority levels
def prioritize(list_keys, list_values):
    choice = input("Enter a songs to change likelihood of (STOP to end and play song random song): ")
    while(choice not in justSong):
        if(choice.upper()=="STOP"):
            break
        choice = input("Invalid input, enter a song in the list(or STOP to end and play random song): ")
        
    if(choice.upper() != "STOP"):
        number = eval(input("What is the value: ")) 
    while(choice.upper() != "STOP"):
        choiceFull = songs[justSong.index(choice)]
        songProb[choiceFull]= number
        list_keys = [ k for k in songProb ]
        list_values = [v for v in songProb.values()]
        output = "{:>{}} {:>{}}"
        num = 5
        print("")
        print(output.format("Prob", num, "Song",num))
        print("-"*num*5)
        for i in range(len(list_keys)):
            print(output.format(list_values[i], num, justSong[i], num))
        print()
        choice = input("Enter a songs to change likelihood of (STOP to end and play random song): ")
        while(choice not in justSong):
            if(choice.upper()=="STOP"):
                break
            choice = input("Invalid input, enter a song in the list(or STOP to end and play random song): ")
        if(choice.upper()=="STOP"):
            break
        number = eval(input("What is the value: ")) 
    return list_keys, list_values
    
list_keys, list_values = prioritize(list_keys,list_values)
# end of priority levels code

playlist = []
def createPlaylist(list_keys, list_values):
    playlist = []
    playLength = 5
    playLength = int(input("What size of playlist do you want: "))
    # playedSongs = []
    for i in range(playLength):
        songChoice = choices(list_keys, list_values)[0]
        if(i>0 and songChoice == playlist[i-1]):
            while(songChoice != playlist[i-1]):
                songChoice = choices(list_keys, list_values)[0]
        playlist.append(songChoice)
    return playlist

def displayPlaylist(playlist):
    print("")
    print("Length\t", "--", "Song Name")
    for i in range(len(playlist)):
        audio = MP3(mypath + playlist[i])
        print(str(i+1)+ ". ", round(int(audio.info.length)/60,2), " --", cleanSong(playlist[i]))
    print("")
def playPlaylist(playlist, start ):
    mixer.init()
    #while start < len(playlist):
    for i in range(len(playlist)):
        audio = MP3(mypath + playlist[i])
        songLength = round(int(audio.info.length)/60,2)
        print('s: skip, e: end, p:pause, u:unpause',end="\r") #, b:song before')
        print("")
        print("Now playing", cleanSong(playlist[i]), end="\r")
        print("")
        start_time = time.time()
        mixer.music.load(mypath + playlist[i])
        #  print(time.time()-start_time)
        mixer.music.play()
        
        
        while mixer.music.get_busy():
            diffTime = 0
            currTime = 0
            while True: 
                try:
                    currTime = (time.time()-start_time)-diffTime
                    print(round((currTime)/60,2), "/", round(songLength,2), end="\r")
                    pygame.time.Clock().tick(1)

                    if keyboard.is_pressed('s'):
                        if(i==len(playlist)-1):
                            sys.exit()
                        else:
                            playPlaylist(playlist[i+1:], start)
                    elif keyboard.is_pressed('e'):
                        sys.exit()
                    elif keyboard.is_pressed('p'):
                        mixer.music.pause()
                        count = 0
                        pauseTime = time.time()
                        num=2
                        while not keyboard.is_pressed('u'):
                            time.sleep(num)
                            count+=1
                            num+=1
                        endTime = time.time()
                        mixer.music.unpause()
                    
                    elif keyboard.is_pressed('r'):
                        mixer.music.rewind()
                    else: 
                        pass
                except:
                    sys.exit()
            
playlist = createPlaylist(list_keys, list_values)
displayPlaylist(playlist)

def check(playlist, list_keys, list_values):
    option = input("Play playlist (p), shuffle(s), choose a song(c), reprioritize(r) end(e): ")
    
    if(option=='e'):
        pass
    elif(option=='p' or option.lower() == "play"):
        playPlaylist(playlist, 0)
    elif(option=='s'):
        shuffle(playlist)
        displayPlaylist(playlist)
        check(playlist, list_keys, list_values)
    elif(option=='c'):
        select = int(input("Which song number do you want to start from? "))-1
        playPlaylist(playlist[select:], 0)
    elif(option=="r"):
        list_keys, list_values = prioritize(list_keys, list_values)
        playlist = createPlaylist(list_keys, list_values)
        displayPlaylist(playlist)
        check(playlist, list_keys, list_values)
    else:
        pass
check(playlist, list_keys, list_values)
    
