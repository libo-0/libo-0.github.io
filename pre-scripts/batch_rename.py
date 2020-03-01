#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 用法： python batch_rename.py source_dir dest_dir
# 批量重命名 source_dir 目录下格式为 2020-01-12-post.md 的文件到 dest_dir 目录下的 post-2020-01-12.md

import os
import sys


def batch_rename(source_dir, dest_dir):
    """批量重命名 source_dir 目录下的文件名格式为 2020-01-12-post.md 的文件为 post-2020-01-12.md"""

    if source_dir is None:
        usage()
    elif os.path.isfile(source_dir):
        print('source_dir must be a directory')
    if dest_dir is None:
        dest_dir = 'result'
    elif not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    if os.path.isfile(dest_dir):
        print('dest_dir must be a directory')
    elif os.path.isdir(dest_dir) and len(os.listdir(dest_dir)) > 0:
        print('dest_dir not empty!')
    else:
        for file in os.listdir(source_dir):
            date = file[0:10]
            name = file[11:-3]
            new_name = name + '-' + date + '.md'
            print(new_name)
            os.rename(source_dir + '/' + file, dest_dir + '/' + new_name)


def usage():
    """usages"""
    usages = "rename source_dir [dest_dir]\n"
    print(usages)


def main(argv):
    if len(argv) < 2:
        usage()
    elif len(argv) < 3:
        batch_rename(argv[1], None)
    else:
        batch_rename(argv[1], argv[2])


if __name__ == '__main__':
    main(sys.argv)
