# coding:utf-8
"""
生成数据集
"""
import sys

data_dir = '~/Documents/code/dataset/淘宝点 击率转化率预估数据集/'
train_file = data_dir + 'sample_train/'
test_file = data_dir + 'sample_test/'


def parse_feat_list(s):
    row = s.split(chr(0x01))
    feat_map = []
    for kv in row:
        ffid, v = kv.split(chr(0x02))
        fid, v = v.split(chr(0x03))
        feat_map.append((str(ffid), int(fid), float(v)))
    return feat_map
def read_skeleton(f):
    for line in f:
        if line is None or len(line)==0:
            continue
        row = line.strip().split(',')
        if len(row) != 6:
            continue
        sample_id = int(row[0])
        ctr_label = int(row[1])
        cvr_label = int(row[2])
        com_feat_idx = row[3]
        feat_num = int(row[4])
        feat_list = parse_feat_list(row[5])

        yield sample_id, ctr_label, cvr_label, com_feat_idx, feat_num, feat_list


def read_com_feat(f):
    for line in f:
        if line is None or len(line)==0:
            continue
        row = line.strip().split(',')
        if len(row) != 3:
            continue

        com_feat_idx = row[0]
        feat_num = int(row[1])
        feat_list = parse_feat_list(row[2])
        yield com_feat_idx, feat_num, feat_list


if __name__ == '__main__':
    from tqdm import tqdm
    if sys.argv[1] == 'skeleton':
        func = read_skeleton
    elif sys.argv[1] == 'comfeat':
        func = read_com_feat
    else:
        raise Exception('not found func')

    for record in tqdm(func(sys.stdin)):
        print(record)



