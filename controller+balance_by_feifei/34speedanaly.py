# _*_ coding:utf-8 _*_
'''
解析trace，这种可能包括普通的，可能包括control
1.最新发现是，token和ledger都可能作为主调函数，这样的话，就不能按顺序往下找了。而是只能关联查找
2.如果有多对多的情况，过于繁琐，可以先按照一对一来处理，如果明天跑出来结果发现有多对多，再问子豪
做一个controller的名单，如果遇到不是controller的，就正常记录这一层。如果遇到了是controller的。就单独记在controller的里面
{count : {logtxhash, logblock, logtime, normal:{lay1{balance:, event, log_sc},controller:{(map,event):{{map{lay1:(address,value)}, event:{lay3:(address,value)} }}}}}
'''
import os
import ujson
import datetime
starttime = datetime.datetime.now()

#loc path
wefound_path = r"E:\BC\WWW\security\data\BalanceMapping_tokenlist.txt"#55332个名单，要跳过他
# order_file_path = ''
# datalog_path = r'E:\BC\WWW\security\data\testfile\\'
# order_file_path = 'F:/BC/WWW/data/ordered_100.txt'
# datalog_path = 'F:/BC/WWW/data/100_data/'
order_file_path = 'F:/BC/WWW/data/other-100/ordered_filename_time_blocknumber_100.txt'
datalog_path = 'F:/BC/WWW/data/other-100/100_data_1/'

indexresult_path = r'E:\BC\WWW\security\data\result_temp\indexresult\\'
txcall_path = r'E:\BC\WWW\security\data\result_temp\txcall\\'
#result_path
analysis_path = r'E:\BC\WWW\security\data\result_temp\analysis\\'
error_path = r''

# #服务器路径-zihao
# wefound_path = '../BalanceMapping_tokenlist.txt'
# order_file_path = '/media/HardDisk4T/lt/datasetmove'
# datalog_path = '/media/HardDisk4T/movedatalog/'
# txcall_path = '../txcall/'
# error_path ='../error/round2/'
# indexresult_path = '../indexresult/'
# analysis_path = '../analysis/'
#
# #服务器路径-chenting
# wefound_path = '../BalanceMapping_tokenlist.txt'
# order_file_path = '/media/yulele/HardDisk10TB/icse/core/lt/formal_ordered_filename_time_blocknumber.txt'
# datalog_path = '/media/yulele/HardDisk10TB/www/syncdata/syncdatalog/'
# txcall_path = '../txcall/'
# error_path ='../error/round2/'
# indexresult_path = '../indexresult/'
# analysis_path = '../analysis/'

#定义全局变量
#建立Transfer_event的字典
transfer_hash = {'2c4d9d1041355b152e80b28195d8cd57a1363203c2b1a39c0559f0e757747d5c': 'uint8', '89896edbd223c9360ce42ddfed7522a2bffb20c056e4c42d42370cb493b65676': 'uint16', '4c3f23e06500a14887485511327c0d579fbccac302d5839c043bcc62bf867793': 'uint24', '0daf680c3f528a8760b5142fe1f6f80d5f4ea18bb76f347a7a44a2d565c2b7dc': 'uint32', 'cdabd7cd7a44bd50521a39c666b076577c82465c3615f66391d096cc719c6ac0': 'uint40', 'e18706cb56ac477fbc72c6acbbd512822f259c1f09006247dbae41d881bc3e17': 'uint48', 'f0cd1a5c0ee7db84a3a9327b544161b199d1a1088d6dd1c99d42646432eaf9fb': 'uint56', '831ac82b07fb396dafef0077cea6e002235d88e63f35cbd5df2c065107f1e74a': 'uint64', 'bff91d4903077cc645099227f3ff63fa8f7c4e51de89afbefde6b29eb549af87': 'uint72', 'a0f2d9d810b7227d93b1d65511f1321d5331a7a323e6d357130dda4aa99690a0': 'uint80', '1c232f833daad9ed1224c5770c053a18edfef5d85918dede55acc1da05ab6c8b': 'uint88', 'ba7196a4bdbfed2416fed23830b5c875c6e32d81744212e9776f7d2b02a33188': 'uint96', '18b3a374e2313c602fb9e4002182a9b948dff0294feab6f98f5e7e4334ef7e9d': 'uint104', 'b7ac3c4762d5a753158c22506d7f1a1373c52dae6059cc91115338581b05e27c': 'uint112', '91925c49b49f6ee4ac0d966d8d2e700e489f031bf933396b5b64bc584529d229': 'uint120', '27772adc63db07aae765b71eb2b533064fa781bd57457e1b138592d8198d0959': 'uint128', '46518209995f34a01926b792690bc92e5037b070563bfdacd84fafd40b513eb5': 'uint136', 'e8032327ba5bd636272f39d92559de88e80732a9d637d0b6752d51281150d4b7': 'uint144', '48c4fa90124ada7723a851f5a30fc80851bbfab1f12649e3ae71a32c627720cd': 'uint152', 'df5c409937706803ae64d124b48586638c7b50733b40fb16cff8141ffa1e0af8': 'uint160', 'd0966ead8911bd02ec5119ed64d10236cb4fd8f29c5001afb73d60689cf88b20': 'uint168', 'b18cf775c754b8fae1157af9b1f2b93496f6bf0cd582c24d7175692fcaa1cd21': 'uint176', 'fcdacb06893591fedb6582b761d2e964d37a4e7f77a844e3a05c5fbf47797c0e': 'uint184', '74c9ae5ff92efee44f316c09cbdbdebb254705f4fd59514ed2d87e1e3da93913': 'uint192', '7344fa9abcab6b3790a118567725311a6bfb30957589e825e4300bce8f3fb020': 'uint200', 'bae695334f1401f46a8c246fb4e028ccdee498d6cd47ddb5683ab940d25fbdc5': 'uint208', '3fb8d49d89b30c4ee5141c3d10e5bb70e95d5babd584e3000107d2dac22a826a': 'uint216', '354cd84171949f23d6c7393b4deca6b9670954625ffedcb35a250a15a08515ed': 'uint224', 'cf73f4a4f977af3327646216f7d3af8970de9bc70aeaf76009cec99dcf46c786': 'uint232', 'c2ac9a11e79ddfc35c6403b568c9d85957090c8416d338be90299141f1e7f425': 'uint240', 'fe28b6744e16875301806797283f9bcc1a29b15f700c0e088645e2c257eec1e5': 'uint248', 'ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef': 'uint256', 'fdb0d9db4fcfa99a69bab4019cf42ab495be117bb60275b901645c28ca3deef4': 'int8', '1306f300bdf23ef00b1fe00644eee04b9576ad8c68837bffa5158e4693ea296a': 'int16', '1315fe0300efd5bde69c874d107401124940c3cdb534666230a2436a47e6a49b': 'int24', 'b659f7922125405e40eb1a5fbfd9879f3d296b8200019be90f730b459f9f1c25': 'int32', 'b76456965aa890ee11746d3b26582281ffca539801841abe6282ab73b2c01993': 'int40', 'fd0e41a48c016debc0ec3c87cdf02ba5e2eb2db4587292c6bdcec7bda1fc3d3c': 'int48', 'bc87650eb8e9c481db3f2576aea1b4e653894d93b7f6cb6a190717a1fca3a319': 'int56', 'cef55929759435389feb62e3ad30d90911d061d3eb8f8e3ead60622531745cc1': 'int64', '19b40000025b47ecd4d2940168402cfe9317418307f848216988dc028e628214': 'int72', 'e670604a3a027fa22059b623a5b0ae38424829237d769b02282dc7d81fb06426': 'int80', '303dc7e5a79ee0ca02c3f06db0502fbfe7a964cd8fa597919e4376f6dbc1e157': 'int88', '0ed1306281e9b4c9d018e1291d83fd014895d20c95da608569e7d9a5361117aa': 'int96', 'a87ac4316a9088110eb185cf27691b5533890444b36f2712b700fe09a5e53ba7': 'int104', '2c5825beae12151d954009ae7f95e998300458d351c8fc8e6d2df9a8753d65a7': 'int112', 'e64efe620012ecf67a6a08208071cfd55ea85c641860fa711388c041c80d72f6': 'int120', '9ce147531995c591b0b50012b20f7f6d0dea75281159a58b8637542388f14626': 'int128', 'e86307cdc23d5574d14f14c07d08814d980276c4b92d6d51e6f6497a807607c8': 'int136', 'a099bc2413531106e46903e9bd7f34d43b6d124631398348d1d5f368baeb8032': 'int144', '467c5dc3035b08b8eda1206c6049fd8eb86db17119be0ca51d0de6f99bf7f548': 'int152', '8d1591cfd32ad19c215c6295623aea4eec85442fc5c4601cda6f7e0a038186ba': 'int160', '4ec3ba770fb8428f5ce8590bc4b28663359570e0193206f9364399c06e768241': 'int168', '7f02f13368f9b374a15f81ad02096044b4c26fa5127a1fa37aeed8e392bd6edd': 'int176', '6e348e9e7927772dff9da0764845053058a54199928284bfe6decb7ac09d40d7': 'int184', 'a88a4735393a2bbb1c23c083874e1d0636d3e87851b6f20a6d2115f5ea540ba0': 'int192', '96a6ed04a9960ed29f91a03141a1256a7e6204eb90c319d76a91ec4aa02bbc2f': 'int200', 'cbab2a67020e790d89db09e426191c44c8c05d9f93dc1f8cc32dda14929f40e5': 'int208', '7c11167a36b8ef38fc546598e268c0964bb2cb21377e6cb80e217bcb6ecb8c67': 'int216', 'f238e8301c28c0dac41fcc9bd2e2d659096a02384c2ffd9b1430ac584c95691e': 'int224', 'd6e7a41c23f4209ee7bed2dbe1d4774884aaf836b11d0c93a84b8eb44878dbd3': 'int232', '81031c58ed866f2ba7f5ac8c702cedc31ed6b4a08cd1d540c988018b0ca5b845': 'int240', '8695741cd0cb852f381bcfad35ffa6af9b0f4d1634247d0b2589ad84233dc590': 'int248', '8b0c34a52f9e28d78caaa7066cd047b398dae74941a208b77777420f492bd7e1': 'int256'}
address0 = '0000000000000000000000000000000000000000000000000000000000000000'

wcount_analy = 0
WeFound = {}
trace_count = 0
MapIndex = {}
Controller = {}
Contrl_Map = {}
Contrl_Event = {}
NOTK = {}
#记录结果
Analy = {}


#读取我们识别到的token
with open(wefound_path, 'r') as f0:
    for line0 in f0:
        wetoken = line0.strip('\n').lower()
        WeFound[wetoken] = 0

#读取记录的mapping
'''
1.存在一对二或者二对一的情况，要改
2.存在controller中，有的时候是本层又操作map又进行event操作的情况。
这种类型出现在eventtoken中，属于event里面有map，但是没见到说maptoken里自己有event的情况。
'''
with open(indexresult_path+'mapindex', 'r') as f01:
    for line01 in f01:
        a01 = line01.strip('\n').split('#')
        mapsc = a01[0]
        mapindex = a01[1]
        MapIndex[mapsc] = mapindex
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
with open(indexresult_path+'notk', 'r') as f04:
    for line04 in f04:
        a04 = line04.strip('\n').lower()
        NOTK[a04] = 0
with open(indexresult_path+'control', 'r') as f05:
    for line05 in f05:
        a05 = line05.strip('\n').lower()
        Controller[a05] = 0

for key in Controller:
    if key in Contrl_Map and key in Contrl_Event:
        print(key)
exit()


def analy_trace(filename, txlist):
    global transfer_hash
    global wcount_analy
    global WeFound
    global trace_count
    global MapIndex
    global Analy
    global Controller
    global Contrl_Event
    global Contrl_Map
    global NOTK
    with open(datalog_path+filename, 'r') as f2:
        for line2 in f2:
            trace_count += 1
            #还原外部交易失效标志
            break_flag = 0
            #每一笔交易维护一个栈
            txstack = ['ept']#ept表示一开始没有call也没有create。
            stack_count = 0
            LayerSC = {}#栈顶-sc
            create_addr_flag = 0 #判断是createend前还是之后的createaddr，前为0，后为1
            #记录失效层数
            Invalid_Layer = {}
            poplayer = 0
            #记录两种event和sha3和sstore
            Transevent = {}
            SHA3dic = {}
            SSTORE = {}

            #开始解析
            trace = ujson.loads(line2)
            txhash = eval(trace['LOG_txhash']).lower()#type str

            if txhash not in txlist:
                continue

            # #test
            # if txhash != 'aa3d32aa4005d48f01f91b27f0662359072c816b78d96a55f769a0801db217e7':
            #     continue

            blocknumber = eval(trace['LOG_blocknumber'])  #type str
            time = eval(trace['LOG_timestamp'])  #type str
            opinfos = list(eval(trace['LOG_opinfos']))
            for op in opinfos:
                opcode = eval(op)   #type dic
                log_type = opcode['log_type']
                #这里有个很严重的问题，就是这个txstack并不是严格的123，有可能直接13,这样一来，进行那个栈顶判断的时候，就会出错。这里为了解决这个问题，用一个变量来专门记录，刚刚pop出去的是谁
                #维护栈结构，此时内外部有了区别，同时有了error字段，需要区分。
                if log_type == 'CALL':
                    stack_count += 1
                    txstack.append(stack_count)
                    contract = opcode['to_addr'].lower()
                    LayerSC[stack_count] = contract
                    if contract in WeFound:
                        Invalid_Layer[stack_count] = 0
                if log_type == 'CALLEND':
                    poplayer = txstack[-1]
                    txstack.pop()
                if log_type == 'CALL_F' or log_type == 'CALL_R':
                    Invalid_Layer[poplayer] = 0

                if log_type == 'CREATE':
                    stack_count += 1
                    txstack.append(stack_count)
                if log_type == 'CREATEEND':
                    poplayer = txstack[-1]
                    txstack.pop()
                    create_addr_flag = 1
                '''
                三种情况下creataddr:
                1.end之前的create_addr,并且不是最外层的。这种情况下，create_flag = 0 and 至少是第二层，那么此时的txstack[-1]!=1
                2.已经是第五层了，但是刚刚pop完，栈顶为1；这种情况下，create_flag = 1 and poplayer !=0
                3.外部的createaddr，就没有creatend，那么flag就是0； create_flag = 0 ，假如只有一层，并且是create，那么poplayer = 0.如果有两层，那poplayer = 2
                
                到底哪一种是无效的呢？
                end之前的createaddr:cflag = 0并且txstach[-1] !=1.假如遇到pop出的第二层，他的cflag = 1，所以还是会抓到
                那么，contract到底是哪一层的呢？
                如果cflag = 1：肯定是poplayer这一层的。因为遇到了end。
                如果cflag = 0 之前想到过，只有两种情况下为0：最外层或者是end之前。由于已经排除了end之前，那么此时就已经是最外层了。               
                '''
                if log_type == 'CREATE_ADDR':
                    layer = txstack[-1]
                    if create_addr_flag == 0 and layer != 1:#没有creatend出现，那么可能是最外层，如果是最外层，那么layer应该是1，如果不是1，那说明是creatend前面那个废物
                        continue
                    else:
                        contract = opcode['to_addr'].lower()
                        if create_addr_flag == 1:#前面有creatend，那么就会有poplayer
                            LayerSC[poplayer] = contract
                            if contract in WeFound:
                                Invalid_Layer[poplayer] = 0
                        else:#说明前面没有creatend，并且layer==1，最外层
                            LayerSC[layer] = contract
                            if layer != 1:
                                print('layererror')
                            if contract in WeFound:
                                Invalid_Layer[layer] = 0
                        create_addr_flag = 0

                if log_type == 'CREATE_F' or log_type == 'CREATE_R':#这个标志不会出现在creatend之前，因此不需要errorflag判断
                    create_addr_flag = 0
                    Invalid_Layer[poplayer] = 0

                #整条交易失败，进行下一条交易，就是下一个for line in f
                if log_type == 'OUT_E' or log_type == 'OUT_I':#这里出了问题，并不是所有的outi都存在
                    break_flag = 1
                    break

                #event解析
                if log_type == 'LOGX':
                    layer = txstack[-1]
                    if layer == 'ept':
                        continue
                    #此处无法判断该层是否失效，只能按照层数记录这个数据，然后失效的话最后清空
                    topic0 = opcode['log_topics'][0:64]
                    topic0 = topic0.lower()
                    if topic0 in transfer_hash:
                        topics = opcode['log_topics']
                        middle = topics.split('#')
                        topics1 = ''
                        for md in middle:
                            if md:
                                topics1 += md

                        data0 = eval(opcode['log_data'])
                        data1 = ''
                        for dt in data0:
                            num = hex(dt)
                            num = num[2:]
                            if len(num) < 2:
                                num = '0'+num
                            data1 += num

                        trans_log = topics1 + data1
                        trans_log = trans_log.lower()
                        if len(trans_log) != 64*4:
                            print('transfer_log_error')
                            with open(error_path+'error.txt', 'a') as f3:
                                f3.write(filename+'#'+txhash+'transfer_log_error'+'\n')
                        fromaddr = trans_log[64:128]
                        toaddr = trans_log[128:192]
                        inputdata = trans_log[192:256]
                        inputdata = int(inputdata, 16)

                        '''
                        这里进行event装箱。装箱原则：1.属于同一个token，同一层 2.属于同一个event，就是拆解出来的from和to要有联系，表明是一个event拆出来的。这个不行，因为想累计，第二条作废。
                        那就是按照层数来记录event。
                        '''

                        #进行存储,这里存的时候，按照address，value来存。区分vlue正负。event = {层数：{addr:value}}；map= {层数：{index{address:value}}}
                        if layer not in Transevent:
                            Transevent[layer] = {}
                        if fromaddr not in Transevent[layer]:
                            Transevent[layer][fromaddr] = 0
                        Transevent[layer][fromaddr] -= inputdata

                        if toaddr not in Transevent[layer]:
                            Transevent[layer][toaddr] = 0
                        Transevent[layer][toaddr] += inputdata

                #sha3+sstore。
                if log_type == 'SHA3':
                    layer = txstack[-1]
                    if layer == 'ept':
                        continue
                    keccak = opcode['log_keccak']
                    sha3_tuple = eval(opcode['log_tuple'])
                    sha3_content = ''
                    for st in sha3_tuple:
                        num2 = hex(st)
                        num2 = num2[2:]
                        if len(num2) < 2:
                            num2 = '0' + num2
                        sha3_content += num2
                    if len(sha3_content) != 128:
                        continue
                    mp_addr = sha3_content[:64]
                    mp_index = sha3_content[64:]

                    if int(mp_index, 16) > 340282366920938463463374607431768211455:#去掉双重sha3的干扰，这个数字是32个f的十进制
                        continue

                    #这里到底怎么存，需要再考虑
                    sha3tp = (layer, keccak)
                    SHA3dic[sha3tp] = (mp_addr, mp_index)

                #因为一定是先sha3,所以遇到SSTORE可以直接匹配。
                if log_type == 'SSTORE':
                    layer = txstack[-1]
                    if layer == 'ept':
                        continue
                    s_keccak = opcode['log_keccak']
                    log_prevalue = int(opcode['log_prevalue'])
                    log_value = int(opcode['log_value'])  #十进制
                    balance = log_value - log_prevalue
                    ssttp = (layer, s_keccak)
                    if ssttp in SHA3dic:
                        addrNindex = SHA3dic[ssttp]
                    else:#寻找结构体；
                        struct_flag = 0
                        for i0 in range(16):
                            new_keccak = int(s_keccak, 16)-1
                            if new_keccak <= 0:
                                break
                            s_keccak = hex(new_keccak)[2:]#这一步需要做测试.这里是针对sstore的skeccak修改，应该是减法
                            s_keccak = s_keccak.zfill(64)
                            ssttp = (layer, s_keccak)
                            if ssttp in SHA3dic:
                                addrNindex = SHA3dic[ssttp]
                                staddr = addrNindex[0]
                                stindex = addrNindex[1]+'@'+str(i0+1)
                                addrNindex = (staddr, stindex)
                                struct_flag = 1
                                break
                            else:
                                continue
                        if struct_flag == 0:#没匹配上结构体
                            continue

                    staddr = addrNindex[0]
                    stindex = addrNindex[1]

                    if layer not in SSTORE:
                        SSTORE[layer] = {}
                    if stindex not in SSTORE[layer]:
                        SSTORE[layer][stindex] = {}
                    if staddr not in SSTORE[layer][stindex]:
                        SSTORE[layer][stindex][staddr] = 0
                    SSTORE[layer][stindex][staddr] += balance

            if break_flag == 1:
                continue

            #查看本条trace是否有必要记录
            valid_flag = 0
            for key in LayerSC:
                testsc = LayerSC[key]
                if testsc in Controller or testsc in MapIndex:
                    valid_flag = 1
                    break
            if valid_flag == 0:
                continue

            #记录trace
            if trace_count in Analy:
                print('tracecount error')
            Analy[trace_count] = {}
            Analy[trace_count]['log_txhash'] = txhash
            Analy[trace_count]['log_time'] = time
            Analy[trace_count]['log_block'] = blocknumber


            '''
            开始解析
            解析数据的数据结构如下：
            {count : {logtxhash, logblock, logtime, normal:{lay1{balance:, event, log_sc},controller:{} }}}
            1.首先，这个count记录还是不记录靠什么呢？靠这些balance我们有没得识别到，因此要专门存储一个识别到的token的字典。如果这样的话，可以在后面标注是不是controller
            2.遍历每一层，如果不是controller就正常记录。如果是controller，那么就按照event先，map后的办法，记录一对。假如出现多次呢？
            说白了这个index还是针对map-contract的。因此应该是记录在mapcontract下面。这样的话，map指向index,event指向map。
            这里又有个问题，会不会出现重复的问题？就是多对多——这里要假设一个行为模式出来，而不是开脑洞
            
            首先，认为是event为主调函数，那么在event之后，紧接着第一个符合匹配mapsc的contract就认为是一对的。
            第二，认为一个event可以对应多个map，因为ledger是可以修改的。
            因此我们需要建立两个字典;A = {mapcontract:index} B:{sc:tp}
            
            上述解决了匹配问题，那么就需要解决第二个记录格式的问题。
            '''

            for ly in LayerSC:
                if ly in Invalid_Layer:
                    continue
                now_token = LayerSC[ly]
                if now_token in Controller:
                    #多一个分支：假如这个token同时是control又同时是普通token的话，就需要判断他究竟要走哪种分支。我们发现这种情况只会在eventtoken中出现，并且有自己的index
                    if now_token in Contrl_Event and now_token in NOTK:
                        if ly in SSTORE:
                            now_index = MapIndex[now_token]
                            if now_index in SSTORE[ly]:#走到这一步的时候，就已经说明触发了他自己的mapping了，找普通的行为。这里制定规则，就是假如只有event，那就认为属于controller。
                                if 'normal' not in Analy[trace_count]:
                                    Analy[trace_count]['normal'] = {}
                                if ly not in Analy[trace_count]['normal']:
                                    Analy[trace_count]['normal'][ly] = {}
                                if ly in Transevent:
                                    Analy[trace_count]['normal'][ly]['event'] = []
                                    for addr in Transevent[ly]:
                                        value = Transevent[ly][addr]
                                        Analy[trace_count]['normal'][ly]['event'].append((addr, value))

                                Analy[trace_count]['normal'][ly]['map'] = []
                                for addr2 in SSTORE[ly][now_index]:
                                    value2 = SSTORE[ly][now_index][addr2]
                                    Analy[trace_count]['normal'][ly]['map'].append((addr2, value2))
                                Analy[trace_count]['normal'][ly]['log_sc'] = now_token

                                continue

                    keytype = 'none'
                    if now_token in Contrl_Map:
                        keytype = 'map'
                        if now_token not in MapIndex:
                            print('error mapindex')
                        now_index = MapIndex[now_token]
                        if ly not in SSTORE:
                            continue
                        if now_index not in SSTORE[ly]:
                            continue
                        addrlist = SSTORE[ly][now_index]
                    elif now_token in Contrl_Event:
                        keytype = 'event'
                        if ly not in Transevent:
                            continue
                        addrlist = Transevent[ly]
                    else:
                        print('keytype error')

                    #还是要带上地址属性，那么地址属性要怎么做呢，用nowtoken
                    if 'controller' not in Analy[trace_count]:
                        Analy[trace_count]['controller'] = {}
                    if now_token not in Analy[trace_count]['controller']:
                        Analy[trace_count]['controller'][now_token] = {}
                    if keytype not in Analy[trace_count]['controller'][now_token]:
                        Analy[trace_count]['controller'][now_token][keytype] = {}
                    if ly not in Analy[trace_count]['controller'][now_token][keytype]:
                         Analy[trace_count]['controller'][now_token][keytype][ly] = []
                    for addr in addrlist:
                        value = addrlist[addr]
                        Analy[trace_count]['controller'][now_token][keytype][ly].append((addr, value))


                elif now_token in MapIndex:#普通的
                    if ly not in Transevent and ly not in SSTORE:
                        continue
                    if ly not in Transevent and ly in SSTORE and MapIndex[now_token] not in SSTORE[ly]:
                        continue
                    if 'normal' not in Analy[trace_count]:
                        Analy[trace_count]['normal'] = {}
                    if ly not in Analy[trace_count]['normal']:
                        Analy[trace_count]['normal'][ly] = {}
                    if ly in Transevent:
                        Analy[trace_count]['normal'][ly]['event'] = []
                        for addr in Transevent[ly]:
                            value = Transevent[ly][addr]
                            Analy[trace_count]['normal'][ly]['event'].append((addr, value))
                    if ly in SSTORE:
                        now_index = MapIndex[now_token]
                        if now_index not in SSTORE[ly]:
                            continue
                        Analy[trace_count]['normal'][ly]['map'] = []
                        for addr2 in SSTORE[ly][now_index]:
                            value2 = SSTORE[ly][now_index][addr2]
                            Analy[trace_count]['normal'][ly]['map'].append((addr2, value2))
                    Analy[trace_count]['normal'][ly]['log_sc'] = now_token
                else:
                    continue

            if len(Analy) >= 5000:
                wcount_analy += 1
                wname_balance = 'analy'+str(wcount_analy)
                with open(analysis_path+wname_balance, 'w') as f4:
                    acountlist = list(Analy.keys())
                    acountlist.sort()
                    for acount in acountlist:
                        f4.write(str(acount)+'#'+str(Analy[acount])+'\n')
                Analy = {}

# #test
# file1 = 'struct957'
# analy_trace(file1)

#加速
FileCount = {}
#入口
count = 0
with open(order_file_path, 'r') as f1:
    for line1 in f1:
        a1 = line1.strip('\n').split('#')
        filename = a1[0]
        FileCount[count] = filename
        count += 1

timecount = 0
Speed = {}
linecount = 0
txfiles = os.listdir(txcall_path)
txlen = len(txfiles)
for i in range(txlen):
    #每次读取十个txcall，判断哪些txhash需要分析，哪些不需要。另外要记得最后可能不足十个，也要处理
    txname = 'txcall'+str(i+1)
    with open(txcall_path+txname, 'r') as fsp:
        for line in fsp:
            alist = eval(line.strip('\n'))
            txhash = alist[0]
            for key in alist:
                if key in Controller or key in MapIndex:
                    fileindex = linecount // 1000
                    if fileindex not in Speed:
                        Speed[fileindex] = {}
                    Speed[fileindex][txhash] = 0
                    break
            linecount += 1#这样做保证第一千行可以在第一个文件里

        if len(Speed) >= 10:
            indexlist = list(Speed)
            indexlist.sort()
            for id in indexlist:
                filename = FileCount[id]
                txlist = Speed[id]
                analy_trace(filename, txlist)
            Speed = {}
            timecount += 1
            if timecount % 10 == 0:
                print(timecount)
                endtime = datetime.datetime.now()
                print(endtime - starttime)

indexlist = list(Speed)
indexlist.sort()
for id in indexlist:
    filename = FileCount[id]
    txlist = Speed[id]
    analy_trace(filename, txlist)

# 末尾结果记录
wcount_analy += 1
wname_balance = 'analy'+str(wcount_analy)
with open(analysis_path+wname_balance, 'w') as f4:
    acountlist = list(Analy.keys())
    acountlist.sort()
    for acount in acountlist:
        f4.write(str(acount)+'#'+str(Analy[acount])+'\n')
Analy = {}


endtime = datetime.datetime.now()
print(endtime - starttime)


