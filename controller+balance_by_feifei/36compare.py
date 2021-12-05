# _*_ coding:utf-8 _*_
'''
比较diff文件
'''

import os
import ujson
import datetime
starttime = datetime.datetime.now()

workdir = "/Users/tang/Desktop/TokenScope"
diff_path = workdir + r'/balance_map/diff/'
#result
compare_path = workdir + r'/results/'
# diff_path = r'E:\BC\WWW\security\data\result_temp\diff\\'
# compare_path = r'E:\BC\WWW\security\data\result_temp\compare\\'
diff_path = r'F:\www-expand\etoken-diff\\'
#compare_path = r'F:\www-expand\etoken-compare\\'
#method_path = r'F:\www-expand\etoken-meth\\'
#读取method数据
Method = {}
midfiles = os.listdir(method_path)
MID = {}
for key in midfiles:
    MID[key] = 0

# for midfile in midfiles:
#     with open(method_path+midfile, 'r') as f0:
#         token = midfile
#         for line in f0:
#             b = line.strip('\n').split('#')
#             txhash = b[0].split('!')[0]
#             conlist = eval(b[1])
#             if token not in Method:
#                 Method[token] = {}
#             if txhash not in Method[token]:
#                 Method[token][txhash] = {}
#             for key in conlist:
#                 kaddr = key[0]
#                 kvalue = key[1]
#                 if kaddr not in Method[token][txhash]:
#                     Method[token][txhash][kaddr] = 0
#                 Method[token][txhash][kaddr] += kvalue



#不一致比较函数;0有三种情况，没有0，一个0，两个0
def dealflag(mapdic, eventdic, methoddic):
    if mapdic == eventdic == methoddic:#全部相同
        return (2, 2, 2)
    elif mapdic == eventdic:#不是全相等，至少两个相同：1.相同的是空的 2.相同的不是空的：①不同的是空的②不同的不是空的
        if mapdic == {}:
            return (0, 0, 1)
        if methoddic:
            return (2, 2, -1)
        else:
            return (2, 2, 0)
    elif mapdic == methoddic:
        if mapdic == {}:
            return (0, 1, 0)
        if eventdic:
            return (2, -1, 2)
        else:
            return (2, 0, 2)
    elif eventdic == methoddic:
        if eventdic == {}:
            return (1, 0, 0)
        if mapdic:
            return (-1, 2, 2)
        else:
            return (0, 2, 2)
    else:#三个都不相同，考虑有一个为0，其他两个不同
        if not mapdic:#mapdic为空
            return (0, -1, -1)
        elif not eventdic:
            return (-1, 0, -1)
        elif not methoddic:
            return (-1, -1, 0)
        else:
            return (-1, -1, -1)

# def dealdic(dicname):
#     newdic = {}
#     for tpkey in dicname:
#         addr = tpkey[0]
#         value = tpkey[1]
#         if addr not in newdic:
#             newdic[addr] = 0
#         newdic[addr] += value
#     return newdic

address0 = '0000000000000000000000000000000000000000000000000000000000000000'
files1 = os.listdir(diff_path)
for file1 in files1:
    if file1 in MID:
        with open(method_path+file1, 'r') as f0:
            TMD = {}
            token = file1
            for line in f0:
                if line in TMD:
                    continue
                TMD[line] = 0
                b = line.strip('\n').split('#')
                txhash = b[0].split('!')[0]
                conlist = eval(b[1])
                if token not in Method:
                    Method[token] = {}
                if txhash not in Method[token]:
                    Method[token][txhash] = {}
                for key in conlist:
                    kaddr = key[0]
                    kvalue = key[1]
                    if kaddr not in Method[token][txhash]:
                        Method[token][txhash][kaddr] = 0
                    Method[token][txhash][kaddr] += kvalue

for file1 in files1:
    with open(diff_path+file1, 'r') as f1:
        Compare = {}
        for line1 in f1:
            a = line1.strip('\n').split('#')
            txhash = a[0]
            eventdic = {}
            mapdic = {}
            methoddic = {}
            doubledic = eval(a[1])

            if 'event' in doubledic:
                eventdic = doubledic['event']
            if 'map' in doubledic:
                mapdic = doubledic['map']


            #留一个method入口
            if file1 in Method:
                if txhash in Method[file1]:
                    methoddic = Method[file1][txhash]

            '''
            不一致情况：子豪有一个思路，先全部加起来，然后减，试一下.这个办法没法很好的刻画，比如当map和event都是method的子集，只能看 到-1 -1 1，但是其实应该是2 2 -1
            '''
            #
            # newmap = dealdic(mapdic)
            # newevent = dealdic(eventdic)
            # newmethod = dealdic(methoddic)
            # if txhash == 'e8e93d6c809b9a7017104e57db256ed233537ef0d3a902368077a6709cfb2c07':
            #     print(eventdic)
            #     print(methoddic)

            if address0 in eventdic and address0 not in mapdic:
                del eventdic[address0]

            if mapdic or eventdic or methoddic:
                resulttp = dealflag(mapdic, eventdic, methoddic)
            else:
                print('error dic')
                continue
            if resulttp == None:
                print('error none')
                continue
            Compare[txhash] = resulttp

    keylist = list(Compare.keys())
    for key in keylist:
        if Compare[key] == (2, 2, 0) or Compare[key] == (2, 2, 2):
            del Compare[key]

    if len(Compare) != 0:
        with open(compare_path+file1, 'w') as f2:
            for tx in Compare:
                f2.write(str(tx)+'#'+str(Compare[tx])+'\n')


