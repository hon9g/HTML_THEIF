import requests
from bs4 import BeautifulSoup
import re
from collections import Counter, OrderedDict
from itertools import chain

### Get Text from HTML
def GetTxt(URL,TYPE):
    req = requests.get(URL)
    txt = req.text  # Include HTML tag
    if TYPE.lower() == 'html':
        soup = BeautifulSoup(txt, 'html.parser')
        txt = soup.get_text() # without HTML tag
    return txt

### Sort english and numbers separately
def GetOrdered(txt):
    nums = sorted(re.findall('[0-9]', txt))
    engs = re.findall('[a-zA-Z]', txt)
    order='AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    od = OrderedDict.fromkeys(order)
    c = Counter(engs) # Counter is log n
    engsSorted = []
    for k, v in c.items(): # 48 iter
        od[k]=v
    for k in od: # 48 iter
        if od[k] != None:
            engsSorted += [k]*od[k]
    return engsSorted, nums

### Mix english and numbers
def Mix(engs, nums):
    longer = engs[len(nums):] if len(engs) > len(nums) else nums[len(engs):]
    total = list(chain.from_iterable(zip(engs, nums))) + longer # (n-l)//2 iter
    return total

### PRINT
def Printing(total):
    print('Floor division // 👇')
    j=0
    for i in range(len(total)//K): # n // K iter
        print(''.join(total[j:j+K]))
        j += K
    print()
    print('Total {} Units( each length: {} ) 😲'.format(len(total)//K, K))
    print()
    print('Modulus % 👇')
    lenM = len(total)%K
    if not lenM == 0:
        print(''.join(total[-lenM:]))
    print('Total length of Modulus {} 🤭'.format(lenM))
    print()

if __name__ == '__main__':
    while 1:
        URL = input('URL: ')
        try:
            requests.get(URL)
        except:
            print('URL is not Valid')
            continue
        TYPE = input('TYPE: ')
        if TYPE.lower() not in ['txt', 'html']:
            print('TYPE is \'TXT\' or \'HTML\'')
            continue
        K = input('Length of Unit: ')
        try:
            K = int(K)
        except ValueError:
            print('Length is integer.')
            continue
        txt = GetTxt(URL, TYPE)
        engs, nums = GetOrdered(txt)
        if len(engs)+len(nums) == 0:
            print('There are NO english and number')
            continue
        mixed = Mix(engs, nums)
        Printing(mixed)
