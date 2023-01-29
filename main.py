import pandas as pd
import requests
import time
import logging
import threading
import numpy as np

def formatData(df, start, end):
    print('formatData')
    data = []
    for i in range(start, end):
        productId = df['id'][i]
        productName = df['name'][i]
        # print(df['name'][i])
        response = requests.get('https://jsonplaceholder.typicode.com/comments/' + str(productId))
        # print(response.status_code)
        jsonData = response.json()
        commentBody = jsonData['body']
        data.append([productId, productName, commentBody])

    # print(data)
    arr = np.asarray(data)
    pd.DataFrame(arr).to_csv( 'result/' + str(start) + '-' + str(end) + 'result.csv', header  = ['productId','productName','commentBody'])
 
def executeThread(name, df, start, end):
    global result
    start_time = time.time()
    # print("Main    : before creating thread")
    z = threading.Thread(target=formatData, args=(df, start, end))
    # print("Main    : before running thread")
    z.start()
    # print("Main    : wait for the thread to finish")
    # x.join()
    # print("Main    : all done")
    # print(name + "--- %s seconds ---" % (time.time() - start_time))

def executeMultipleThread(df, executeThread, length, skip = 0):
    total = length//skip
    reste = length%skip
    # print('total %s' % total)
    # print('reste %s' % reste)
    threads = list()
    for index in range(total):
        # print("Main    : create and start thread %d.", index)
        name = str(index) + 'sd'
        start = index * skip
        end = start + skip - 1
        if index + 1 == total:
            end += reste
        # print("Debut: %d.", start)
        # print("Fin: %d.", end)
        
        x = threading.Thread(target=executeThread, args=(name, df, start, end))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        # print("Main    : before joining thread %d.", index)
        thread.join()
        # print("Main    : thread %d done", index)

df = pd.read_csv(r'assets/products.csv')
# print(df)
dataLength = len(df['name'])
print('Taille de donnees est %s' % dataLength)
print(df['name'][0])

print(type(df))
start_time = time.time()

# executeThread('T1', df, 0, 10)

executeMultipleThread(df, executeThread, dataLength, 20)

# formatData(df, 0, dataLength - 1)

print("--- %s seconds ---" % (time.time() - start_time))


