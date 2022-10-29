import torch
from models import SimpleGenerativeModel

def train():
    # load data
    tag_ids = torch.load("dataset/tags_10.pt")
    pixels = torch.load("dataset/pixels_10.pt")

    # build model
    n_tags = 63
    dim = 8
    scale = 1
    imag_shape = (64, 64, 3)
    model = SimpleGenerativeModel(n_tags=n_tags, dim=dim, img_shape=imag_shape)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-2)

    # train loop
    for epoch in range(100):
        model.train()
        optimizer.zero_grad()
        noise = torch.randn(tag_ids.size(0), dim)
        pixels_pred = model(noise=noise, tag_ids=tag_ids)
        loss = ((pixels_pred - pixels) ** 2).mean()
        loss.backward()
        optimizer.step()
        print("epoch {}: loss {}".format(epoch, loss.item()))

    # evaluate
    model.eval()
    torch.manual_seed(0)
    noise = torch.randn(tag_ids.size(0), dim)
    pixels_pred = model(noise=noise, tag_ids=tag_ids).clamp(0, 1)
    loss = ((pixels_pred - pixels) ** 2).mean(axis=(1, 2, 3))
    print("Final loss:")
    for i in range(tag_ids.size(0)):
        print("   {}: {:.5f}".format(i, loss[i].item()))
    print("mean: {:.5f}".format(loss.mean().item()))
    print(" max: {:.5f}".format(loss.max().item()))

    # save model
    torch.save(model.state_dict(), "checkpoint/model.pt")

if __name__ == "__main__":
    train()


