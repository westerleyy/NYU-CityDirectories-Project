import numpy as np
from bs4 import BeautifulSoup
from sklearn.cluster import KMeans
from math import sqrt
from statistics import mean
from PIL import Image, ImageOps, ImageDraw
import re
import json


# Page Array Structure
# col 0 = ID number of line
# col 1-4 = bbbox x1, y1, x2, y2
# col 5 = 0:col line; 1: indent line; 2:kill line
# col 6 = 1:col 1; 2: col2 (column assignment)
# col 7 = 0:ok to append, 1: not ok (likely gap)


def imagebuilder(r, col_locations, image_filename, std, gap_locations):
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

    # Draw the gap lines

    for gap_location in gap_locations:
        overlay.line([(0, gap_location), (pageimg.size[0], gap_location)],
                     fill=(0, 0, 0, 127), width=4)


    pageimg.show()

def load_hocr_lines(filepath):
    page_array = []
    rawhtml = BeautifulSoup(open(filepath, encoding='utf-8'), "lxml")
    for line in rawhtml.html.body.div.find_all('span'):
        line_list = []
        if line['class'][0] == 'ocr_line':
            
            # We do a check to weed out any junk lines with no alphanumeric characters
            
            check_for_chars = []
            for child in line.children:
                check_for_chars.append(child.string)
            check_for_chars = ' '.join(check_for_chars)
            if re.search(r'[A-Za-z0-9]+', check_for_chars):
                line_list.append(int(line['id'].split('_')[2]))
                line_list += [int(i) for i in line['title'].split(';')[0].split(' ')[1:]]
                line_list += [0,0,0]
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
        # Col 1 identification:
        if abs(r[i:i + 1, 1] - top_cands[0]) < (std1 / 32):
            r[i:i + 1, 6] = 1
        # Col 2 identification:
        elif abs(r[i:i + 1, 1] - top_cands[1]) < (std2 / 32):
            r[i:i + 1, 6] = 2
    else:
        r[i:i+1,5] = 2
    #Adding back in indents
    if r[i:i + 1, 5] == 2 and r[i:i + 1, 1] - (top_cands[0] + (std1 /8)) < 0:
        #Col 1 indent identification
        r[i:i + 1, 5] = 1
        r[i:i + 1, 6] = 1
    elif r[i:i + 1, 5] == 2 and r[i:i + 1, 1] - (top_cands[1] + (std2 /8 )) < 0:
        # Col 2 indent identification
        r[i:i + 1, 5] = 1
        r[i:i + 1, 6] = 2
    #Re-eliminating anything to left of column 1
    if r[i:i+1, 1] < (min(top_cands) - (std1/32)):
       r[i:i + 1, 5] = 2
 
##
#   Pass to find lines flush with a column whose y vals make them unlikely to be in the page block for entries
##

reduced_array = r[r[:,5] !=2]
sorted_y_array = np.sort(reduced_array.view('i8,i8,i8,i8,i8,i8,i8,i8'), order=['f2'], axis=0).view(np.int)

half_page = len(sorted_y_array)//2
hp_line_y = sorted_y_array[half_page:half_page+1,2]
gap = float(r[-2:-1,2]*.10)
entry_density = len([i for i in sorted_y_array[:,2] if abs(i - sorted_y_array[half_page:half_page+1,2]) < gap/2])


for i in range(len(sorted_y_array)):
    proximate_lines = [yval for yval in sorted_y_array[:,2] if abs(yval - sorted_y_array[i:i+1,2]) < gap/2]
    if len(proximate_lines) - 1 < entry_density/2:
        top_line_proximate_lines = [yval for yval in sorted_y_array[:, 2] if yval - sorted_y_array[i:i + 1, 2] < gap \
                                    and yval - sorted_y_array[i:i + 1, 2] > 0]
        bottom_line_proximate_lines = [yval for yval in sorted_y_array[:, 2] if \
                                    sorted_y_array[i:i + 1, 2] - yval < gap and sorted_y_array[i:i + 1, 2] - yval > 0]
        if len(top_line_proximate_lines) > entry_density or len(bottom_line_proximate_lines) > entry_density:
            pass
        else:
            sorted_y_array[i:i+1,5] = 2
        
##
#   Pass to look for missing lines
##

line_only_array = sorted_y_array[sorted_y_array[:,5] != 2]
sorted_line_only_array = np.sort(line_only_array.view('i8,i8,i8,i8,i8,i8,i8,i8'), order=['f6','f2'], axis=0).view(np.int)
sample_lines = sorted_line_only_array[int(len(sorted_line_only_array)*.15):int(len(sorted_line_only_array)*.30),:]
gaps = []

for i in range(len(sample_lines)):
    try:
        gaps.append(int(sample_lines[i+1:i+2,2] - sample_lines[i:i+1,2]))
    except:
        pass

average_line_gap = sum(gaps) // len(sample_lines)
gap_locations = []
for i in range(len(sorted_line_only_array)):
    try:
        if int(sorted_line_only_array[i + 1:i + 2, 2] - sorted_line_only_array[i:i + 1, 2]) > average_line_gap*1.95:
            #print("Likely line missing after line: ", i)
            gap_locations.append(sorted_line_only_array[i:i + 1, 2] + average_line_gap*1.5)
    except:
        pass


jpeg_path = '/Users/Nicholas/Desktop/TEMP-NYU-DIRECTORIES-PROJECT-OFFLINE/test-verification-files/1875.4b4b2b90-317a-0134-6800-00505686a51c/cropped-jpegs/198.56789039.6c645950-5cec-0134-2c5e-00505686a51c_cropped.jpeg'
#print(r[:,5])
imagebuilder(sorted_line_only_array, top_cands, jpeg_path, std, gap_locations)