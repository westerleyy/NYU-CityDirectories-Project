import argparse

def process_directories(args):
    import os
    path = args.input
    # return original directory as a check
    print("Current working directory: " + os.getcwd())

    # change working directory to path given above
    os.chdir(path)

    print("New working directory: " + os.getcwd())

    # sub-directories required
    sub_dir_req = ["bbox-images", "cropped-jpegs", "final-entries", "hocr", "manifest", "tsv"]

    # Create sub-directories
    for x in os.listdir():
        if os.path.isdir(x):
            for sub_dir in sub_dir_req:
                sub_dir_path = x + "/" + sub_dir
                os.makedirs(sub_dir_path)


def main():
    parser=argparse.ArgumentParser(description="Create subdirectories within each pre-processed directory.")
    parser.add_argument("-in", help="Input file directory", dest="input", type=str, required=True)
    parser.set_defaults(func=process_directories)
    args=parser.parse_args()
    args.func(args)

if __name__=="__main__":
    main()