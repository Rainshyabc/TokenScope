# _*_ coding:utf-8 _*_
'''
试图处理不一致
现在的问题是，这个不一致数据要怎么处理=-=
分成两种，一种是normal的，一种是controller的，normal的还是给图图处理
我来处理controller，关键是怎么记录？仅仅是两者对比没有问题，但是要和method扯上关系。我想想，method调用的是标准函数，标准函数的出发点是event，所以我用event记
Diff = {token:{txhash:{event,map}}}
'''

import os
import ujson
import datetime
starttime = datetime.datetime.now()

workdir = "/Users/tang/Desktop/TokenScope"
analysis_path = workdir + r'/balance_map/analysis/'
indexresult_path = workdir + r'/balance_map/indexresult/'

#result
diff_path = workdir + r'/balance_map/diff/'
remove_path = workdir + r'balance_map/false_report/'

# analysis_path = r'E:\BC\WWW\security\data\result_temp\analysis\\'
#analysis_path = r'E:\BC\WWW\security\data\服务器正式数据下载\analy\analysis140\\'
# diff_path = r'E:\BC\WWW\security\data\服务器正式数据下载\diff\\'
# indexresult_path = r'E:\BC\WWW\security\data\服务器正式数据下载\indexresult\\'
# remove_path = r'E:\BC\WWW\security\data\误报\\'

Diff = {}
Contrl_Map = {}
Contrl_Event = {}
with open(indexresult_path+'mapevent', 'r') as f02:
    for line02 in f02:
        a02 = line02.strip('\n').split('#')
        mapsc = a02[0]
        eventdic = eval(a02[1])
        Contrl_Map[mapsc] = eventdic
with open(indexresult_path+'eventmap', 'r') as f03:
    for line03 in f03:
        a03 = line03.strip('\n').split('#')
        eventsc = a03[0]
        mapdic = eval(a03[1])
        Contrl_Event[eventsc] = mapdic

Remove = {}
###################### START #############################
# files2 = os.listdir(remove_path)
# for file2 in files2:
#     with open(remove_path+file2, 'r') as frm:
#         for line in frm:
#             token = line.strip('\n').lower()
#             Remove[token] = 0
########################### END ############################            
#无用，拿PRG时间戳的
# TX = {}
# prt_path = r'E:\BC\WWW\pic\prg_timestamp.txt'
# with open(prt_path, 'r') as f233:
#     for line in f233:
#         tx = line.split('!')[0]
#         TX[tx] = 0


def record(filename):
    global Diff
    global Contrl_Map
    global Remove
    with open(analysis_path+filename, 'r') as f1:
        for line1 in f1:
            a = line1.strip('\n').split('#')
            anadic = eval(a[1])
            if 'controller' not in anadic:
                continue
            txhash = anadic['log_txhash']
            txtime = anadic['log_time']
            controldic = anadic['controller']
            TempMap = {}
            eventsc = 'none'

            rmflag = 0
            for addr in controldic:
                if addr in Remove:
                    rmflag = 1
                    break
                else:
                    if addr in Contrl_Map:
                        for key in Contrl_Map[addr]:
                            if key in Remove:
                                rmflag = 1
                                break
                    if addr in Contrl_Event:
                        for key in Contrl_Event[addr]:
                            if key in Remove:
                                rmflag = 1
                                break
            if rmflag == 1:
                continue
            #
            if txhash == 'db2fac0489ddd3bc4428aebdb150db1e2ff6f0c988f28aa457a25c37e3fc7596':
                print(controldic)
                print(filename)


            for addr in controldic:
                for keytype in controldic[addr]:
                    if keytype == 'event':
                        eventsc = addr
                        if eventsc not in Diff:
                            Diff[eventsc] = {}
                        if txhash not in Diff[eventsc]:
                            Diff[eventsc][txhash] = {}
                        if keytype not in Diff[eventsc][txhash]:
                            Diff[eventsc][txhash][keytype] = {}

                        for layer in controldic[addr][keytype]:
                            addrlist = controldic[addr][keytype][layer]
                            for addrtp in addrlist:
                                addr1 = addrtp[0]
                                value = addrtp[1]
                                if addr1 not in Diff[eventsc][txhash][keytype]:
                                    Diff[eventsc][txhash][keytype][addr1] = 0
                                Diff[eventsc][txhash][keytype][addr1] += value

                    elif keytype == 'map':
                        mapsc = addr
                        if mapsc not in TempMap:
                            TempMap[mapsc] = {}
                        if txhash not in TempMap[mapsc]:
                            TempMap[mapsc][txhash] = {}
                        if keytype not in TempMap[mapsc][txhash]:
                            TempMap[mapsc][txhash][keytype] = {}
                        for layer in controldic[addr][keytype]:
                            addrlist = controldic[addr][keytype][layer]
                            for addrtp in addrlist:
                                addr2 = addrtp[0]
                                value = addrtp[1]
                                if addr2 not in TempMap[mapsc][txhash][keytype]:
                                    TempMap[mapsc][txhash][keytype][addr2] = 0
                                TempMap[mapsc][txhash][keytype][addr2] += value
            #三种情况：有event有map，有event没有map。没有event，有map。啥也没有就不会记录的。
            if eventsc != 'none':
                if TempMap:
                    Diff[eventsc][txhash].update(TempMap[mapsc][txhash])
            else:
                eventdic = Contrl_Map[mapsc]
                for key in eventdic:
                    if len(eventdic) == 1:
                        eventsc = key
                        if eventsc not in Diff:
                            Diff[eventsc] = {}
                        Diff[eventsc].update(TempMap[mapsc])
                    else:
                        eventsc = 'both'+str(mapsc)
                        if eventsc not in Diff:
                            Diff[eventsc] = {}
                        Diff[eventsc].update(TempMap[mapsc])


files1 = os.listdir(analysis_path)
count = 0
for file1 in files1:
    count += 1
    if count % 10 == 0:
        print(count)
        endtime = datetime.datetime.now()
        print(endtime - starttime)
    record(file1)
#
for sc in Diff:
    print(sc[0])
    print(sc[1])
    # filename = diff_path
    # for key in eval(sc[0]).keys():
    #     filename += key
    # filename += '_' + sc[1]
    with open(diff_path+str(sc), 'a') as f2:
        for tx in Diff[sc]:
            f2.write(str(tx)+'#'+str(Diff[sc][tx])+'\n')


