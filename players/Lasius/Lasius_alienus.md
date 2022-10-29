# 猜数字

题解作者:Lasius

本人解法较为特别，如下。

## 题解

通过对题目的分析，可以意识到通过暴力破解的手段是足够低效的，对页面检查，发现可以更改输入框的输入类型。

找到input type元素并将其修改为"float"，

![修改的项目](assets/1.png)

此时输入框内可以被键入文本(此处以键入"flag"为例)。

![输入](assets/2.png)

此时提交被禁用，发现按钮元素被添加disabled，将其删除。

![删除](assets/3.png)

此时提交可以被点击，获得flag。

![flag](assets/4.png)

Powered by *Lasius alienus*

**qigaolasius@sina.com**