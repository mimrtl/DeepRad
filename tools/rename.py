#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import glob
import argparse
import numpy as np


def usage():
    print("Error in input argv")


def main():
    parser = argparse.ArgumentParser(
        description='''This script aims to reshape the data folder tree for DeepRad ''',
        epilog="""All's well that ends well.""")
    parser.add_argument('--seg_name', metavar='', type=str, default="seg",
                        help='Part of names of all segmentation files.(breast1_pet)<str>')

    args = parser.parse_args()

    path_organized = os.path.join('Data_folder', 'train')
    truth_piece = "*"+args.seg_name+"*"

    list_folder = glob.glob(os.path.join(path_organized, '*'))
    for folder in list_folder:
        list_file = glob.glob(os.path.join(folder, truth_piece))
        for file in list_file:
            old_name_left = file.rfind(os.sep) + 1
            old_name_right = file.find('.')
            new_name = file[:old_name_left] + 'truth' + file[old_name_right:]
            os.rename(file, new_name)
            print("Old name:", file)
            print("New name:", new_name)
            print("---------------------------")
    print("complete")

if __name__ == "__main__":
    main()
