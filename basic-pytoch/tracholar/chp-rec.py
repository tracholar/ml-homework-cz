# coding:utf-8
# pytorch for rec
import os
import torch
import torchrec
import torch.distributed as dist

os.environ["RANK"] = "0"
os.environ["WORLD_SIZE"] = "1"
os.environ["MASTER_ADDR"] = "localhost"
os.environ["MASTER_PORT"] = "29500"

dist.init_process_group(backend='nccl')

torchrec.EmbeddingBagCollection(
    device="meta",
    tables=[

    ]
)