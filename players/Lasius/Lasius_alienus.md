# 猜数字

题解作者:Lasius

本人解法较为特别，如下。

## 题解

通过对题目的分析，可以意识到通过暴力破解的手段是足够低效的，对页面检查，发现可以通过删去disabled属性以提交空的输入内容。

首先清空输入框，然后打开检查。

![清空输入框](assets/1.png)

此时提交被禁用，发现按钮元素被添加disabled属性，将其删除。

![删除属性](assets/2.png)

此时点击提交，获得flag。

![flag](assets/3.png)

Powered by *Lasius alienus*

**qigaolasius@sina.com**
