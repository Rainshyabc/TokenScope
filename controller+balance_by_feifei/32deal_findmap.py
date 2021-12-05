# _*_ coding:utf-8 _*_
'''
处理balance mapping，选取出现次数最多的那个
'''
import os
# #loc
workdir = '/Users/tang/Desktop/TokenScope'
balance_path = workdir + '/balance_map/findmap/'
indexresult_path = workdir + r'/balance_map/indexresult/'
# balance_path = r'E:\BC\WWW\security\data\result_temp\findmap\\'
# balance_path = r'F:\www-expand\controller-test\findmap\\'
# indexresult_path = r'F:\www-expand\controller-test\indexresult\\'
# #服务器路径
# balance_path = '../findmapall/'
# indexresult_path = '../indexresult/'

files1 = os.listdir(balance_path)
BALANCE = {}
for file1 in files1:
    print(file1)
    with open(balance_path+file1, 'r') as f1:
        for line1 in f1:
            a = line1.strip('\n').split('#')
            addrtp = eval(a[0])
            indexdic = eval(a[1])
            if addrtp not in BALANCE:
                BALANCE[addrtp] = indexdic
            else:#新增进去
                for key in indexdic:
                    if key not in BALANCE[addrtp]:
                        BALANCE[addrtp][key] = 0
                    BALANCE[addrtp][key] += indexdic[key]
'''
认为一个event可以对应多个map，因为ledger是可以修改的。
因此我们需要建立两个字典;A = {mapcontract:index} B:{eventsc:{mapsc:0, mapsc2:0}}
这里先改成event和map一对一。
'''

MapIndex = {}
MapEvent = {}
EventMap = {}
Controller = {}
NOTK = {}

for baddr in BALANCE:
    mapsc = baddr[0]
    eventsc = baddr[1]
    # map_index = baddr[2]
    # symbol = baddr[3]
    bindexdic = BALANCE[baddr]
    true_index = max(bindexdic, key=bindexdic.get)
    if mapsc in MapIndex and true_index != MapIndex[mapsc]:
        print('dup index', mapsc)
    MapIndex[mapsc] = true_index
    if eventsc == 'none':
        NOTK[mapsc] = 0
        continue
    #能走到这说明是controller
    if mapsc not in MapEvent:
        MapEvent[mapsc] = {}
    MapEvent[mapsc][eventsc] = 0

    if eventsc not in EventMap:
        EventMap[eventsc] = {}
    EventMap[eventsc][mapsc] = 0

    Controller[mapsc] = 0
    Controller[eventsc] = 0


with open(indexresult_path+'mapindex', 'w') as f2:
    for key in MapIndex:
        f2.write(str(key)+'#'+str(MapIndex[key])+'\n')

with open(indexresult_path+'mapevent', 'w') as f3:
    for key in MapEvent:
        f3.write(str(key)+'#'+str(MapEvent[key])+'\n')

with open(indexresult_path+'eventmap', 'w') as f4:
    for key in EventMap:
        f4.write(str(key)+'#'+str(EventMap[key])+'\n')

with open(indexresult_path+'notk', 'w') as f5:
    for key in NOTK:
        f5.write(str(key)+'\n')

with open(indexresult_path+'control', 'w') as f6:
    for key in Controller:
        f6.write(str(key)+'\n')
