import numpy as np
import torch
import torch.nn as nn


class TagEncoder(nn.Module):
    def __init__(self, n_tags, output_dim):
        super().__init__()
        self.embedding = nn.Embedding(n_tags, output_dim, padding_idx=0)

    def forward(self, tag_ids: torch.Tensor) -> torch.Tensor:
        # input: batched tag ids (padding idx: 0), (batch_size, max_seq_len)
        # output: batched tag embeddings, (batch_size, output_dim)
        text = self.embedding(tag_ids).sum(dim=1)
        return text


class SimpleGenerativeModel(nn.Module):
    def __init__(self, n_tags: int, dim: int, img_shape: tuple):
        super().__init__()
        self.n_tags = n_tags
        self.img_shape = img_shape

        # (tag ids) -> dim
        self.tag_encoder = TagEncoder(n_tags=n_tags, output_dim=dim)

        # 2 * dim -> dim -> W * H * C
        self.model = nn.Sequential(
            nn.Linear(2 * dim, dim),
            nn.ReLU(),
            nn.Linear(dim, dim),
            nn.ReLU(),
            nn.Linear(dim, np.prod(img_shape)),
            nn.Tanh(),
        )

    def forward(self, noise: torch.Tensor, tag_ids: torch.Tensor) -> torch.Tensor:
        # input: batched noise and tag ids
        # output: batched generated images
        tag_emb = self.tag_encoder(tag_ids)
        x = torch.cat([noise, tag_emb], dim=-1)
        x = self.model(x)
        x = x.view(x.shape[0], *self.img_shape)
        return x
