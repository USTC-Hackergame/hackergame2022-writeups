# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from tqdm import tqdm
import argparse
import pathlib
import pickle
import torch
import numpy as np
import sys
if True:
    import sys
    sys.path.append('SAFEtorch')
    from safetorch.parameters import Config
    from safetorch.safe_network import SAFE
    from utils.radare_analyzer import BinaryAnalyzer
    from utils.capstone_disassembler import disassemble
    from utils.instructions_converter import InstructionsConverter
    from utils.function_normalizer import FunctionNormalizer

parser = argparse.ArgumentParser()
parser.add_argument('problem_dir', type=pathlib.Path)
args = parser.parse_args()

problem_dir = args.problem_dir.resolve()

# initialize SAFE
config = Config()
safe = SAFE(config)

# load instruction converter and normalizer
I2V_FILENAME = "SAFEtorch/model/word2id.json"
converter = InstructionsConverter(I2V_FILENAME)
normalizer = FunctionNormalizer(max_instruction=150)

# load SAFE weights
SAFE_torch_model_path = "SAFEtorch/model/best_model.pth"
state_dict = torch.load(SAFE_torch_model_path)
safe.load_state_dict(state_dict['state_dict'])
safe = safe.to('cuda')
safe = safe.eval()

problems = list([p for p in problem_dir.iterdir() if p.is_dir()])


def call_ra2(problem_folder):
    try:
        def analyse_func(binary_path, addr):
            binary = BinaryAnalyzer(binary_path)
            offsets = binary.get_functions()

            if addr not in offsets:
                return None
            # print(hex(addr))
            asm = binary.get_hexasm(addr)
            # print(asm)
            instructions = disassemble(asm, binary.arch, binary.bits)
            # print(instructions)
            converted_instructions = converter.convert_to_ids(instructions)
            instructions, length = normalizer.normalize_functions(
                [converted_instructions])
            return instructions, length

        def analyse_binary(binary_path):
            binary = BinaryAnalyzer(str(binary_path))
            offsets = binary.get_functions()

            ret = {}

            func_offset = []
            func_instrs = []
            func_length = []

            # generate each function embedding
            for offset in offsets:
                asm = binary.get_hexasm(offset)
                instructions = disassemble(asm, binary.arch, binary.bits)
                converted_instructions = converter.convert_to_ids(instructions)
                instructions, length = normalizer.normalize_functions(
                    [converted_instructions])

                instructions = torch.tensor(np.array(instructions))

                func_offset.append(offset)
                func_instrs.append(instructions)
                func_length.append(length)

            func_instrs = torch.vstack(func_instrs)
            func_length = torch.LongTensor(func_length).unsqueeze(1)

            return func_offset, func_instrs, func_length

        src_target_addr = problem_folder / 'src_target_addr'
        with src_target_addr.open('r') as f:
            src_target_addr = int(f.read(), 16)

        src_func_info = analyse_func(
            str(problem_folder/'src'), src_target_addr)
        dst_info = analyse_binary(problem_folder / 'dst')

        # print(src_func_info)

        return src_func_info, dst_info
    except Exception as e:
        print(e)


def analyse(problem_folder, src_func_info, dst_info):
    func_instrs = torch.vstack([torch.tensor(np.array(src_func_info[0])), dst_info[1]]).to('cuda')

    func_length = torch.vstack([torch.tensor(np.array([src_func_info[1]])), dst_info[2].squeeze(1)]).to('cuda')

    function_embeddings = []

    for i in range(len(func_length)):
        function_embeddings.append(safe(func_instrs[i], func_length[i]).to('cuda'))

    function_embeddings = torch.vstack(function_embeddings)
    src_func_emb = function_embeddings[0]
    dst_func_emb = function_embeddings[1:]

    src_func_emb = src_func_emb / src_func_emb.norm()
    dst_func_emb = dst_func_emb / dst_func_emb.norm(dim=1, keepdim=True)

    similarity = torch.matmul(src_func_emb, dst_func_emb.t()).detach()
    similarity = similarity.cpu().numpy()
    max_index = similarity.argmax()

    dst_addr = [addr for addr in dst_info[0]][max_index]

    with open(problem_folder / 'safe_dst_target_addr', 'w') as f:
        f.write(hex(dst_addr))


def process(problem_folder):
    # print(problem_folder)
    src_binary = problem_folder/'src'
    dst_binary = problem_folder/'dst'
    dst_addr = 0
    try:
        src_embedding = analyse(str(src_binary))
        dst_embedding = analyse(str(dst_binary))

        # print([hex(x) for x in list(src_embedding.keys())])

        dst_func_dst = list(dst_embedding.keys())

        dst_emb_torch = torch.vstack([dst_embedding[offset]
                                      for offset in dst_func_dst])

        src_target_addr = problem_folder / 'src_target_addr'
        with src_target_addr.open('r') as f:
            src_target_addr = int(f.read(), 16)
        # print('src_target_addr', hex(src_target_addr))
        src_func_emb = src_embedding[src_target_addr]

        sim = src_func_emb @ dst_emb_torch.T / \
            (src_func_emb.norm() * dst_emb_torch.norm(dim=1))

        index = torch.argmax(sim)
        dst_addr = dst_func_dst[index]
    except KeyError as e:
        print('exception', e)

    with open(problem_folder/'safe_dst_target_addr', 'w') as f:
        f.write(hex(dst_addr))


if (problem_dir / 'safe_func_info.pkl').exists():
    with open(problem_dir / 'safe_func_info.pkl', 'rb') as f:
        all_results = pickle.load(f)
else:
    all_results = []

    for problem_folder in tqdm(problems):
        # print(problem_folder)
        all_results.append([problem_folder, call_ra2(problem_folder)])
        # process(problem_folder)

    with open(problem_dir / 'safe_func_info.pkl', 'wb') as f:
        pickle.dump(all_results, f)


for problem_folder, batch in all_results:
    if batch[0] is None:
        continue
    analyse(problem_folder, *batch)
