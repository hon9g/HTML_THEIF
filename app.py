import requests
from bs4 import BeautifulSoup
import re
from collections import Counter, OrderedDict
from itertools import chain
from flask import Flask, request, render_template

app = Flask(__name__)

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
def GetD(total, K):
    print('Floor division // 👇')
    d = []
    j=0
    for i in range(len(total)//K): # n // K iter
        d.append(''.join(total[j:j+K]))
        j += K
    return d

def GetM(total, K):
    print('Modulus % 👇')
    m = ''
    lenM = len(total) % K
    if not lenM == 0:
        m=''.join(total[-lenM:])
    print(len(m))
    return m


@app.route('/', methods=['Get','Post'])
def hello_world():
    error = ''
    try:
        if request.method == "POST":
            attempted_URL = request.form['URL']
            attempted_TYPE = request.form['TYPE']
            attempted_K = int(request.form['Length'])
            # print(attempted_URL, attempted_TYPE, attempted_K)

            if attempted_URL and attempted_TYPE and attempted_K:
                txt = GetTxt(attempted_URL, attempted_TYPE)
                engs, nums = GetOrdered(txt)
                mixed = Mix(engs, nums)
                # print(mixed)
                d = GetD(mixed, attempted_K)
                m = GetM(mixed, attempted_K)
                print(d,m)
                return render_template("index.html", division=d, modulus=m)
            else:
                error = 'please Check your inputs'
        return render_template("index.html", error=error)
    except Exception as e:
        return render_template("index.html", error=error)

if __name__ == '__main__':
    app.run()
