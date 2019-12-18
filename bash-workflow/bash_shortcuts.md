### Dependencies

Working with JSON in bash:
<pre>brew install jq</pre>


### Step 1: Crop [file level action]

<pre>crop_for_columns.py cropped-jpegs/</pre>

### Step 2: Tesseract (from within directory containing downloaded cropped jpegs) [file-level actions]

<pre>for page in *_cropped.jpeg; do tesseract $page ${page/.jpeg/} --psm 1 --oem 1 hocr; done;</pre>

### Step 3: HOCR Detect Columns and Conditional Random Fields [file level >> entry level]

<pre>for page in *.hocr; do hocr-detect-columns --mode json $page; done | jq .pages[0].lines[].completeText > ${page/.hocr/_lineoutput.txt}</pre>

(to send the unlabeled entries to a text file) or

<pre>for page in *.hocr; do hocr-detect-columns --mode json $page; done | jq .pages[0].lines[].completeText | sed 's/"//1' | sed 's/\\n//g' | tr -s '[:space:]' | python ../../city-directory-entry-parser/parse.py --training ../../city-directory-entry-parser/data/nyc-city-directories/nypl-labeled-70-training.csv</pre>

(to produce the entire workflow from hocr to labeled entries in json format.

### Alternate: Making test html views from the HOCR files

<pre>for page in *.hocr; do hocr-detect-columns --mode html $page; done > testing-output.html</pre>