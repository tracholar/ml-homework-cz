# coding:utf-8
from collections import defaultdict
from random import choice

class YelpDataset(object):
    def __init__(self):
        self._ROOT = 'dataset/yelp2018/'
        self._train = self._ROOT + 'train.txt'
        self._test = self._ROOT + 'test.txt'

        self.load()

    def _load(self, name):
        data = []
        with open(name) as f:
            for line in f:
                row = line.strip().split()
                if len(row) != 3:
                    continue
                userid = row[0]
                itemid = row[1]
                weight = float(row[2])
                data.append((userid, itemid, weight))
        return data

    def load(self):
        train_data = self._load(self._train)
        test_data = self._load(self._test)

        user_uid2id = dict()
        item_iid2id = dict()

        for uid, iid, weight in (train_data + test_data):
            if uid not in user_uid2id:
                user_uid2id[uid] = len(user_uid2id)
            if iid not in item_iid2id:
                item_iid2id[iid] = len(item_iid2id)

        self._train_data, self._test_data = train_data, test_data
        self.user_uid2id, self.item_iid2id = user_uid2id, item_iid2id
        self.user_id2uid = {i : uid for uid, i in user_uid2id.items()}
        self.item_id2iid = {i : iid for iid, i in item_iid2id.items()}

    @property
    def user_num(self):
        return len(self.user_uid2id)

    @property
    def item_num(self):
        return len(self.item_iid2id)

    def _dump(self, data):
        # (uid, iid, weight) -> (uid, iid, neg_iid)
        user_item_list = defaultdict(set)
        item_list = list()
        for uid, iid, weight in data:
            user_item_list[uid].add(iid)
            item_list.append(iid)

        dump_data = []
        for uid, iid, weight in data:
            neg_iid = choice(item_list)
            u_item_set = user_item_list.get(uid)
            while neg_iid in u_item_set:
                neg_iid = choice(item_list)
            dump_data.append((self.user_uid2id[uid], self.item_iid2id[iid], self.item_iid2id[neg_iid]))

        return dump_data

    def dump(self):
        self.train_dump = self._dump(self._train_data)
        self.test_dump = self._dump(self._test_data)
        return self.train_dump, self.test_dump

if __name__ == '__main__':
    yelp = YelpDataset()
    train, test = yelp.dump()

    from torch.utils.data import DataLoader
    from itertools import islice
    train_dataloader = DataLoader(train, batch_size=2048, shuffle=True)
    test_dataloader = DataLoader(test, batch_size=102400)

    print(list(yelp.item_iid2id.items())[:100])
    print(list(yelp.user_uid2id.items())[:100])
    for uid, iid, neg_iid in train_dataloader:
        print(uid, iid, neg_iid)
        break












