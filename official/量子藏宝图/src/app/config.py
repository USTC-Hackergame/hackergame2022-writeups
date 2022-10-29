import os

output_dir = os.getenv('ENV_OUTPUT', "static/output/")
debug = bool(os.getenv('ENV_DEBUG', "False") == "True")
port = int(os.getenv('ENV_PORT', '18080'))

if os.getenv('ENV_KEY_LEN'):
    qkd_key_len_required = int(os.getenv('ENV_KEY_LEN'))
elif debug:
    qkd_key_len_required = 3
else:
    qkd_key_len_required = 128
