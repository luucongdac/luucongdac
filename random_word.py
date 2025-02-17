

import random
import os
import math

def forever():
    while(1):
        None

def randomWord():
    with open("words.txt", 'r') as file:
        keyWords = [line.strip() for line in file]
    random.shuffle(keyWords)
    with open("random_word.txt", 'w') as file:
        file.writelines(word + '\n' for word in keyWords)    
      

def create():
    words = []
    with open('random_word.txt', 'r') as file:
        words = [line.strip().replace('"',"") for line in file.readlines()]
    
    os.remove('random_word.txt')
    try:
        os.remove('output_words.txt')
    except:
        None
    #print(words)
    keyWords = input("input key words to gen Words for Meta:  ")
    keyWords = keyWords.replace(" ","").split(",")
    for word in keyWords:
        if word not in words:
            print(f"{word} not in dict")
            return
    keyPass = input("input password to gen Words for Meta:  ")
    ascii_keyPass = []
    words_without_keyWords = []
    for word in words:
        if word not in keyWords:
            words_without_keyWords.append(word)
    random.shuffle(words_without_keyWords)
    # print(len(words))
    # print(len(words_without_keyWords))


    sum_ascii = 0
    for i in keyPass:
        sum_ascii += ord(i)
    for i in keyPass:
        sum_ascii *= ord(i)          
        if(sum_ascii > len(words)/2):
            break
    # print(sum_ascii)
    
    for i in keyPass:
        t = sum_ascii * ord(i)
        while(t > len(words)/3):
            t = int(t*2/3) 
        ascii_keyPass.append(t)

    while(sum_ascii > len(words)/2):
        sum_ascii = int(sum_ascii*2/3) 
    # print(sum_ascii)

    ascii_key_sort_increase = sorted(ascii_keyPass)
    ascii_key_sort_decrease = sorted(ascii_keyPass,reverse=True)
    # print(ascii_key_sort_increase)
    # print(ascii_key_sort_decrease)

    count = 0
    for i in ascii_key_sort_decrease:
        words_without_keyWords.insert(sum_ascii - i, keyWords[count])
        count += 1
    for i in ascii_key_sort_increase:
        words_without_keyWords.insert(sum_ascii + i, keyWords[count])
        count += 1


    with open("output_words.txt", 'w') as file:
        file.writelines(word + '\n' for word in words_without_keyWords)

# randomWord() 
# create()

def checkFile():
    a = []
    b = []
    with open("MetaWords", 'r') as file:
        a = [line.strip() for line in file]
    with open("TrustWords", 'r') as file:
        b = [line.strip() for line in file]

    for i in range (0, len(a)):
        if(i < len(a) and i < len(b)):
            if( a[i] == b[i]):
                print(f"{i}, {a[i]}")
# checkFile()

def getWords():
    keyWords = []
    file_ = input("input file name to gen Words for Meta:  ")
    keyPass = input("input password to gen Words for Meta:  ")
    with open(file_, 'r') as file:
        keyWords = [line.strip() for line in file]
    # print(keyWords)  # In ra mảng các từ   

    sum_ascii = 0
    ascii_keyPass = []

    sum_ascii = 0
    for i in keyPass:
        sum_ascii += ord(i)
    for i in keyPass:
        sum_ascii *= ord(i)          
        if(sum_ascii > len(keyWords)/2):
            break
    # print(sum_ascii)
    
    for i in keyPass:
        t = sum_ascii * ord(i)
        while(t > len(keyWords)/3):
            t = int(t*2/3) 
        ascii_keyPass.append(t)

    while(sum_ascii > len(keyWords)/2):
        sum_ascii = int(sum_ascii*2/3) 

    # print(ascii_keyPass)
    ascii_key_sort_increase = sorted(ascii_keyPass)
    ascii_key_sort_decrease = sorted(ascii_keyPass,reverse=True)

    key = []
    for i in ascii_key_sort_decrease:
        key.append(keyWords[sum_ascii - i])

    for i in ascii_key_sort_increase:
        key.append(keyWords[sum_ascii + i])
    print(key)

# getWords()

keyCharacter = [
    ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"],
    ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
    ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    ["!", "#", "$", "%", "&", "(", ")", "*", "+", "[", "]", "^", "{", "}", "~", ":", ";", "<", "=", ">", "?", "@"],
]

def getPassWords():
    keyPass = input("input password to gen pasword:  ")
    sum_ascii = 0

    for i in keyPass:
        sum_ascii = (sum_ascii + 2)* ord(i) 

    key = ""
    count = 0
    for i in keyPass:
        genKey = (sum_ascii + count)* ord(i) 
        # print(genKey)
        while(genKey >= len(keyCharacter[count])):
            genKey = int(genKey/3)
        key += keyCharacter[count][genKey]
        count += 1
        if(count >= len(keyCharacter)):
            count = 0
        # print(f"{count}, {genKey} , {key}")
    print(key)


# getPassWords()