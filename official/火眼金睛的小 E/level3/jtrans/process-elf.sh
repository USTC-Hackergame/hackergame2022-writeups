#!/bin/bash

elf_path=$1
idb_path=$2
log_file_path=$3

# TODO: 替换为 IDA 的地址
ida_binary="idapro/idat64"

# TODO: 替换为 clone 得到的 jTrans 的 repo 地址
pushd jTrans/datautils

"$ida_binary" -L$log_file_path -c -A -S"process.py" -o$idb_path $elf_path
