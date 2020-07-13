import os
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='')
ori_data_dir = '../data/full_data'

'''
    data_dir -
        tmp -
        imgs
        tags.csv
'''
if __name__ == "__main__":
    parser.add_argument('--data_dir', dest='data_dir', help='Please specify an empty folder', default='/root/data/anime_heads', type=str)
    args = parser.parse_args()
    data_dir = Path(args.data_dir)
    tmp_dir = data_dir/'tmp'

    os.system(f"mkdir -p {tmp_dir}")
    os.system(f"cp {ori_data_dir}/data.zip {tmp_dir}")
    os.system(f"7z x {tmp_dir/'data.zip'} -o{tmp_dir}")

    os.system(f"mv {tmp_dir/'extra_data/images'} {data_dir/'imgs'}")
    os.system(f"mv {tmp_dir/'extra_data/tags.csv'} {data_dir}")
    os.system(f"rm -rf {tmp_dir}")