# 你先别急

题解作者：[volltin](https://github.com/volltin)

出题人、验题人、文案设计等：见 [Hackergame 2022 幕后工作人员](../../credits.pdf)。

## 题目描述

- 题目分类：web

- 题目分值：300

2032 年（仍然是人类统治的时代）的某一天，小 K 进入元宇宙抢购自己最喜爱的歌姬的限量版虚拟签名，但是又一次因为验证码输入过慢而被别人抢光了。

「急急急急，急死我了，为什么要对我这种一看就是人类的用户进行这么复杂的验证呢？」小 K 一边急，一边想这个问题。

如果能根据用户的特征来判断用户的风险等级，然后决定验证码的复杂度是不是就能缓解这个问题呢？

于是小 K 实现了自适应难度验证码，但由于小 K 还要急着参加下一场虚拟签名的抢购，所以只用数据库实现了一个简单的 demo，而这个数据库中还不小心存放了一些重要信息，你能得到其中的秘密吗？

[验证码生成逻辑代码下载](files/captcha_gen.py)

## 题解

tl;dr: 这个题是一道 SQLite 注入题，但是返回的信息比较少，几乎没有报错，需要通过观察返回的验证码来得到查询结果。

题解见 [nxbj.ipynb](exp/nxbj.ipynb)。

## 附注

@taoky: 这里补充一个用深度学习的解法。我改的时候在题目给了验证码生成脚本，也是为了能让大家本地快速生成数据来训练区分，而不是自己手动一个一个判断。同时，验证码的字符集里面删除了一些容易和数字混淆的字母，也给训练降低了难度。

训练脚本是直接从 PyTorch 的 "Training a Classifier" 这个 tutorial 修改的，`net.py` 代码：

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.datasets import ImageFolder
import torch.optim as optim
import torchvision.transforms as transforms


transform = transforms.Compose(
        [transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(14784, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 2)

    def forward(self, x):
        # print(x.shape)
        x = self.pool(F.relu(self.conv1(x)))
        # print(x.shape)
        x = self.pool(F.relu(self.conv2(x)))
        # print(x.shape)
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        # print(x.shape)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


if __name__ == "__main__":
    net = Net()
    net.train()

    # path/to/data/simple/*.png: label "simple" images
    # path/to/data/op/*.png: label "op" images
    dataset = ImageFolder('path/to/data', transform=transform)

    splitted_dataset = torch.utils.data.random_split(dataset, [1600, 400])
    trainset = splitted_dataset[0]
    print(trainset)
    trainset.dataset.transforms = transform
    testset = splitted_dataset[1]

    trainloader = torch.utils.data.DataLoader(trainset, batch_size=4,
                                            shuffle=True, num_workers=2)
    testloader = torch.utils.data.DataLoader(testset, batch_size=4,
                                            shuffle=False, num_workers=2)

    criterion = nn.CrossEntropyLoss()
    # optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
    optimizer = optim.Adam(net.parameters())

    for epoch in range(15):  # loop over the dataset multiple times

        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % 20 == 19:    # print every 20 mini-batches
                print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 20:.3f}')
                running_loss = 0.0

    print('Finished Training')
    torch.save(net.state_dict(), 'model.pth')

    correct = 0
    total = 0
    net.eval()
    # since we're not training, we don't need to calculate the gradients for our outputs
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            # calculate outputs by running images through the network
            outputs = net(images)
            # the class with the highest energy is what we choose as prediction
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(correct, total)

    # prepare to count predictions for each class
    correct_pred = {classname: 0 for classname in dataset.classes}
    total_pred = {classname: 0 for classname in dataset.classes}

    # again no gradients needed
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            outputs = net(images)
            _, predictions = torch.max(outputs, 1)
            # collect the correct predictions for each class
            for label, prediction in zip(labels, predictions):
                if label == prediction:
                    correct_pred[dataset.classes[label]] += 1
                total_pred[dataset.classes[label]] += 1


    # print accuracy for each class
    for classname, correct_count in correct_pred.items():
        accuracy = 100 * float(correct_count) / total_pred[classname]
        print(f'Accuracy for class: {classname:5s} is {accuracy:.1f} %')
```

其中最主要的修改，就是拿 Adam optimizer（而不是 SGD）来训练，这样可以避免调 lr（tutorial 的 lr 设置直接用过来效果不好）。以及 `fc1` 的线性层大小也有调整，以配合验证码的实际大小。这个分类模型分类 Simple-1 和 OP-9，每个 label 一千张图片，合计两千张图片选择 400 张作为测试集。因为这个模型实在很简单（当然比二次元那个还是大不少），即使是用 CPU，也能轻松训练。

训练有随机性，在写这段题解的时候我跑了一些，等待一段时间后，训练 15 个 epoch 在测试集上效果大致如下：

```
Finished Training
361 400
Accuracy for class: op    is 87.0 %
Accuracy for class: simple is 93.8 %
```

准确率大概还算能接受。实际使用的时候：

```python
from net import Net, transform
from PIL import Image
from base64 import b64decode
from io import BytesIO
import torch

network = Net()
network.load_state_dict(torch.load("model.pth"))
network.eval()

def get_complex_metric(b64):
    image = Image.open(BytesIO(b64decode(b64)))
    with torch.no_grad():
        data = transform(image).unsqueeze(0)
        outputs = network(data)
        probs = torch.nn.functional.softmax(outputs, dim=1)
        _, predicted = torch.max(outputs.data, 1)
    return predicted.item(), probs[0][1]
```

就能看到对于特定的验证码图片的输出了。既然有了相对可靠的验证码分类器，那么接下来就好做了。

> 所以，真正的机器学习题：
> 
> 二次元神经网络 ❌
> 
> 你先别急 ✅
