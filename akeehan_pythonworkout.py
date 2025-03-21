#!/usr/bin/env python3
'''
DATA 420
Stephen Davies, University of Mary Washington, spring 2024


Add your code in the section designated below, and then run the program to
print out your score thus far. There are a total of 14 points available.
'''


HAL = 9000

BB = "8"

R2 = ["D", "2"]

L = [3]

K = {"2SO"}

C = ["3PO"]

WALL = [["E"]]

Galactica = {'Karl':'Helo', 'Kara':'Starbuck', 'Lee':'Apollo'}

Galactica['Sharon'] = 'Boomer'
Galactica['Marge'] = 'Racetrack'
Galactica['Louanne'] = 'Kat'

Germanna_levels = ["Freshman", "Sophomore"]

UMW_levels = ["Freshman", "Sophomore", "Junior", "Senior"]

MaryWash_levels = UMW_levels

CNU_levels = ["Freshman", "Sophomore", "Junior", "Senior"]



def plus2(num):
	return 2 + num


def center(string):
    length = len(string)
    if string == "":
        return None
    elif length % 2 != 0:
        index = length // 2
        ans = string[index]
        return ans
    elif length % 2 == 0:
        index = length // 2
        ans = string[index - 1] + string[index]
    return ans        
    
def nuke_last(lst, item):
    temp = []
    if item not in lst:
        exit()
    else:
        i = len(lst) - 1

        while i >= 0:
            if lst[i] == item and lst[i] not in temp:
                temp.append(lst[i])
                del lst[i]
            i = i - 1
    return


def middlest(num1, num2, num3):
    nums = []
    nums.append(num3)
    nums.append(num2)
    nums.append(num1)
    nums.sort()
    length = len(nums) // 2
    return nums[length]

def tack_on_end(lst, add, num=1):
    while num > 0:
        if isinstance(add, list):
            for x in add:
                lst.append(x)
        else:
            lst.append(add)
        num -= 1

def wondrous_count(num):
    count = 0;
    while num != 1:
        if num % 2 == 0:
            num = num / 2
        else:
            num = num * 3 + 1
        count += 1
    return count

def unique_vals(text):
    ans = []
    for key in text:
        if text[key] not in ans:
            ans.append(text[key])
    return ans



































# Below is Stephen stuff. Ignore it.

points = 0

from collections import OrderedDict
the_vars = OrderedDict()
the_vars['HAL'] = 9000
the_vars['BB'] = '8'
the_vars['R2'] = list('D2')
the_vars['C'] = ['3PO']
the_vars['WALL'] = [['E']]
the_vars['Galactica'] = { 'Karl':'Helo', 'Kara':'Starbuck', 'Lee':'Apollo', 
    'Sharon':'Boomer', 'Marge':'Racetrack', 'Louanne':'Kat' }

for var,val in the_vars.items():
    if (var not in locals() or
        type(val) != type(locals()[var]) or
        val != locals()[var]):
            print("Some variables incomplete or incorrect.")
            break
    else:
        print("{} correct +1...".format(var))
        points += 1
else:
    names = ['Germanna_levels','UMW_levels','MaryWash_levels','CNU_levels']
    for name in names:
        globals()[name] = locals()[name]
    if (Germanna_levels != UMW_levels and UMW_levels is MaryWash_levels and
        UMW_levels == CNU_levels and UMW_levels is not CNU_levels):
        points += 1
        print("levels correct +1...")
    else:
        print("Variables incomplete/incorrect.")
    

if 'plus2' in locals():
    if plus2(27) == 29:
        points += 1
        print("plus2() correct! +1")
    else:    
        print("plus2() incorrect.")
else:
    print("(plus2() incomplete.)")


if 'center' in locals():
    if (center('spiderman') == 'e' and
       center('batman') == 'tm' and
       center('') == None and
       center('thor') == 'ho'):
        points += 1
        print("center() correct! +1")
    else:    
        print("center() incorrect.")
else:
    print("(center() incomplete.)")


if 'nuke_last' in locals():
    stuff = list('abcdefedbcaerugioaidsfosa')
    nuke_last(stuff,'o')
    nuke_last(stuff,'a')
    nuke_last(stuff,'s')
    nuke_last(stuff,'e')
    nuke_last(stuff,'r')
    nuke_last(stuff,'i')
    if ''.join(stuff) == 'abcdefedbcaugioadsf':
        points += 1
        print("nuke_last() correct! +1")
    else:    
        print("stuff = {}".format(''.join(stuff)))
        print("nuke_last() incorrect.")
else:
    print("(nuke_last() incomplete.)")


if 'middlest' in locals():
    if (middlest(5,9,1) == 5 and
       middlest(1,22,3) == 3 and
       middlest(1,2,3) == 2 and
       middlest(2,2,2) == 2):
        points += 1
        print("middlest() correct! +1")
    else:    
        print("middlest() incorrect.")
    
else:
    print("(middlest() incomplete.)")


if 'tack_on_end' in locals():
    some_thing = ['a','b']
    tack_on_end(some_thing,'c')
    tack_on_end(some_thing,'d',2)
    tack_on_end(some_thing,['e','f'],2)
    tack_on_end(some_thing,['g','h','i'])
    if some_thing == ['a','b','c','d','d','e','f','e','f','g','h','i']:
        points += 1
        print("tack_on_end() correct! +1")
    else:    
        print("tack_on_end() incorrect.")
    
else:
    print("(tack_on_end() incomplete.)")


if 'wondrous_count' in locals():
    test_vals = { 1:0, 6400:31, 6401:124, 99999:226, 6171:261, 6170:36,
        75128138246:225, 75128138247:1228 }
    if all([wondrous_count(tv) == tw for tv,tw in test_vals.items()]):
        points += 1
        print("wondrous_count() correct! +1")
    else:    
        print("wondrous_count() incorrect.")
    
else:
    print("(wondrous_count() incomplete.)")


if 'unique_vals' in locals():
    uv = unique_vals({ 'Malone':32, 'Ruth':3, 'Favre':4, 'Jordan':23, 
        'Sandberg':23, 'Kobe':24, 'Jeter':2, 'Brown':32, 'Magic':32, 
        'Elway':7, 'Koufax':32, 'Mantle':7 })
    if (type(uv) == list and len(uv) == 7 and
        all([ x in uv for x in [2,3,4,7,23,24,32]])):
        points += 1
        print("unique_vals() correct! +1")
    else:    
        print("unique_vals() incorrect.")
else:
    print("(unique_vals() incomplete.)")


print(f"You got {points}/14 possible XP!")
