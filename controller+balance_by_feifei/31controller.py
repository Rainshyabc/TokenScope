# _*_ coding:utf-8 _*_
'''
解决跨合约问题，普通的controller
涉及这样几个点：
1.已经识别到的token，可以跳过不分析。
2.没识别到的，这次可以把那个from地址value更大的搞进去。……看情况
3.跨合约的话，这种（address,value）对，要做个链接，使他们是同一对。
4.考虑如何记录跨合约涉及的三个合约组。
5.考虑拿加速数据，记录txhash和涉及的token
'''

'''
方案：如果是跨合约的话，其实可以先装箱，后交互。这样起码可以保证是一个箱子里的。
'''
import ujson
import datetime
starttime = datetime.datetime.now()

########################## PLEASE SET YOUR WORKDIR ######################################
workdir = "/Users/tang/Desktop/TokenScope"

#loc path
# wefound_path = workdir + r"/new_balance_55332_mapping_index_all.txt"#55332个名单，要跳过他
# order_file_path = ''
# datalog_path = r'E:\BC\WWW\security\data\testfile\\'
# order_file_path = 'F:/BC/WWW/data/ordered_100.txt'
# datalog_path = 'F:/BC/WWW/data/100_data/'
#result_path
txcall_path = workdir + r'/balance_map/txcall/'


order_file_path =workdir + '/other-100/ordered_filename_time_blocknumber_100.txt'
datalog_path = workdir + '/other-100/100_data_1/'
# datalog_path = 'F:/www-expand/test_controller_trace/controller_trace-2/controller_trace/'
# result_path
balance_path = workdir + r'/balance_map/findmap/'
error_path = workdir + r'/balance_map/error1/'

# #服务器路径-zihao
# wefound_path = '../BalanceMapping_tokenlist.txt'
# order_file_path = '/media/HardDisk4T/lt/datasetmove'
# datalog_path = '/media/HardDisk4T/movedatalog/'
# txcall_path = '../txcall/'
# balance_path = '../findmap/'
# error_path ='../error/round1/'

# #服务器路径-chenting
# wefound_path = '../BalanceMapping_tokenlist.txt'
# order_file_path = '/media/yulele/HardDisk10TB/icse/core/lt/formal_ordered_filename_time_blocknumber.txt'
# datalog_path = '/media/yulele/HardDisk10TB/www/syncdata/syncdatalog/'
# txcall_path = '../txcall/'
# balance_path = '../findmap/'
# error_path ='../error/round1/'

#定义全局变量
#建立Transfer_event的字典
transfer_hash = {'2c4d9d1041355b152e80b28195d8cd57a1363203c2b1a39c0559f0e757747d5c': 'uint8', '89896edbd223c9360ce42ddfed7522a2bffb20c056e4c42d42370cb493b65676': 'uint16', '4c3f23e06500a14887485511327c0d579fbccac302d5839c043bcc62bf867793': 'uint24', '0daf680c3f528a8760b5142fe1f6f80d5f4ea18bb76f347a7a44a2d565c2b7dc': 'uint32', 'cdabd7cd7a44bd50521a39c666b076577c82465c3615f66391d096cc719c6ac0': 'uint40', 'e18706cb56ac477fbc72c6acbbd512822f259c1f09006247dbae41d881bc3e17': 'uint48', 'f0cd1a5c0ee7db84a3a9327b544161b199d1a1088d6dd1c99d42646432eaf9fb': 'uint56', '831ac82b07fb396dafef0077cea6e002235d88e63f35cbd5df2c065107f1e74a': 'uint64', 'bff91d4903077cc645099227f3ff63fa8f7c4e51de89afbefde6b29eb549af87': 'uint72', 'a0f2d9d810b7227d93b1d65511f1321d5331a7a323e6d357130dda4aa99690a0': 'uint80', '1c232f833daad9ed1224c5770c053a18edfef5d85918dede55acc1da05ab6c8b': 'uint88', 'ba7196a4bdbfed2416fed23830b5c875c6e32d81744212e9776f7d2b02a33188': 'uint96', '18b3a374e2313c602fb9e4002182a9b948dff0294feab6f98f5e7e4334ef7e9d': 'uint104', 'b7ac3c4762d5a753158c22506d7f1a1373c52dae6059cc91115338581b05e27c': 'uint112', '91925c49b49f6ee4ac0d966d8d2e700e489f031bf933396b5b64bc584529d229': 'uint120', '27772adc63db07aae765b71eb2b533064fa781bd57457e1b138592d8198d0959': 'uint128', '46518209995f34a01926b792690bc92e5037b070563bfdacd84fafd40b513eb5': 'uint136', 'e8032327ba5bd636272f39d92559de88e80732a9d637d0b6752d51281150d4b7': 'uint144', '48c4fa90124ada7723a851f5a30fc80851bbfab1f12649e3ae71a32c627720cd': 'uint152', 'df5c409937706803ae64d124b48586638c7b50733b40fb16cff8141ffa1e0af8': 'uint160', 'd0966ead8911bd02ec5119ed64d10236cb4fd8f29c5001afb73d60689cf88b20': 'uint168', 'b18cf775c754b8fae1157af9b1f2b93496f6bf0cd582c24d7175692fcaa1cd21': 'uint176', 'fcdacb06893591fedb6582b761d2e964d37a4e7f77a844e3a05c5fbf47797c0e': 'uint184', '74c9ae5ff92efee44f316c09cbdbdebb254705f4fd59514ed2d87e1e3da93913': 'uint192', '7344fa9abcab6b3790a118567725311a6bfb30957589e825e4300bce8f3fb020': 'uint200', 'bae695334f1401f46a8c246fb4e028ccdee498d6cd47ddb5683ab940d25fbdc5': 'uint208', '3fb8d49d89b30c4ee5141c3d10e5bb70e95d5babd584e3000107d2dac22a826a': 'uint216', '354cd84171949f23d6c7393b4deca6b9670954625ffedcb35a250a15a08515ed': 'uint224', 'cf73f4a4f977af3327646216f7d3af8970de9bc70aeaf76009cec99dcf46c786': 'uint232', 'c2ac9a11e79ddfc35c6403b568c9d85957090c8416d338be90299141f1e7f425': 'uint240', 'fe28b6744e16875301806797283f9bcc1a29b15f700c0e088645e2c257eec1e5': 'uint248', 'ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef': 'uint256', 'fdb0d9db4fcfa99a69bab4019cf42ab495be117bb60275b901645c28ca3deef4': 'int8', '1306f300bdf23ef00b1fe00644eee04b9576ad8c68837bffa5158e4693ea296a': 'int16', '1315fe0300efd5bde69c874d107401124940c3cdb534666230a2436a47e6a49b': 'int24', 'b659f7922125405e40eb1a5fbfd9879f3d296b8200019be90f730b459f9f1c25': 'int32', 'b76456965aa890ee11746d3b26582281ffca539801841abe6282ab73b2c01993': 'int40', 'fd0e41a48c016debc0ec3c87cdf02ba5e2eb2db4587292c6bdcec7bda1fc3d3c': 'int48', 'bc87650eb8e9c481db3f2576aea1b4e653894d93b7f6cb6a190717a1fca3a319': 'int56', 'cef55929759435389feb62e3ad30d90911d061d3eb8f8e3ead60622531745cc1': 'int64', '19b40000025b47ecd4d2940168402cfe9317418307f848216988dc028e628214': 'int72', 'e670604a3a027fa22059b623a5b0ae38424829237d769b02282dc7d81fb06426': 'int80', '303dc7e5a79ee0ca02c3f06db0502fbfe7a964cd8fa597919e4376f6dbc1e157': 'int88', '0ed1306281e9b4c9d018e1291d83fd014895d20c95da608569e7d9a5361117aa': 'int96', 'a87ac4316a9088110eb185cf27691b5533890444b36f2712b700fe09a5e53ba7': 'int104', '2c5825beae12151d954009ae7f95e998300458d351c8fc8e6d2df9a8753d65a7': 'int112', 'e64efe620012ecf67a6a08208071cfd55ea85c641860fa711388c041c80d72f6': 'int120', '9ce147531995c591b0b50012b20f7f6d0dea75281159a58b8637542388f14626': 'int128', 'e86307cdc23d5574d14f14c07d08814d980276c4b92d6d51e6f6497a807607c8': 'int136', 'a099bc2413531106e46903e9bd7f34d43b6d124631398348d1d5f368baeb8032': 'int144', '467c5dc3035b08b8eda1206c6049fd8eb86db17119be0ca51d0de6f99bf7f548': 'int152', '8d1591cfd32ad19c215c6295623aea4eec85442fc5c4601cda6f7e0a038186ba': 'int160', '4ec3ba770fb8428f5ce8590bc4b28663359570e0193206f9364399c06e768241': 'int168', '7f02f13368f9b374a15f81ad02096044b4c26fa5127a1fa37aeed8e392bd6edd': 'int176', '6e348e9e7927772dff9da0764845053058a54199928284bfe6decb7ac09d40d7': 'int184', 'a88a4735393a2bbb1c23c083874e1d0636d3e87851b6f20a6d2115f5ea540ba0': 'int192', '96a6ed04a9960ed29f91a03141a1256a7e6204eb90c319d76a91ec4aa02bbc2f': 'int200', 'cbab2a67020e790d89db09e426191c44c8c05d9f93dc1f8cc32dda14929f40e5': 'int208', '7c11167a36b8ef38fc546598e268c0964bb2cb21377e6cb80e217bcb6ecb8c67': 'int216', 'f238e8301c28c0dac41fcc9bd2e2d659096a02384c2ffd9b1430ac584c95691e': 'int224', 'd6e7a41c23f4209ee7bed2dbe1d4774884aaf836b11d0c93a84b8eb44878dbd3': 'int232', '81031c58ed866f2ba7f5ac8c702cedc31ed6b4a08cd1d540c988018b0ca5b845': 'int240', '8695741cd0cb852f381bcfad35ffa6af9b0f4d1634247d0b2589ad84233dc590': 'int248', '8b0c34a52f9e28d78caaa7066cd047b398dae74941a208b77777420f492bd7e1': 'int256'}
address0 = '0000000000000000000000000000000000000000000000000000000000000000'
wcount_txcall = 0
wcount_balance = 0
WeFound = {}
#记录结果
BALANCE = {}#contract:index记录mapping index
TxCall = {}#i:[txhash,con1,con2,con3]按顺序记录所有TXcall中的合约调用关系，这个其实是layersc就有的


def analy_trace(filename):
    global BALANCE
    global TxCall
    global transfer_hash
    global wcount_txcall
    global wcount_balance
    global WeFound
    with open(datalog_path+filename, 'r') as f2:
        for line2 in f2:
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

            # #test
            # if txhash != '6549492df34b71830e9bd083317f46e934c87ac3cbf3a68952d03fccb7fd4f1a':
            #     continue
            # else:
            #     print(trace)
            #     return

            # blocknumber = eval(trace['LOG_blocknumber'])  #type str
            # time = eval(trace['LOG_timestamp'])  #type str
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
                    layindex = str(layer)+'#'+stindex
                    if layindex not in SSTORE:
                        SSTORE[layindex] = {}
                    if staddr not in SSTORE[layindex]:
                        SSTORE[layindex][staddr] = 0
                    SSTORE[layindex][staddr] += balance

            length1 = len(TxCall)
            TxCall[length1] = [txhash]
            lylist = list(LayerSC.keys())
            lylist.sort()
            for ly in lylist:
                sc = LayerSC[ly]
                TxCall[length1].append(sc)

            #loc
            if len(TxCall) == 5000:
                wcount_txcall += 1
                wname_txcall = 'txcall'+str(wcount_txcall)
                with open(txcall_path+wname_txcall, 'a') as f3:
                    for key in TxCall:
                        f3.write(str(TxCall[key])+'\n')
                TxCall = {}

            if break_flag == 1:
                continue

            '''
            开始匹配
            1.某一个Index被识别到的次数，与event长度相匹配.index_address_value都匹配。index匹配上的次数应当和event字典长度相同。
            2.当event中遇到了0和this要去掉。
            这时候有个问题就是，到底是用event和map匹配，还是用map和event匹配呢？用map吧
            3.在这里可以记录下来controller对，就是谁负责event谁负责map
            '''

            for lay_index in SSTORE:
                find_flag = 0
                map_contract = 'none'
                event_contract = 'none'
                stlayer = int(lay_index.split('#')[0])
                if stlayer in Invalid_Layer:
                    continue
                map_contract = LayerSC[stlayer]
                stidx = lay_index.split('#')[1]
                mapdic = SSTORE[lay_index]
                if stlayer in Transevent:#先查看本层有没有event，如果有就在本层匹配
                    transdic = Transevent[stlayer]
                    find_flag = match_balance(mapdic, transdic, map_contract, 0)
                else:#本层没有，遍历其他层，进行匹配
                    for ly in Transevent:
                        if ly in Invalid_Layer:
                            continue
                        transdic = Transevent[ly]
                        find_flag = match_balance(mapdic, transdic, map_contract, 1)
                        if find_flag == 1:
                            event_contract = LayerSC[ly]
                            break

                if find_flag == 1:#匹配到了
                    # # test
                    # if map_contract == 'c9c3a465380bfaac486c89ff7d5f60cc275d4e08':
                    #     print(filename)
                    #     print(txhash)

                    contract_couple = (map_contract, event_contract)
                    if contract_couple not in BALANCE:
                        BALANCE[contract_couple] = {}
                    if stidx not in BALANCE[contract_couple]:
                        BALANCE[contract_couple][stidx] = 0
                    BALANCE[contract_couple][stidx] += 1

            #loc
            if len(BALANCE) >= 5000:
                wcount_balance += 1
                wname_balance = 'findmap'+str(wcount_balance)
                with open(balance_path+wname_balance, 'a') as f4:
                    for sccp in BALANCE:
                        f4.write(str(sccp)+'#'+str(BALANCE[sccp])+'\n')
                BALANCE = {}

#都是address_value对
def match_balance(mapdic, transdic, this, control_flag):
    # print(this+':'+str(control_flag))
    # print(mapdic)
    # print(transdic)
    # print('===================='*5)

    this = this.zfill(64)
    global address0
    if mapdic == transdic:
        return 1
    else:
        if address0 in transdic and address0 not in mapdic:
            del transdic[address0]
        if this in transdic and this not in mapdic:
            del transdic[this]
        if mapdic == transdic and mapdic:
            return 1
        else:
            if mapdic == {}:
                return 0
            if control_flag == 1:#0代表不是跨层,1代表是跨层,跨层不做收费检测
                return 0
            #收费的个例识别，收费的仅限于非controller的情况
            event_addr_list = list(transdic.keys())
            map_addr_list = list(mapdic.keys())
            event_addr_list.sort()
            map_addr_list.sort()
            if event_addr_list == map_addr_list:#名单相同，可能出现收费情况,from扣费多。扣的绝对值大。
                find_num = 0
                for addr in event_addr_list:
                    event_value = transdic[addr]
                    map_value = mapdic[addr]
                    if event_value > 0:#to地址
                        if event_value == map_value:
                            find_num += 1
                        else:#直接跳出循环
                            break
                    else:#from地址
                        if abs(event_value) <= abs(map_value):
                            find_num += 1
                        else:
                            break
                if find_num == len(transdic):
                    return 1
        return 0

# #test
# file1 = 'struct957'
# analy_trace(file1)


#入口
count = 0
with open(order_file_path, 'r') as f1:
    for line1 in f1:
        count += 1
        # #loc
        # if count % 10 == 0:
        #服务器
        if count % 200 == 0:
            print(count)
            endtime = datetime.datetime.now()
            print(endtime - starttime)
        a1 = line1.strip('\n').split('#')
        filename = a1[0]
        try:
            analy_trace(filename)
        except:
            print('error')
            with open(error_path+'error1.txt', 'a') as f5:
                f5.write(filename+'\n')

# 末尾结果记录
wcount_txcall += 1
wname_txcall = 'txcall'+str(wcount_txcall)
with open(txcall_path+wname_txcall, 'a') as f3:
    for key in TxCall:
        f3.write(str(TxCall[key])+'\n')
TxCall = {}

wcount_balance += 1
wname_balance = 'findmap'+str(wcount_balance)
with open(balance_path+wname_balance, 'a') as f4:
    for sccp in BALANCE:
        f4.write(str(sccp)+'#'+str(BALANCE[sccp])+'\n')
BALANCE = {}


endtime = datetime.datetime.now()
print(endtime - starttime)


