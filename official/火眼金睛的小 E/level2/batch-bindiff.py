
import re
import subprocess
from concurrent.futures import ProcessPoolExecutor
import os
import sys
import pickle
import numpy as np
import subprocess
import pathlib
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('problem_dir')
args = parser.parse_args()

problem_dir = pathlib.Path(args.problem_dir)
problems = list([x for x in problem_dir.iterdir() if x.is_dir()])


def bindiff(working_dir, src_target_addr):
    subprocess.run([
        './ida-bindiff-helper.sh', working_dir
    ])

    with open(working_dir / 'src_vs_dst.results', 'r') as f:
        results = f.read()
    pattern = re.compile(r'([0-9a-fA-F]+)\t([0-9a-fA-F]+)')
    found = False

    dst_target_addr = 0
    for src, dst in pattern.findall(results):
        src = int(src, 16)
        dst = int(dst, 16)
        if src == src_target_addr:
            print('problem target:', hex(src_target_addr))
            print('found src:', hex(src))
            print('found dst:', hex(dst))
            found = True
            dst_target_addr = dst
            break
    if not found:
        print('****Not Found****')
    with open(working_dir / 'bindiff_dst_target_addr', 'w') as f:
        f.write(hex(dst_target_addr))


with ProcessPoolExecutor(max_workers=48) as executor:
    for problem_folder in sorted(problems):
        src_idb = problem_folder / 'src.idb'
        dst_idb = problem_folder / 'dst.idb'

        src_target_addr = problem_folder / 'src_target_addr'
        with src_target_addr.open('r') as f:
            src_target_addr = int(f.read(), 16)

        executor.submit(bindiff, problem_folder, src_target_addr)
        # bindiff(problem_folder, src_target_addr)
