# _*_ coding:utf-8 _*_
'''
需求：利用拿到的mapindex解析trace，记录所有有关allowed的信息。为后续的不一致信息提取提供中间数据。
目前的一个方案是，遇到approval或者allowed，那么该条trace该层的所有信息都记录。如果只有transfer，则不记录。用一个flag+layer.
具体的记录方案为：
1.单条trace,以层数为单位，记录该层的信息。如果是approval，就记录event和map
2.如果是transferFrom函数，就记录的是map和event.如果只有event没有map,就啥都不记录。由于这里要和balance匹配。因此，要和图图统一格式。——统一格式可以第三步做。
具体的格式：
单条trace:{txhash;blocknumber;time;layx:{sc;map:[（ad1,ad2,value)];transevent:[];appevent:[]}}
'''
#标记（凡是标记部分，正式跑之前都要删掉）：test；loc/服务器;

import os
import ujson
import datetime
starttime = datetime.datetime.now()

# #locpath
order_file = 'F:/www/other100/other_100_test/ordered_filename_time_blocknumber_100.txt'
datalog_path = 'F:/www/other100/other_100_test/test/'
# # order_file = 'F:/BC/WWW/data/other-100/ordered_filename_time_blocknumber_100.txt'
# # datalog_path = 'F:/BC/WWW/data/other-100/100_data_1/'
findmapresult_path = 'F:/www/other100/FirstRound/findmapresult/'
error_path = 'F:/www/other100/FirstRound/error/'
usemap_path = 'F:/www/other100/FirstRound/usemap/'#result

# #服务器路径-zihao
# order_file = './order5W'
# datalog_path = '/media/HardDisk4T/movedatalog/'
# findmapresult_path = './findmapresult/'
# error_path = './error/round2/'
# usemap_path = './usemap/'

#服务器路径-chenting
# order_file = './order7W'
# datalog_path = '/media/yulele/HardDisk10TB/www/syncdata/syncdatalog/'
# findmapresult_path = './findmapresult/'
# error_path = './error/round2/'
# usemap_path = './usemap/'

#建立Transfer和Approval的字典
transfer_hash = {'2c4d9d1041355b152e80b28195d8cd57a1363203c2b1a39c0559f0e757747d5c': 'uint8', '89896edbd223c9360ce42ddfed7522a2bffb20c056e4c42d42370cb493b65676': 'uint16', '4c3f23e06500a14887485511327c0d579fbccac302d5839c043bcc62bf867793': 'uint24', '0daf680c3f528a8760b5142fe1f6f80d5f4ea18bb76f347a7a44a2d565c2b7dc': 'uint32', 'cdabd7cd7a44bd50521a39c666b076577c82465c3615f66391d096cc719c6ac0': 'uint40', 'e18706cb56ac477fbc72c6acbbd512822f259c1f09006247dbae41d881bc3e17': 'uint48', 'f0cd1a5c0ee7db84a3a9327b544161b199d1a1088d6dd1c99d42646432eaf9fb': 'uint56', '831ac82b07fb396dafef0077cea6e002235d88e63f35cbd5df2c065107f1e74a': 'uint64', 'bff91d4903077cc645099227f3ff63fa8f7c4e51de89afbefde6b29eb549af87': 'uint72', 'a0f2d9d810b7227d93b1d65511f1321d5331a7a323e6d357130dda4aa99690a0': 'uint80', '1c232f833daad9ed1224c5770c053a18edfef5d85918dede55acc1da05ab6c8b': 'uint88', 'ba7196a4bdbfed2416fed23830b5c875c6e32d81744212e9776f7d2b02a33188': 'uint96', '18b3a374e2313c602fb9e4002182a9b948dff0294feab6f98f5e7e4334ef7e9d': 'uint104', 'b7ac3c4762d5a753158c22506d7f1a1373c52dae6059cc91115338581b05e27c': 'uint112', '91925c49b49f6ee4ac0d966d8d2e700e489f031bf933396b5b64bc584529d229': 'uint120', '27772adc63db07aae765b71eb2b533064fa781bd57457e1b138592d8198d0959': 'uint128', '46518209995f34a01926b792690bc92e5037b070563bfdacd84fafd40b513eb5': 'uint136', 'e8032327ba5bd636272f39d92559de88e80732a9d637d0b6752d51281150d4b7': 'uint144', '48c4fa90124ada7723a851f5a30fc80851bbfab1f12649e3ae71a32c627720cd': 'uint152', 'df5c409937706803ae64d124b48586638c7b50733b40fb16cff8141ffa1e0af8': 'uint160', 'd0966ead8911bd02ec5119ed64d10236cb4fd8f29c5001afb73d60689cf88b20': 'uint168', 'b18cf775c754b8fae1157af9b1f2b93496f6bf0cd582c24d7175692fcaa1cd21': 'uint176', 'fcdacb06893591fedb6582b761d2e964d37a4e7f77a844e3a05c5fbf47797c0e': 'uint184', '74c9ae5ff92efee44f316c09cbdbdebb254705f4fd59514ed2d87e1e3da93913': 'uint192', '7344fa9abcab6b3790a118567725311a6bfb30957589e825e4300bce8f3fb020': 'uint200', 'bae695334f1401f46a8c246fb4e028ccdee498d6cd47ddb5683ab940d25fbdc5': 'uint208', '3fb8d49d89b30c4ee5141c3d10e5bb70e95d5babd584e3000107d2dac22a826a': 'uint216', '354cd84171949f23d6c7393b4deca6b9670954625ffedcb35a250a15a08515ed': 'uint224', 'cf73f4a4f977af3327646216f7d3af8970de9bc70aeaf76009cec99dcf46c786': 'uint232', 'c2ac9a11e79ddfc35c6403b568c9d85957090c8416d338be90299141f1e7f425': 'uint240', 'fe28b6744e16875301806797283f9bcc1a29b15f700c0e088645e2c257eec1e5': 'uint248', 'ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef': 'uint256', 'fdb0d9db4fcfa99a69bab4019cf42ab495be117bb60275b901645c28ca3deef4': 'int8', '1306f300bdf23ef00b1fe00644eee04b9576ad8c68837bffa5158e4693ea296a': 'int16', '1315fe0300efd5bde69c874d107401124940c3cdb534666230a2436a47e6a49b': 'int24', 'b659f7922125405e40eb1a5fbfd9879f3d296b8200019be90f730b459f9f1c25': 'int32', 'b76456965aa890ee11746d3b26582281ffca539801841abe6282ab73b2c01993': 'int40', 'fd0e41a48c016debc0ec3c87cdf02ba5e2eb2db4587292c6bdcec7bda1fc3d3c': 'int48', 'bc87650eb8e9c481db3f2576aea1b4e653894d93b7f6cb6a190717a1fca3a319': 'int56', 'cef55929759435389feb62e3ad30d90911d061d3eb8f8e3ead60622531745cc1': 'int64', '19b40000025b47ecd4d2940168402cfe9317418307f848216988dc028e628214': 'int72', 'e670604a3a027fa22059b623a5b0ae38424829237d769b02282dc7d81fb06426': 'int80', '303dc7e5a79ee0ca02c3f06db0502fbfe7a964cd8fa597919e4376f6dbc1e157': 'int88', '0ed1306281e9b4c9d018e1291d83fd014895d20c95da608569e7d9a5361117aa': 'int96', 'a87ac4316a9088110eb185cf27691b5533890444b36f2712b700fe09a5e53ba7': 'int104', '2c5825beae12151d954009ae7f95e998300458d351c8fc8e6d2df9a8753d65a7': 'int112', 'e64efe620012ecf67a6a08208071cfd55ea85c641860fa711388c041c80d72f6': 'int120', '9ce147531995c591b0b50012b20f7f6d0dea75281159a58b8637542388f14626': 'int128', 'e86307cdc23d5574d14f14c07d08814d980276c4b92d6d51e6f6497a807607c8': 'int136', 'a099bc2413531106e46903e9bd7f34d43b6d124631398348d1d5f368baeb8032': 'int144', '467c5dc3035b08b8eda1206c6049fd8eb86db17119be0ca51d0de6f99bf7f548': 'int152', '8d1591cfd32ad19c215c6295623aea4eec85442fc5c4601cda6f7e0a038186ba': 'int160', '4ec3ba770fb8428f5ce8590bc4b28663359570e0193206f9364399c06e768241': 'int168', '7f02f13368f9b374a15f81ad02096044b4c26fa5127a1fa37aeed8e392bd6edd': 'int176', '6e348e9e7927772dff9da0764845053058a54199928284bfe6decb7ac09d40d7': 'int184', 'a88a4735393a2bbb1c23c083874e1d0636d3e87851b6f20a6d2115f5ea540ba0': 'int192', '96a6ed04a9960ed29f91a03141a1256a7e6204eb90c319d76a91ec4aa02bbc2f': 'int200', 'cbab2a67020e790d89db09e426191c44c8c05d9f93dc1f8cc32dda14929f40e5': 'int208', '7c11167a36b8ef38fc546598e268c0964bb2cb21377e6cb80e217bcb6ecb8c67': 'int216', 'f238e8301c28c0dac41fcc9bd2e2d659096a02384c2ffd9b1430ac584c95691e': 'int224', 'd6e7a41c23f4209ee7bed2dbe1d4774884aaf836b11d0c93a84b8eb44878dbd3': 'int232', '81031c58ed866f2ba7f5ac8c702cedc31ed6b4a08cd1d540c988018b0ca5b845': 'int240', '8695741cd0cb852f381bcfad35ffa6af9b0f4d1634247d0b2589ad84233dc590': 'int248', '8b0c34a52f9e28d78caaa7066cd047b398dae74941a208b77777420f492bd7e1': 'int256'}
approval_hash = {'611d0801b9a936d7e62d45aa93e967f00a929991de32d84517019e3dcf9eef5d': 'uint8', '0a9d294fd4bd42bb30e96cba2b478d149a783fba3c729b1e5c42bec89d95b85a': 'uint16', 'b3ba96ffca58a5c0843f7fa57ac208298b3b86e7feed3d33a9f706270c2626e9': 'uint24', 'e26b9b29b95cb706aaebdd86a3524de879b8590b0ba7e61b104f54196bab2031': 'uint32', '4c3c5c1dcab266f9cbc926f6e78bcd8f584e9dc3d081f3fcc0e7d78958a86369': 'uint40', '4796d4e837f21da69df41f03f3e0a8d62bf832a6392dc107c5e4ab6162fc34f9': 'uint48', '4ed3c7595630c834d0daa2ff368f18fe007667949f4b54b1e191af11c61b6ad7': 'uint56', '16304dfea7f3fbabcf59225f0629cb307fecb8d5652b069080aa9be2c765d7d2': 'uint64', '2318f7d28490f7cee21d53e90848ad9cb2ddc35468fee892b94294a8ba3f28c4': 'uint72', '3212f41ec92f177d999db7467a64faeb241827d867f4f176dc2be61581122d1a': 'uint80', '9e7c8d7ae45ef86759782f7bebc2eb949dfb477bec28976151ae39c2999509f3': 'uint88', '19ed2b70d0b204384ff1671abf69ee2e07332f5827fb8ef9eaccefd3c4fd84f6': 'uint96', 'ac4baab1a1c0abe1ef1a20d8b649aeec8e1d58fd87cea8dead3290994d4abbc7': 'uint104', '2c2717f8c0c9abadb94086901ff3a5e3c416e2735086be753e96912ddd05cf58': 'uint112', 'bdd455a9c6236e658d0ef088cb976eda861c5a5ae1c6cd7f3cced3f40b4cdbf4': 'uint120', '444360fd9f99263247bc59eb6f6c9f5d7f1096ba7962aa22cb94c3f5b743eded': 'uint128', '4cbd576684a0d88e1eda10cdba47dbecbbcbb4d189e93e26d5d4e380f978d618': 'uint136', '2589c40a575d794a67d5a80b470a7781a46bfc7b8366a306c614e4cc2f4f422c': 'uint144', 'fd5dd4bbb12e80230ca445967fe3c2bc44df0f2855264f70db91e36eb79bf149': 'uint152', '621afae5277bf1254bd37441bf7675038b2d92e67e36528d50ece5edd980f66c': 'uint160', '40f6e77ac39abbf03c972224330b0ba8141e027d7e897417dbad3a0fb8f1e05b': 'uint168', 'c11ab962196b359249cad722175c1b5bf5cb11978203ff6d024d94376db7f53e': 'uint176', 'dea3fc7d6bda2134fdd0a80a5048a8e18a21123ab7602a96e6acafa6a71c0882': 'uint184', '28b2637e74d43adce90ce8a563f56362d98649573b41067d7c9791d27d172572': 'uint192', 'ae90dba1fd8e9c6d13db5e2b121ee33a4f8f00c08acd401a69a24c3a6ae961f2': 'uint200', '99315e87058049e818e24b3b1a3df7997e1aaedfccf2fbf0ef91d40e27ff7fd8': 'uint208', '7aac39111fb107ed22b8f218f5f9875ca36c89fa77d3d0d04671b73fa7a94de2': 'uint216', 'b9244d497d09501d52dac5a497c9984c496446e94a9d0b25b81d6e4c745a9937': 'uint224', 'fa1549e4470b16217f1640a3d9b9256ade6f391093ad06d7f3623110ffc9034b': 'uint232', 'a10a7a77144cd5dc9e7b671f64747886004404bd02e5793fd42795b80129f13f': 'uint240', 'e3e78edbddaa50bbc62ae668141bad4163a767a486bb9dc900ae35760a867202': 'uint248', '8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925': 'uint256', '1947fcfd1c8eae160c7ca1c8affe63589686ecdbb87a258806510501e488f480': 'int8', '37d66f019b45f660b9261b17e835866b935da926f56881ed8d74331b2e37b658': 'int16', 'e1812197073582e52673fcebab69b805a362d9a897ea9403e1d9e1c95997d0f0': 'int24', 'd7dc3a93fb6f3edcfa2cf33339b05f153f5ed077e3e345e60dd896d2e601e076': 'int32', '2f5b2046f7a840ce2f195bb06b361bf0d3b926bcdbad64b3d9c4044515c2348d': 'int40', '42b630f4dfe0ad7dd2c36d0932e6854307de3cff90496ac90ea1ed2a4562c4ed': 'int48', 'cecffb51bbd45f2f3b09fb2301afda04849e6f646ab97d90017f0c35a83ff29c': 'int56', '61df88c5062f70a3a49980efd761a155cabdf187e1cace20a98f85655ccdbac7': 'int64', 'eeacb6c03f31f9b6752cdedbfb0042fde0d2e00bd500d92d7e14503daa1fb208': 'int72', 'ab5b01ad1163a3cc4a5112cb4ae1335ab2f2ed8d8fb9a6fb8d39e1edb64eaacc': 'int80', 'b36c77c1f139a72ae511f910ea7b927ed5b366ff739e080846bc3d5d74493a69': 'int88', 'ca9055347a5ffd54d7d7e53f2cce0bb71812b5d0409558db343759583efe43b3': 'int96', 'df8dbb8d1c42cf6fdacf3c02e0b36be64fd74616cf8114866d55b898f4504349': 'int104', 'd77a66b5574966f4d3af1bf1f62250f66cfbd0c7a0564c2864fcfb594e41cc81': 'int112', '3a51815283643d21deed182a2871dcb3a674ce6e97f66abd3209b1763841d03d': 'int120', '62b2917683ac3406e3d9cfb4e95a047ae041fc4928b2b723e50cbaa04cca6216': 'int128', 'bc9e8fbdec1db655e7143c5a13848d9db39d701780345ae5cc9fe8c2e55d89d6': 'int136', '24a99c930a2787abb8ffbdcc6d1db5a44e9510f65fd1caa3928422cedfb7deb8': 'int144', 'be5d5a4d573fe6be806e178742dfd1e545f4e989efdfea48e520f4ad5a159975': 'int152', '0db6498167d89be3bfc62869d54b215d17ded3c55ba6d8abec7a00c399b688c0': 'int160', 'db29719e85079ee8dd509f9f95b2728a5842a2237e1bdd959264914b24f5df74': 'int168', '82cece37c7ba2bb254ea82dd96052d1c9f433c5c874019f6836c543acde81255': 'int176', 'f82536e2b93ffe7001f1bec1e1e4a223fa0bcb2c4ae0294b7e155e6c0e98bc89': 'int184', '12fd8185e5fefef133399d8d789f6f3db6cd6ea4c078dcb017105e8d2ce2556f': 'int192', 'fbdde4d2695291e10a7d05a942cbdf8336d27075cc428054d8234d596d77b7f0': 'int200', 'e85f62a051ae1b89e66d58f9c0cfa9282c4c732d37c1838e9217b7daf64e4534': 'int208', '0ac87ee9a1d376d59e62fac27da795fc55d3e9b88a8215f6d383e877280a20c4': 'int216', '4aee8d2b10ca88e143a1acc8dc445b35f3447f24cf7ca4066c846f0493ce8823': 'int224', 'c38731ddbb1d7560eee4fbe184a38a1e68e8b97190736138b9e219ed213c2562': 'int232', '2eb19f930d15a26a73aca8a321ac079f65469c955849067d916f30078ab8d21c': 'int240', '4ce85f62f0c56e3f407acc809bf5ab8260d71814a63300d1699142229cc96dd0': 'int248', 'ec06647eb3d581d530bd6914e5c859db8edbc5bfb6bffa5d4cf720b824295e0a': 'int256'}

#字典存储所有token的mapindex
ALLOWMAP = {}
files1 = os.listdir(findmapresult_path)
for file1 in files1:
    with open(findmapresult_path+file1, 'r') as f0:
        for line0 in f0:
            a0 = line0.strip('\n').split('#')
            sc = a0[0]
            mapindex = a0[1]
            ALLOWMAP[sc] = mapindex

#记录最终结果的全局字典
USEMAP = {}
usecount = 0
wcount = 0


#解析trace
def usemap(filename):
    global ALLOWMAP
    global USEMAP
    global usecount
    global wcount
    with open(datalog_path+filename, 'r') as f2:
        for line2 in f2:
            #记录USEMAP的个数
            usecount += 1
            USEMAP[usecount] = {}
            #还原外部交易失效标志
            break_flag = 0
            #每一笔交易维护一个栈
            txstack = ['ept']#ept表示一开始没有call也没有create。
            stack_count = 0
            LayerSC = {}#栈顶-sc
            create_addr_flag = 0 #判断是createend前还是之后的createaddr，前为0，后为1
            create_error_flag = 0
            #记录失效层数
            Invalid_Layer = {}
            poplayer = 0
            #记录双层sha3和sstore
            SHA3dic = {}
            SSTORE = {}


            #开始解析
            trace = ujson.loads(line2)
            txhash = eval(trace['LOG_txhash'])  #type str
            blocknumber = eval(trace['LOG_blocknumber'])  #type str
            time = eval(trace['LOG_timestamp'])  #type str

            # #test
            # if txhash != 'd09f7389bb2ca1f47d6e485a32d446766078c7fbf3359b73c3b9f1a141ca8d0e':
            #     continue

            #记录头数据
            USEMAP[usecount]['log_txhash'] = txhash
            USEMAP[usecount]['log_block'] = blocknumber
            USEMAP[usecount]['log_time'] = time

            opinfos = list(eval(trace['LOG_opinfos']))
            for op in opinfos:
                opcode = eval(op)   #type dic
                log_type = opcode['log_type']

                '''
                在解析的时候一定要注意次序。
                单条trace:{txhash;blocknumber;time;layx:{map:[（ad1,ad2,value,sc)];transevent:[];appevent:[]}}
                '''
                #维护栈结构，此时内外部有了区别，同时有了error字段，需要区分。
                if log_type == 'CALL':
                    stack_count += 1
                    txstack.append(stack_count)
                    contract = opcode['to_addr']
                    LayerSC[stack_count] = contract
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
                    create_error_flag = 1
                if log_type == 'CREATE_ADDR':
                    layer = txstack[-1]
                    if create_addr_flag == 0 and layer != 1:#说明在create end之前
                        continue
                    else:
                        contract = opcode['to_addr']
                        if create_addr_flag == 1:
                            LayerSC[poplayer] = contract
                        else:
                            LayerSC[layer] = contract
                            if layer != 1:
                                print('layererror')
                        create_addr_flag = 0
                        create_error_flag = 0

                if log_type == 'CREATE_F' or log_type == 'CREATE_R':
                    if create_error_flag == 0:
                        continue
                    elif create_error_flag == 1:
                        create_error_flag = 0
                        create_addr_flag = 0
                        Invalid_Layer[poplayer] = 0
                    else:
                        print('create_error_error')
                #整条交易失败，进行下一条交易，就是下一个for line in f
                if log_type == 'OUT_E' or log_type == 'OUT_I':#这里出了问题，并不是所有的outi都存在
                    break_flag = 1
                    break

                #event解析
                if log_type == 'LOGX':
                    layer = txstack[-1]
                    if layer == 'ept':
                        continue

                    nowlayer = 'lay'+str(layer)
                    if nowlayer not in USEMAP[usecount]:
                        USEMAP[usecount][nowlayer] = {}

                    #此处无法判断该层是否失效，只能按照层数记录这个数据，然后失效的话最后清空
                    topic0 = opcode['log_topics'][0:64]
                    topic0 = topic0.lower()
                    if topic0 in transfer_hash or topic0 in approval_hash:
                        topics = opcode['log_topics']
                        middle = topics.split('#')
                        topics1 = ''
                        for md in middle:
                            if md != '':
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
                        eventtp = (fromaddr, toaddr, inputdata)
                        #进行存储。存储结构是为了便于后续的匹配。起码要包括层数信息。分成transfer和approval两种去记录；approval不需要合并。并且应该不会有重复。
                        if topic0 in transfer_hash:
                            if 'trans_event' not in USEMAP[usecount][nowlayer]:
                                USEMAP[usecount][nowlayer]['trans_event'] = []
                            USEMAP[usecount][nowlayer]['trans_event'].append(eventtp)
                        elif topic0 in approval_hash:
                            if 'app_event' not in USEMAP[usecount][nowlayer]:
                                USEMAP[usecount][nowlayer]['app_event'] = []
                            USEMAP[usecount][nowlayer]['app_event'].append(eventtp)

                '''
                改到了这里，如何才能利用我的mappingindex去做呢？可以按照层数存储sha3和sstore，然后最后用层数-合约-index-sha3
                如果是这样的话，首先sha3：key是层数，根据层数存储每一层内容。sstore也是层数。根据层数去取
                找的时候，根据层数拿到栈顶合约，然后根据栈顶合约拿到index，然后找哪一个sha3的index符合，所以第二层是按照index为key
                sha3 = {layer:{index：}}
                这里首先每个index肯定会出现很多次，因为要和不同的addr结合。然后同一个index，不同的addr产生不同的keccak
                sha3 = {layer:{index：{addr:keccak}}}
                当找到了某一个addr的keccak，要去同一层的sstore取值。如何存储呢？
                '''
                #sha3
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
                    mp_addr = sha3_content[-128:-64]
                    mp_index = sha3_content[-64:]

                    if layer not in SHA3dic:
                        SHA3dic[layer] = {}
                    if mp_index not in SHA3dic[layer]:
                        SHA3dic[layer][mp_index] = {}
                    SHA3dic[layer][mp_index][mp_addr] = keccak

                if log_type == 'SSTORE':
                    layer = txstack[-1]
                    if layer == 'ept':
                        continue
                    s_keccak = opcode['log_keccak']
                    log_prevalue = int(opcode['log_prevalue'])
                    log_value = int(opcode['log_value'])  #十进制
                    #balance = log_value - log_prevalue

                    if layer not in SSTORE:
                        SSTORE[layer] = {}
                    #当和app event对比的时候，app关系的是log_value。当和transevent对比的时候，关心的是value-prevalue的差值。还是记录第一个pre和最后一个value
                    if s_keccak not in SSTORE[layer]:
                        SSTORE[layer][s_keccak] = (log_prevalue, log_value)
                    else:
                        oldpre = SSTORE[layer][s_keccak][0]
                        SSTORE[layer][s_keccak] = (oldpre, log_value)

            if break_flag == 1:
                del USEMAP[usecount]
                continue

            #开始匹配allow内容,删掉失效层的记录，删掉没有抓到map的sc的那一层的记录。这里的问题是，如果某一层没有sha3,并且还失效了，那其实应该跳过的。
            for ly in SHA3dic:
                if ly not in SSTORE:#这里指的是层数，如果这一层没有sstore那肯定啥也匹配不上
                    continue
                if ly in Invalid_Layer:
                    continue
                if ly not in LayerSC:   #理论上不该出现这个情况
                    print('layerror')
                    print(txhash+filename)
                    continue
                ly_contract = LayerSC[ly]
                if ly_contract not in ALLOWMAP:
                    continue
                ly_index = ALLOWMAP[ly_contract]
                if ly_index not in SHA3dic[ly]:#这里就不需要删掉USEMAP的记录了，因为到了这理论上是有可能只有event没有map的错误出现。
                    continue

                for ad1 in SHA3dic[ly][ly_index]:
                    ad1_keccak = SHA3dic[ly][ly_index][ad1]
                    if ad1_keccak not in SHA3dic[ly]:
                        continue
                    else:
                        for ad in SHA3dic[ly][ad1_keccak]:#这里还真的出现了问题，就是同一个from.来了两个to地址。
                            ad2 = ad
                            ad2_keccak = SHA3dic[ly][ad1_keccak][ad2]
                            if ad2_keccak not in SSTORE[ly]:
                                continue
                            else:
                                sstp = SSTORE[ly][ad2_keccak]#可以记录了
                                pre = sstp[0]
                                nowvalue = sstp[1]
                                usemaptp = (ad1, ad2, pre, nowvalue)
                                nowlayer = 'lay'+str(ly)
                                if nowlayer not in USEMAP[usecount]:
                                    USEMAP[usecount][nowlayer] = {}
                                if 'maplog' not in USEMAP[usecount][nowlayer]:
                                    USEMAP[usecount][nowlayer]['maplog'] = []
                                USEMAP[usecount][nowlayer]['maplog'].append(usemaptp)

            #删掉error层内容
            for key in Invalid_Layer:
                inv_layer = 'lay'+str(key)
                if inv_layer not in USEMAP[usecount]:#存在这种问题：某一层啥内容都没有，是空的。所以这一层没有记录。因此这里需要continue
                    continue
                del USEMAP[usecount][inv_layer]

            #加一条，去掉没有allowed的只有transfer event记录的那层
            uselist = list(USEMAP[usecount].keys())
            for key2 in uselist:
                if key2 == 'log_txhash' or key2 =='log_block' or key2 == 'log_time':
                    continue
                if 'maplog' not in USEMAP[usecount][key2] and 'app_event' not in USEMAP[usecount][key2]:
                    del USEMAP[usecount][key2]

            #最后加每一层的contract信息,假如这个contract并没有捕捉mapindex,删掉
            uselist2 = list(USEMAP[usecount].keys())
            for key3 in uselist2:
                if key3 == 'log_txhash' or key3 =='log_block' or key3 == 'log_time':
                    continue
                layinfo = int(key3[3:])
                nowcontract = LayerSC[layinfo]
                if nowcontract not in ALLOWMAP:
                    del USEMAP[usecount][key3]
                else:
                    USEMAP[usecount][key3]['log_sc'] = nowcontract

            if len(USEMAP[usecount]) == 3:
                del USEMAP[usecount]

        if len(USEMAP) >= 5000:
            wcount += 1
            wname = 'usemap'+str(wcount)
            with open(usemap_path+wname, 'a') as f4:
                for key in USEMAP:
                    f4.write(str(key)+'#'+str(USEMAP[key])+'\n')
            USEMAP.clear()

# #test
# datalog_path = 'F:/BC/WWW/data/testfile_10/'
# ALLOWMAP['c3951d77737733174152532e8b0f27e2c4e9f0dc'] = '0000000000000000000000000000000000000000000000000000000000000005'
# usemap('a918a9a97a7768c7d8048e4e19fa6d8dec49611d1449662388c1cfce64a798eb')
# exit()
# #test


#入口
count = 0
with open(order_file, 'r') as f1:
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
            usemap(filename)
        except:
            print('error')
            with open(error_path+'error1.txt', 'a') as f3:
                f3.write(filename+'\n')

#末尾结果记录
wcount += 1
wname = 'usemap'+str(wcount)
with open(usemap_path+wname, 'a') as f4:
    for key in USEMAP:
        f4.write(str(key)+'#'+str(USEMAP[key])+'\n')
