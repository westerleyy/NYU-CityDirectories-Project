#! /usr/bin/env python

import argparse
import json
import os
from fuzzywuzzy import fuzz

def check_json(args):
    for file in os.listdir(args.input):
        if file.endswith("labeled.json"):
            with open(args.input + file) as f:
                labeled_json_recs = []
                list_json = [i.strip() for i in f.readlines() if len(i)]
                for rec in list_json:
                    entry_json = json.loads(rec)
                    try:
                        if rec_json['locations'][0]['value'] != 'null':
                            labeled_json_recs.append(entry_json)
                    except:
                        labeled_json_recs.append(entry_json)
            f.close()
            with open(args.test + file.replace('_cropped.hocr','_validate')) as f:
                validate_json = json.loads(f.read())
                print(len(validate_json))
            f.close()
            curr_index = 0
            for labeled_entry in labeled_json_recs:
                # name/subject

                name_score = fuzz.ratio(labeled_entry['subjects'], validate_json[curr_index]['name'])
                print("Machine: ", labeled_entry['subjects'])
                print("Human: ", validate_json[curr_index]['name'])
                print(name_score)
                # occupations

                occ_score = fuzz.ratio(labeled_entry['subjects'], validate_json[curr_index]['name'])

                #

                # if name_score > 98:
                #     print("Machine: ", labeled_entry['subjects'])
                #     print("Human: ", validate_json[curr_index]['name'])
                # else:
                if curr_index < len(validate_json) - 1:
                    curr_index+=1



def main():
    parser=argparse.ArgumentParser(description="Check a directory of labeled JSON outputs against test versions of the same")
    parser.add_argument("-in", help = "Input file directory", dest="input", type=str, required=True)
    parser.add_argument("-test",help="Test files directory" ,dest="test", type=str, required=True)
    parser.set_defaults(func=check_json)
    args=parser.parse_args()
    args.func(args)

if __name__=="__main__":
    main()