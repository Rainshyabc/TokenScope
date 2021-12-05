# _*_ coding:utf-8 _*_
import os

# #locpath
findmap_path = 'F:/www/other100/FirstRound/findmap/'
findmapresult_path = 'F:/www/other100/FirstRound/findmapresult/'

#服务器路径
# findmap_path = './findmap/'
# findmapresult_path = './findmapresult/'#result

#这里也需要改，需要叠加所有文件里面的次数才能做比较，不能单个文件比较
RESULT = {}
wcount = 0
files1 = os.listdir(findmap_path)
for file1 in files1:
    with open(findmap_path+file1, 'r') as f1:
        for line1 in f1:
            a = line1.strip('\n').split('#')
            contract = a[0]
            mapdic = eval(a[1])
            if contract not in RESULT:
                RESULT[contract] = {}
            for key in mapdic:
                if key not in RESULT[contract]:
                    RESULT[contract][key] = mapdic[key]
                else:
                    RESULT[contract][key] += mapdic[key]

REALResult = {}
for sc in RESULT:
    scdic = RESULT[sc]
    index = 0
    maxnum = 0
    for idx in scdic:
        num = scdic[idx]
        if num > maxnum:
            maxnum = num
            index = idx
    REALResult[sc] = index

wcount += 1
wname = 'mapresult'+str(wcount)
with open(findmapresult_path+wname, 'w') as f2:
    for sc in REALResult:
        f2.write(str(sc)+'#'+str(REALResult[sc])+'\n')

