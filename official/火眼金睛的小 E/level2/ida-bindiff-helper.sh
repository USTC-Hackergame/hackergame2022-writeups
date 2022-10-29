#!/bin/bash

# TODO: 这里换成 ida 的具体位置
ida_binary="PATH_TO_IDA_PRO/idapro/idat64"

working_dir=$1

cd $working_dir

# TODO: 这里需要替换为正确的路径
script_path=`pwd`/analyse.py

"$ida_binary" -Lsrc-bindiff.log -A -S"$script_path" src.i64
"$ida_binary" -Ldst-bindiff.log -A -S"$script_path" dst.i64

/opt/bindiff/bin/bindiff src.export dst.export --output_format log
