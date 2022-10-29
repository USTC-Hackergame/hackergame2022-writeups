import pickle
import pathlib
import random
import os
from math import ceil
import time


base_url = os.getenv('BASE_URL', 'http://localhost:20001')

token = os.getenv('hackergame_token', '1:123')

user_id = int(token.split(':')[0])


def main(frontend_info, round, src_optimize_level, dst_optimize_level, dry_run=False):
    correct_time = 0

    for idx in range(round):
        print(f'Challenge {idx + 1} of {round}')
        selected_binary = random.choice(frontend_info)

        src_binary_hash_path = selected_binary['stripped_binary_path_hash'][src_optimize_level]
        dst_binary_hash_path = selected_binary['stripped_binary_path_hash'][dst_optimize_level]

        print(f'1st binary: {base_url}/{src_binary_hash_path}')
        print(f'2nd binary: {base_url}/{dst_binary_hash_path}')

        selected_func_name = random.choice(
            list(selected_binary['all_func_addr'].keys()))

        func_across_binary_info = selected_binary['all_func_addr'][selected_func_name]

        addr_in_src = func_across_binary_info[src_optimize_level]
        addr_in_dst = func_across_binary_info[dst_optimize_level]

        print(
            f'There is a function at {hex(addr_in_src)} in the first binary.')
        print('And there is a function very similar to the function mentioned above in the second binary.')
        print('Please show me the address of that function (in hex): ')

        while True:
            try:
                user_input = int(input(), 16)
            except Exception:
                print('Invalid input')
                continue
            break

        if dry_run:
            print(f'real pair: {hex(addr_in_src)} -> {hex(addr_in_dst)}')
        if user_input == addr_in_dst:
            correct_time += 1
        else:
            pass

    correct_rate = correct_time / round
    if dry_run:
        print('Your correct rate is: {:.2f}%'.format(correct_rate * 100))
    return correct_rate


def input_timestamp(time_limit):
    server_timestamp = int(time.time())

    timestamp_begin = server_timestamp - time_limit
    print('现在，将输入用于生成题目的时间戳')
    print('如果输入了两次相同的时间戳，那么你将会得到相同的题目')
    print('而如果两次输入的时间戳相差 10 分钟或以上，你将会得到不同的题目')
    print('本次连接允许的输入的时间戳的范围是: [{}, {}]'.format(
        timestamp_begin, server_timestamp))
    print('即：如果你在本次连接中拿到了题目，你将有最多 {} 分钟的时间来提交结果'.format(
        time_limit // 60))
    print('Please input the timestamp:', end=' ')

    start_timestamp = int(input())

    if timestamp_begin <= start_timestamp <= server_timestamp:
        return start_timestamp

    raise Exception("Invalid timestamp, out of range")


if __name__ == '__main__':
    print('Choose your difficulty')
    print('1. Very easy')
    print('2. Somewhat easy')
    print('3. Easy')
    level = int(input())

    params = {
        1: [2, 'O1', 'O2'],
        2: [100, 'O1', 'O2'],
        3: [200, 'O0', 'O3'],
    }

    requirement = {
        1: 1.0,
        2: 0.4,
        3: 0.3,
    }

    time_limit = {
        1: 24 * 60 * 60,
        2: 60 * 60,
        3: 3 * 60 * 60,
    }

    if level in params:
        print('Do you want to perform dry run, so that you can see how many challenges you can answer correctly? (y/N)')
        dry_run = input().lower() == 'y'

        if dry_run:
            params[level][0] = min(params[level][0], 100)

        target_correct_rate = requirement[level]

        start_timestamp = input_timestamp(time_limit[level])

        print(f'Your target correct rate is {target_correct_rate * 100}%')
        correct_num = ceil(target_correct_rate * params[level][0])
        print(
            f'That means you need to answer at least {correct_num} challenges correctly')

        random.seed((start_timestamp // 600) *
                    10000000 + user_id * 10 + level)

        frontend_info_files = list(sorted(list(pathlib.Path(
            '/frontend_info/level_{}'.format(level)).iterdir())))
        if dry_run:
            chosen_pkl = frontend_info_files[0]
        else:
            chosen_pkl = random.choice(frontend_info_files[1:])

        with open(chosen_pkl, 'rb') as f:
            frontend_info = pickle.load(f)

        correct_rate = main(frontend_info, *params[level], dry_run=dry_run)

        if not dry_run:
            if correct_rate and correct_rate >= target_correct_rate:
                print(open(f"/flag{level}", "r").read())
            else:
                print('Try again :)')
