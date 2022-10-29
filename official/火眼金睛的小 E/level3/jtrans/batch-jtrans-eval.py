
import os
import sys
import pickle
import numpy as np
import pathlib
import torch
from tqdm import tqdm
import argparse
from transformers import BertTokenizer, BertForMaskedLM, BertModel
from torch.utils.data import DataLoader
from torch.nn.parallel import DataParallel

parser = argparse.ArgumentParser()
parser.add_argument('problem_dir')
args = parser.parse_args()


os.chdir('/home/elsa/Code/jTrans')
sys.path.append('/home/elsa/Code/jTrans')

if True:
    import data


problem_dir = pathlib.Path(args.problem_dir)
problems = list([p for p in problem_dir.iterdir() if p.is_dir()])


if (problem_dir / 'tokens.pkl').exists():
    with open(problem_dir / 'tokens.pkl', 'rb') as f:
        tokens = pickle.load(f)

        all_input_ids = tokens['all_input_ids']
        all_mask = tokens['all_mask']
        all_problem_func_addr = tokens['all_problem_func_addr']

else:
    all_input_ids = None
    all_mask = None
    all_problem_func_addr = []

    tokenizer = BertTokenizer.from_pretrained('./jtrans_tokenizer/')

    for problem_folder in tqdm(problems):
        src_pkl = problem_folder / 'src.pkl'
        dst_pkl = problem_folder / 'dst.pkl'

        src_target_addr = problem_folder / 'src_target_addr'
        with src_target_addr.open('r') as f:
            src_target_addr = int(f.read(), 16)

        with src_pkl.open('rb') as f:
            src_data = pickle.load(f)

        with dst_pkl.open('rb') as f:
            dst_data = pickle.load(f)

        problem_func_addr = []
        problem_func_str = []

        src_func = None
        for func, func_data in src_data.items():
            if func_data[0] == src_target_addr:
                src_func = (func_data[0], data.gen_funcstr(func_data, True))
                problem_func_addr.append(src_func[0])
                problem_func_str.append(src_func[1])
                break

        # print('func count', len(dst_data))
        for func, func_data in dst_data.items():
            dst_func = (func_data[0], data.gen_funcstr(func_data, True))
            problem_func_addr.append(dst_func[0])
            problem_func_str.append(dst_func[1])

        all_problem_func_addr.append(problem_func_addr)

        tokens = tokenizer(problem_func_str, add_special_tokens=True, max_length=512,
                           padding='max_length', truncation=True, return_tensors='pt')
        input_ids = tokens['input_ids'].cuda()
        mask = tokens['attention_mask'].cuda()

        if all_input_ids is None or all_mask is None:
            all_input_ids = input_ids
            all_mask = mask
        else:
            all_input_ids = torch.cat((all_input_ids, input_ids), dim=0)
            all_mask = torch.cat((all_mask, mask), dim=0)

    assert all_input_ids is not None
    assert all_mask is not None

    with open(problem_dir / 'tokens.pkl', 'wb') as f:
        pickle.dump({
            'all_input_ids': all_input_ids,
            'all_mask': all_mask,
            'all_problem_func_addr': all_problem_func_addr
        }, f)

if (problem_dir / 'embedding.pkl').exists():
    with open(problem_dir / 'embedding.pkl', 'rb') as f:
        all_embs = pickle.load(f)
else:
    all_embs = None

    class BinBertModel(BertModel):
        def __init__(self, config, add_pooling_layer=True):
            super().__init__(config)
            self.config = config
            self.embeddings.position_embeddings = self.embeddings.word_embeddings

    device = torch.device("cuda:0")

    model = BinBertModel.from_pretrained('./models/jTrans-finetune')
    # model = DataParallel(
    #     model, device_ids=[0, 1, 2, 3], output_device=0)
    model.to(device)

    batch_size = 256

    for i in tqdm(range(0, len(all_input_ids), batch_size)):
        with torch.no_grad():
            batch_ids = all_input_ids[i:i+batch_size]
            batch_mask = all_mask[i:i+batch_size]
            output = model(batch_ids, attention_mask=batch_mask)
            anchor = output.pooler_output
            embs = anchor.detach().cpu()

            if all_embs is None:
                all_embs = embs
            else:
                all_embs = torch.cat((all_embs, embs), dim=0)

    assert all_embs is not None
    with open(problem_dir / 'embedding.pkl', 'wb') as f:
        pickle.dump(all_embs, f)

pos = 0
for problem_folder, func_addr in zip(problems, all_problem_func_addr):
    src_emb = all_embs[pos]
    dst_emb = all_embs[pos + 1: pos + len(func_addr)]
    sim = src_emb @ dst_emb.T
    sim /= torch.norm(src_emb) * torch.norm(dst_emb, dim=1)
    max_idx = torch.argmax(sim).item()
    # print(f'dst addr = {hex(problem_func_addr[1 + max_idx])}')

    with (problem_folder / 'dst_target_addr').open('w') as f:
        f.write(hex(func_addr[1 + max_idx]))

    with (problem_folder / 'jtrans_pred').open('w') as f:
        sorted_values, indices = torch.sort(sim, descending=True)

        for val, idx in zip(sorted_values, indices):
            f.write(f'{hex(func_addr[idx + 1])}\t{val.item()}\n')

    pos += len(func_addr)
