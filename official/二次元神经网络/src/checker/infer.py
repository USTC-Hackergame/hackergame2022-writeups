import io
import json
import base64

import torch
import matplotlib
import matplotlib.image

from models import SimpleGenerativeModel


def infer(pt_file):
    # load input data
    tag_ids = torch.load("dataset/tags_10.pt", map_location="cpu")

    # args
    n_tags = 63
    dim = 8
    img_shape = (64, 64, 3)

    # load model
    model = SimpleGenerativeModel(n_tags=n_tags, dim=dim, img_shape=img_shape)
    model.load_state_dict(torch.load(pt_file, map_location="cpu"))

    # generate noise
    torch.manual_seed(0)
    n_samples = tag_ids.shape[0]
    noise = torch.randn(n_samples, dim)

    # forward
    with torch.no_grad():
        model.eval()
        predictions = model(noise, tag_ids).clamp(0, 1)

    gen_imgs = []
    for i in range(n_samples):
        out_io = io.BytesIO()
        matplotlib.image.imsave(out_io, predictions[i].numpy(), format="png")
        png_b64 = base64.b64encode(out_io.getvalue()).decode()
        gen_imgs.append(png_b64)

    # save the predictions
    json.dump({"gen_imgs_b64": gen_imgs}, open("/tmp/result.json", "w"))


if __name__ == "__main__":
    infer(open("checkpoint/model.pt", "rb"))
    print(open("/tmp/result.json", "r").read())
