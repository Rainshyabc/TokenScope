# Tokenscope
## 整体描述
序号31-36的py程序，是做controller这个mapping结构的不一致识别，具体过程如下：

1.从trace找到controller这样子的结构，31controller.py的功能是识别mapping，然后结果存入findmap文件； 

2.然后根据这个结构把mapping解析出来，再找到mapping，32deal_findmap.py的功能就是处理mapping；

3.再去datalog里面提取出mapping对应的trace，event，从而拿到交易下每个合约的event跟mapping的一个对应。33analy_control.py的功能是分析拿到的mapping文件；

4.最后是识别不一致，将mapping、event、method拿来比较不一致，即35-36两个py程序的工作。
## 注意
1.两个34是跑不同的数据，可以先不管
2.共四个结构：etoken、controller、普通的、还有另外一个 
3.method：交易调用合约时产生的数据（inputdata解析可得到，目前这个文件已经丢失了，可自行加上再跑36那个程序）
4.程序中的白名单暂时缺失，正式实验时需要补上
5.etoken的不一致检测过程是序号21-24的程序
