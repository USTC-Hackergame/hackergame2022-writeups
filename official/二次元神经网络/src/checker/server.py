import io
import json
import base64
import os
import sys
import logging

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"


logging.disable(logging.CRITICAL)


if __name__ == "__main__":
    binary = input("Base64 of binary: ")
    binary = base64.b64decode(binary)
    try:
        buffer_stdout = io.StringIO()
        buffer_stderr = io.StringIO()
        sys.stdout = buffer_stdout
        sys.stderr = buffer_stderr
        from infer import infer

        f = io.BytesIO(binary)
        infer(f)
    except Exception as e:
        pass

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    print(open("/tmp/result.json", "r").read())
