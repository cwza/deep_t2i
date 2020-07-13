import os
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='')
ori_data_dir = '../data/full_data'

'''
    data_dir -
        tmp -
        imgs -
        caps -
        images.txt
        bounding_boxes.txt
        train_test_split.txt
'''

if __name__ == "__main__":
    parser.add_argument('--data_dir', dest='data_dir', help='Please specify an empty folder', default='/root/data/birds', type=str)
    args = parser.parse_args()
    data_dir = Path(args.data_dir)
    tmp_dir = data_dir/'tmp'
    imgs_dir = data_dir/'imgs'
    caps_dir = data_dir/'caps'

    os.system(f"mkdir -p {tmp_dir}")

    # Birds images
    os.system(f"cp {ori_data_dir}/CUB_200_2011.tgz {tmp_dir}")

    os.system(f"7z x -tgzip -so {tmp_dir/'CUB_200_2011.tgz'} | 7z x -si -ttar -o{tmp_dir}")
    os.system(f"mv {tmp_dir/'CUB_200_2011/images'} {imgs_dir}")
    os.system(f"mv {tmp_dir/'CUB_200_2011/images.txt'} {data_dir}")
    os.system(f"mv {tmp_dir/'CUB_200_2011/train_test_split.txt'} {data_dir}")
    os.system(f"mv {tmp_dir/'CUB_200_2011/bounding_boxes.txt'} {data_dir}")

    # Birds Captions
    os.system(f"cp {ori_data_dir}/birds.zip {tmp_dir}")

    os.system(f"7z x {tmp_dir/'birds.zip'} -o{tmp_dir}")
    os.system(f"7z x {tmp_dir/'birds/text.zip'} -o{tmp_dir/'birds/'}")
    os.system(f"mv {tmp_dir/'birds/text'} {caps_dir}")

    # Clean
    os.system(f"rm -rf {tmp_dir}")
