# HMM+Vetebi算法实现词性标注 python实现


　　隐马尔可夫模型（Hidden Markov Model，HMM）是统计模型，它用来描述一个含有隐含未知参数的马尔可夫过程。其难点是从可观察的参数中确定该过程的隐含参数。然后利用这些参数来作进一步的分析，例如模式识别。
　　在正常的马尔可夫模型中，状态对于观察者来说是直接可见的。这样状态的转换概率便是全部的参数。而在隐马尔可夫模型中,状态并不是直接可见的，但受状态影响的某些变量则是可见的。每一个状态在可能输出的符号上都有一概率分布。因此输出符号的序列能够透露出状态序列的一些信息。


## 马尔科夫模型 （Markov Model，HMM）
　　在考虑隐马尔科夫模型之前，我们首先要了解马尔可夫模型。马尔可夫模型描述了一类重要的随机过程，这个随机过程是随时间而随机变化的过程。我们常会考虑一个并不互相独立的随机变量组成的序列，序列中每个变量的值依赖于它前面的元素。简单来说：
　　![马尔科夫公式][1]
　　**即在特定条件下，系统在时间t的状态只与其在时间t-1的状态相关该随机过程称为一阶马尔可夫过程。**

## 隐马尔科夫模型（Hidden Markov Model，HMM）
　　如果知道某个事件的观察序列，是可以使用一个马尔可夫模型来计算；但是，有时候有些事件是不可以直接观测到的。例如，本篇博文要讲的词性标注这个例子：
　　字串(可观察序列)：　结合　　/　　成　　/　　分子　　/　　时
　　字的词性(隐序列)：　vn,v　/ 　v,nr,q,a,an,j　/　 n　/ 　Ng,nr,Dg　/
　　**HMM就是估算隐藏于表面事件背后的事件的概率。**
　　![HMM公式][2]

### 转移概率矩阵
　　转移概率指的是估计的事件的序列之间的概率关系，上诉例子中，我们所需要的转移概率为P(v|vn)p(v|v)...P(v|n)表示前一个词的词性是名词，则这个词为动词的概率。通过训练集的统计我们可以统计得出转移概率矩阵。即词性转移矩阵：

|  |v|n|s|
|:-:|:-:|:-:|:-:|
|ｖ|0.5|0.375|0.125|
|ｎ|0.25|0.125|0.625|
|ｓ|0.25|0.375|0.375|
　　
### 发射概率矩阵
　　发射概率指的是，隐藏序列和可观察序列之间的概率关系，上述例子中，我们需要的发射概率为P(结合｜v)...表示“结合”这个词为动词的概率。通过训练集的统计，我们同样也能够得出发射概率矩阵：

|  |v|n|s|
|:-:|:-:|:-:|:-:|
|结合|0.5|0.375|0.125|
|成|0.25|0.125|0.625|
|分子|0.25|0.375|0.375|
|时|0.25|0.375|0.375|

*ps 上面矩阵的数据都是乱写的*

### 计算观测序列的概率
　　有了转移矩阵和概率矩阵，我们终于可以来预测句子中每个词的词性。最直接易懂的方法便是穷举法，我们通过求每个词每个词性每种情况的概率，取最大的概率作为我们预测的词性标注。
　　例如上述例子：
　　**字串**：　结合　　/　　成　　/　　分子　　/　　时
　　**字的词性**：　vn,v　/ 　v,nr,q,a,an,j　/　 n　/ 　Ng,nr,Dg　/
　　第一种可能的词性序列是：vn,v,n,Ng
　　即:
　　P(结合,成,分子,时,vn,v,n,Ng)
　=p(结合|vn)×p(成|v)×p(分子|n)×p(时|Ng)×p(vn|start)×p(v|vn)×p(n|v)×p(Ng|n)
　
## Vetebi算法
　　如果直接使用上述的穷举法去寻找最优的概率，毋庸置疑该算法的复杂度是相当复杂的，例如上述例子仅有４个词却总共有36种情况需要考虑，也就是说我们需要分别计算36种情况的概率，然后取最大值作为我们的预测结果。那么我们有没有什么可以简化的方法吗？
　　因此在算法优化上，我们可以引用维特比算法(Vetebi)。维特比算法是现代数字通信中使用最频繁的算法，同时也是很多自然语言处理的解码算法。
　　算法描述：依据最后一个时刻中概率最高的状态，逆向通过找其路径中的上一个最大部分最优路径，从而找到整个最优路径。
　　![部分最优路径][3]
　　vt(j)是所有序列中在t时刻以状态j终止的最大概率,所对应的路径为部分最优路径。

**实例**
　　还是以“结合　成　分子　时”为例子，在计算概率的途中，我们可以理解为不断寻找最优解的过程。
　　我们可以首先考虑“结合 成”这2个词的词性计算词性概率，对于“成”的6个词性分别都有一个最大的概率和对应的前置词性如图所示：
　　![Vetebi_1][4]
　　接着考虑“分子”的词性为n，它的最优前置词性为an，如图所示：
　　![Vetebi_2][5]
　　最后考虑“时”的词性Ng,nr,Dg，分别计算得最后的概率为0.1，0.2，0.3；如图所示：
　　![Vetebi_3][6]
　　取最大概率Dg为0.3，从后往前将全局最优路径导出，如图所示：
　　![Vetebi_4][7]
　　最后我们可以得出最终结果: 结合/v; 成/an; 分子/n; 时/Dg
　　
### python代码实现
核心代码
```python
def hmm(self, sentence_list):
    """
    :param sentence_list: 已分好词的句子列表
    :return: 对应每个词的词性列表
    """
    sentence_list = list(sentence_list)
    sentence_len = sentence_list.__len__()  # 句子长度
    cixin_len = self.cixin_list.__len__()  # 词性个数
    # 概率分布表 .[i, j, 0]表示第i个词为第j个词性的最优概率;.[i, j, 1]表示该最优概率的前一个词的词性索引,若为-1表示该词为第一个词无前词
    pro_table = np.zeros((sentence_len, cixin_len, 2))
    try:
        pro_table[0, :, 0] = self.emitter_pro_matrix[self.vocab_map[sentence_list[0]]]
        pro_table[0, :, 1] = -1
        for i in range(sentence_len)[1:]:
            for j in range(cixin_len):
                if self.emitter_pro_matrix[self.vocab_map[sentence_list[i]], j] == 0:
                    continue
                pre_cixin_pro = pro_table[i-1, :, 0]
                pre_cixin_pro *= self.trans_pro_matrix[j]
                pre_cixin_pro *= self.emitter_pro_matrix[self.vocab_map[sentence_list[i]], j]
                pro_table[i, j, 0] = np.max(pre_cixin_pro)
                pro_table[i, j, 1] = np.where(pre_cixin_pro == np.max(pre_cixin_pro))[0][0]
        result_cixin_map = []
        sy = int(np.where(pro_table[-1, :, 0] == np.max(pro_table[-1, :, 0]))[0][0])
        t = -1
    except KeyError:
        return "无法正常运行 有词语不存在词库之中"
    while sy != -1:
        result_cixin_map.append(sy)
        sy = int(pro_table[t, sy, 1])
        t -= 1
    result_cixin = []

    for s in result_cixin_map[::-1]:
        result_cixin.append(self.cixin_list[s])
    return result_cixin
```


完整代码及数据[下载][8]


　　
　　
　　
　　


  [1]: http://oevwfwaro.bkt.clouddn.com/%E9%A9%AC%E5%B0%94%E5%8F%AF%E5%A4%AB%E5%85%AC%E5%BC%8F.png
  [2]: http://oevwfwaro.bkt.clouddn.com/HMM%E5%85%AC%E5%BC%8F.png
  [3]: http://oevwfwaro.bkt.clouddn.com/%E9%83%A8%E5%88%86%E6%9C%80%E4%BC%98%E8%B7%AF%E5%BE%84.png
  [4]: http://oevwfwaro.bkt.clouddn.com/vetebi_1.png
  [5]: http://oevwfwaro.bkt.clouddn.com/Vetebi_2.jpg
  [6]: http://oevwfwaro.bkt.clouddn.com/Vetebi_3.jpg
  [7]: http://oevwfwaro.bkt.clouddn.com/Vetebi_4.jpg
  [8]: https://github.com/Hareric/Natural-Language-Processing/tree/master/HMM
