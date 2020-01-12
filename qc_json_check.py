#! /usr/bin/env python

import argparse
import json
import os
import difflib

def check_json(args):
    for file in os.listdir(args.input):
        if file.endswith("labeled.json"):
            with open(args.input + file) as f:
                labeled_json_recs = []
                list_json = [i.strip() for i in f.readlines() if len(i)]
                for rec in list_json:
                    entry_json = json.loads(rec)
                    try:
                        if entry_json['locations'][0]['value'] != 'null':
                            labeled_json_recs.append(entry_json)
                    except:
                        if len(entry_json['locations']) != 0:
                            labeled_json_recs.append(entry_json)
            f.close()
            labeled_txt = ""
            for entry in labeled_json_recs:
                labeled_txt += ' '.join([i for i in entry['subjects']]) + ' '
                labeled_txt += ' '.join([i for i in entry['occupations']]) + ' '
                locations_list = sorted(entry['locations'], key=lambda x:x['value'])
                for loc in locations_list:
                    labeled_txt += loc['value'] + ' '
                    try:
                        labeled_txt += ' '.join([k for k in loc['labels']]) + ' '
                    except:
                        pass
                labeled_txt = labeled_txt.rstrip() + '\n'
            labeled_txt = labeled_txt.replace('\n\n', '\n')
            with open(args.test + file.replace('_cropped.hocr','_validate')) as f:
                validate_json = json.loads(f.read())
            f.close()
            validate_txt = ""
            for val_entry in validate_json:
                validate_txt += val_entry['name'] + ' '
                validate_txt += ' '.join([i for i in val_entry['occupations']]) + ' '
                locations_list = sorted(val_entry['locations'], key=lambda x:x['value'])
                for loc in locations_list:
                    validate_txt += loc['value'] + ' '
                    try:
                        validate_txt += ' '.join([k for k in loc['labels']]) + ' '
                    except:
                        pass
                validate_txt = validate_txt.rstrip() + '\n'
            validate_txt = validate_txt.replace('\n\n', '\n')
            d = difflib.SequenceMatcher(a=validate_txt.split('\n'), b=labeled_txt.split('\n'))
            print("Diff score for ", file, ": ", d.ratio())



def main():
    parser=argparse.ArgumentParser(description="Check a directory of labeled JSON outputs against test versions of the same")
    parser.add_argument("-in", help = "Input file directory", dest="input", type=str, required=True)
    parser.add_argument("-test",help="Test files directory" ,dest="test", type=str, required=True)
    parser.set_defaults(func=check_json)
    args=parser.parse_args()
    args.func(args)

if __name__=="__main__":
    main()