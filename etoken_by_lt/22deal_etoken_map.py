# _*_ coding:utf-8 _*_
'''
处理balance mapping，选取出现次数最多的那个
'''
import os
# #loc
# balance_path = r'E:\BC\WWW\security\data\result_temp\findmap\\'
balance_path = r'F:\www-expand\etoken-test\findmap\\'
indexresult_path = r'F:\www-expand\etoken-test\indexresult\\'
test_path = r"F:\www\误报\etoken"


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
    map_index = baddr[2]
    symbol = baddr[3]
    bindexdic = BALANCE[baddr]
    true_index = max(bindexdic, key=bindexdic.get)
    if mapsc in MapIndex and true_index != MapIndex[mapsc]:
        print('dup index', mapsc)
    if mapsc not in MapIndex:
        MapIndex[mapsc] = {}
    MapIndex[mapsc][(true_index,map_index,symbol)] = 0
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


with open(indexresult_path+'etoken', 'w') as f6:
    for key in Controller:
        f6.write(str(key)+'\n')

test_dict = {}
with open(test_path,'r')as f:
    for line in f :
        line = line.strip('\n')
        test_dict[line] = 0

count = 0
for key in EventMap:
    if key not in test_dict:
        print(key)
    else:
        count+=1
print(count)

for key in MapEvent:
    if key in EventMap:
        print(key)


