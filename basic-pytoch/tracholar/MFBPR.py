# coding:utf-8
import torch
from torch.nn import Module, Embedding
from data import YelpDataset
from tqdm import tqdm

class MFModel(Module):
    def __init__(self, user_num, item_num, dim=128):
        super(MFModel, self).__init__()
        self.u = Embedding(user_num, dim)
        self.i = Embedding(item_num, dim)

    def forward(self, x):
        u, i, neg_i = x
        return self.u(u), self.i(i), self.i(neg_i)


def bpr_loss(u, i, negi):
    y = torch.sigmoid(torch.mul(u, i - negi).sum(dim=1))
    loss = -torch.log(1e-8 + y)
    return loss.mean()

def reg_loss(reg, emb):
    return reg * torch.norm(emb, p=2)


def train_step():
    yelp = YelpDataset()
    train, test = yelp.dump()
    model = MFModel(yelp.user_num, yelp.item_num, 4).cuda()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-2)

    from torch.utils.data import DataLoader
    train_dataloader = DataLoader(train, batch_size=2048, shuffle=True)

    reg = 1e-2
    for epoch in range(10):
        for uid, iid, neg_iid in tqdm(train_dataloader):
            model.train()

            uid, iid, neg_iid = [x.to('cuda') for x in [uid, iid, neg_iid]]
            tu, ti, tneg_i = model([uid, iid, neg_iid])
            loss = bpr_loss(tu, ti, tneg_i) + reg_loss(reg, tu) + reg_loss(reg, ti) + reg_loss(reg, tneg_i)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()


        # eval
        with torch.no_grad():
            uid, iid, neg_iid = [torch.tensor(x, dtype=int, device='cuda') for x in zip(*test)]
            tu, ti, tneg_i = model([uid, iid, neg_iid])
            loss = bpr_loss(tu, ti, tneg_i)

            print(f'{epoch} loss = {loss.item():.4f}', flush=True)

    torch.save(model.state_dict(), 'model/mfbpr.pth')


if __name__ == '__main__':
    train_step()