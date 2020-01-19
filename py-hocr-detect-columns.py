import numpy as np
from bs4 import BeautifulSoup
from sklearn.cluster import KMeans
from math import sqrt
from statistics import mean

def load_hocr_lines(filepath):
    page_array = []
    rawhtml = BeautifulSoup(open(filepath, encoding='utf-8'), "lxml")
    for line in rawhtml.html.body.div.find_all('span'):
        line_list = []
        if line['class'][0] == 'ocr_line':
            line_list.append(int(line['id'].split('_')[2]))
            line_list += [int(i) for i in line['title'].split(';')[0].split(' ')[1:]]
            page_array.append(line_list)
    return np.array(page_array)



path = '/Users/Nicholas/Desktop/TEMP-NYU-DIRECTORIES-PROJECT-OFFLINE/test-verification-files/1875.4b4b2b90-317a-0134-6800-00505686a51c/198.56789039.6c645950-5cec-0134-2c5e-00505686a51c_cropped.hocr'
r = load_hocr_lines(path)

kmeans = KMeans(n_clusters=6).fit(r[:,1].reshape(-1,1))


centroids = kmeans.cluster_centers_
cands_cols = {}

for j in range(len(centroids)):
    cands_cols[centroids[j,0]] = 0
    std = sqrt(mean([((i - centroids[j,0])**2) for i in r[:,1]]))
    print(std/8)
    for xval in r[:,1]:
        if abs(xval - centroids[j,0]) > (std/8):
            pass
            #print("This val is too far away: ", xval, centroids[j,0], std)
        else:
            cands_cols[centroids[j,0]]+=1

print(cands_cols)