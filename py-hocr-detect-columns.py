import numpy as np
from bs4 import BeautifulSoup
from sklearn.cluster import KMeans
from math import sqrt
from statistics import mean
from PIL import Image, ImageOps, ImageDraw


# Page Array Structure
# col 0 = ID number of line
# col 1-4 = bbbox x1, y1, x2, y2
# col 5 = 0:col line; 1: indent line; 2:kill line

def imagebuilder(r, col_locations, image_filename, std):
    pageimg = Image.open(image_filename)
    overlay = ImageDraw.Draw(pageimg, 'RGBA')

    color = {0:(255,0,0,90),1:(0,0,255,90),2:(0,255,0,90)}
    ##Draw the hocr boxes
    
    for i in range(len(r)):
        overlay.polygon([(r[i:i+1, 1], r[i:i+1, 4]),
                      (r[i:i+1, 1], r[i:i+1, 2]),
                     (r[i:i+1, 3], r[i:i+1, 2]),
                     (r[i:i+1, 3], r[i:i+1, 4])],
                     fill=color[int(r[i:i+1, 5])], outline=color[int(r[i:i+1, 5])])

    # Draw the column bounds

    for loc in col_locations:

        overlay.polygon([(loc - std/32, 0), (loc + std/32, 0),
                         (loc + std/32, pageimg.size[1]),
                         (loc - std/32, pageimg.size[1])],
                        fill=(255, 1, 255, 100))
        overlay.line([(loc, 0), (loc, pageimg.size[1])],
                     fill=(0, 0, 0, 127), width=4)
    pageimg.show()

def load_hocr_lines(filepath):
    page_array = []
    rawhtml = BeautifulSoup(open(filepath, encoding='utf-8'), "lxml")
    for line in rawhtml.html.body.div.find_all('span'):
        line_list = []
        if line['class'][0] == 'ocr_line':
            line_list.append(int(line['id'].split('_')[2]))
            line_list += [int(i) for i in line['title'].split(';')[0].split(' ')[1:]]
            line_list.append(0)
            page_array.append(line_list)
    return np.array(page_array)



path = '/Users/Nicholas/Desktop/TEMP-NYU-DIRECTORIES-PROJECT-OFFLINE/test-verification-files/1875.4b4b2b90-317a-0134-6800-00505686a51c/198.56789039.6c645950-5cec-0134-2c5e-00505686a51c_cropped.hocr'
r = load_hocr_lines(path)


##
#   Pass to find our likey column locations
##

kmeans = KMeans(n_clusters=8).fit(r[:,1].reshape(-1,1))
centroids = kmeans.cluster_centers_
cands_cols = {}

for j in range(len(centroids)):
    cands_cols[centroids[j,0]] = 0
    std = sqrt(mean([((i - centroids[j,0])**2) for i in r[:,1]]))
    for i in range(len(r)):
        if abs(r[i:i+1,1] - centroids[j,0]) > (std/16):
            pass
        else:
            cands_cols[centroids[j,0]]+=1

top_cands = sorted(cands_cols.items(), key=lambda x: x[1], reverse=True)
top_cands = [i[0] for i in top_cands][0:2]

##
#  Pass to identify and keep lines that are at x-val of column edges
##

std1 = sqrt(mean([((i - top_cands[0])**2) for i in r[:, 1]]))
std2 = sqrt(mean([((i - top_cands[1])**2) for i in r[:, 1]]))
for i in range(len(r)):
    if abs(r[i:i + 1, 1] - top_cands[0]) < (std1 / 32) or abs(r[i:i + 1, 1] - top_cands[1]) < (std2 / 32):
        pass
    else:
        r[i:i+1,5] = 2
    if r[i:i + 1, 5] == 2 and (r[i:i + 1, 1] - (top_cands[0] + (std1 /8)) < 0 or r[i:i + 1, 1] - (top_cands[1] + (std2 /8 )) < 0):
        r[i:i + 1, 5] = 1
    if r[i:i+1, 1] < (min(top_cands) - (std1/32)):
        r[i:i + 1, 5] = 2
 
##
#   Pass to find lines flush with a column whose y vals make them unlikely to be in the page block for entries
##






jpeg_path = '/Users/Nicholas/Desktop/TEMP-NYU-DIRECTORIES-PROJECT-OFFLINE/test-verification-files/1875.4b4b2b90-317a-0134-6800-00505686a51c/cropped-jpegs/198.56789039.6c645950-5cec-0134-2c5e-00505686a51c_cropped.jpeg'
#print(r[:,5])
imagebuilder(r, top_cands, jpeg_path, std)