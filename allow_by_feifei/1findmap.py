# _*_ coding:utf-8 _*_
#需求：寻找双层mapping allowed。第一步，定位mapindex
#标记（凡是标记部分，正式跑之前都要删掉）：test；loc/服务器;

import ujson
import datetime
starttime = datetime.datetime.now()

# loc path
order_file = '/media/yulele/HardDisk10TB/tutu/order_646'
datalog_path = '/media/yulele/HardDisk10TB/www/syncssd/newdatalog/'
# order_file = 'F:/BC/WWW/data/other-100/ordered_filename_time_blocknumber_100.txt'
# datalog_path = 'F:/BC/WWW/data/other-100/100_data_1/'
findmap_path = '/media/yulele/HardDisk10TB/tutu/allow_map/findmap/'#result
error_path = 'media/yulele/HardDisk10TB/tutu/error/'

# #服务器路径-zihao
# order_file = './order5W'
# datalog_path = '/media/HardDisk4T/movedatalog/'
# findmap_path = './findmap/'#result
# error_path = './error/round1/'
#
# #服务器路径-chenting
# order_file = './order7W'
# datalog_path = '/media/yulele/HardDisk10TB/www/syncdata/syncdatalog/'
# findmap_path = './findmap/'#result
# error_path = './error/round1/'

#建立Transfer和Approval的字典
transfer_hash = {'2c4d9d1041355b152e80b28195d8cd57a1363203c2b1a39c0559f0e757747d5c': 'uint8', '89896edbd223c9360ce42ddfed7522a2bffb20c056e4c42d42370cb493b65676': 'uint16', '4c3f23e06500a14887485511327c0d579fbccac302d5839c043bcc62bf867793': 'uint24', '0daf680c3f528a8760b5142fe1f6f80d5f4ea18bb76f347a7a44a2d565c2b7dc': 'uint32', 'cdabd7cd7a44bd50521a39c666b076577c82465c3615f66391d096cc719c6ac0': 'uint40', 'e18706cb56ac477fbc72c6acbbd512822f259c1f09006247dbae41d881bc3e17': 'uint48', 'f0cd1a5c0ee7db84a3a9327b544161b199d1a1088d6dd1c99d42646432eaf9fb': 'uint56', '831ac82b07fb396dafef0077cea6e002235d88e63f35cbd5df2c065107f1e74a': 'uint64', 'bff91d4903077cc645099227f3ff63fa8f7c4e51de89afbefde6b29eb549af87': 'uint72', 'a0f2d9d810b7227d93b1d65511f1321d5331a7a323e6d357130dda4aa99690a0': 'uint80', '1c232f833daad9ed1224c5770c053a18edfef5d85918dede55acc1da05ab6c8b': 'uint88', 'ba7196a4bdbfed2416fed23830b5c875c6e32d81744212e9776f7d2b02a33188': 'uint96', '18b3a374e2313c602fb9e4002182a9b948dff0294feab6f98f5e7e4334ef7e9d': 'uint104', 'b7ac3c4762d5a753158c22506d7f1a1373c52dae6059cc91115338581b05e27c': 'uint112', '91925c49b49f6ee4ac0d966d8d2e700e489f031bf933396b5b64bc584529d229': 'uint120', '27772adc63db07aae765b71eb2b533064fa781bd57457e1b138592d8198d0959': 'uint128', '46518209995f34a01926b792690bc92e5037b070563bfdacd84fafd40b513eb5': 'uint136', 'e8032327ba5bd636272f39d92559de88e80732a9d637d0b6752d51281150d4b7': 'uint144', '48c4fa90124ada7723a851f5a30fc80851bbfab1f12649e3ae71a32c627720cd': 'uint152', 'df5c409937706803ae64d124b48586638c7b50733b40fb16cff8141ffa1e0af8': 'uint160', 'd0966ead8911bd02ec5119ed64d10236cb4fd8f29c5001afb73d60689cf88b20': 'uint168', 'b18cf775c754b8fae1157af9b1f2b93496f6bf0cd582c24d7175692fcaa1cd21': 'uint176', 'fcdacb06893591fedb6582b761d2e964d37a4e7f77a844e3a05c5fbf47797c0e': 'uint184', '74c9ae5ff92efee44f316c09cbdbdebb254705f4fd59514ed2d87e1e3da93913': 'uint192', '7344fa9abcab6b3790a118567725311a6bfb30957589e825e4300bce8f3fb020': 'uint200', 'bae695334f1401f46a8c246fb4e028ccdee498d6cd47ddb5683ab940d25fbdc5': 'uint208', '3fb8d49d89b30c4ee5141c3d10e5bb70e95d5babd584e3000107d2dac22a826a': 'uint216', '354cd84171949f23d6c7393b4deca6b9670954625ffedcb35a250a15a08515ed': 'uint224', 'cf73f4a4f977af3327646216f7d3af8970de9bc70aeaf76009cec99dcf46c786': 'uint232', 'c2ac9a11e79ddfc35c6403b568c9d85957090c8416d338be90299141f1e7f425': 'uint240', 'fe28b6744e16875301806797283f9bcc1a29b15f700c0e088645e2c257eec1e5': 'uint248', 'ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef': 'uint256', 'fdb0d9db4fcfa99a69bab4019cf42ab495be117bb60275b901645c28ca3deef4': 'int8', '1306f300bdf23ef00b1fe00644eee04b9576ad8c68837bffa5158e4693ea296a': 'int16', '1315fe0300efd5bde69c874d107401124940c3cdb534666230a2436a47e6a49b': 'int24', 'b659f7922125405e40eb1a5fbfd9879f3d296b8200019be90f730b459f9f1c25': 'int32', 'b76456965aa890ee11746d3b26582281ffca539801841abe6282ab73b2c01993': 'int40', 'fd0e41a48c016debc0ec3c87cdf02ba5e2eb2db4587292c6bdcec7bda1fc3d3c': 'int48', 'bc87650eb8e9c481db3f2576aea1b4e653894d93b7f6cb6a190717a1fca3a319': 'int56', 'cef55929759435389feb62e3ad30d90911d061d3eb8f8e3ead60622531745cc1': 'int64', '19b40000025b47ecd4d2940168402cfe9317418307f848216988dc028e628214': 'int72', 'e670604a3a027fa22059b623a5b0ae38424829237d769b02282dc7d81fb06426': 'int80', '303dc7e5a79ee0ca02c3f06db0502fbfe7a964cd8fa597919e4376f6dbc1e157': 'int88', '0ed1306281e9b4c9d018e1291d83fd014895d20c95da608569e7d9a5361117aa': 'int96', 'a87ac4316a9088110eb185cf27691b5533890444b36f2712b700fe09a5e53ba7': 'int104', '2c5825beae12151d954009ae7f95e998300458d351c8fc8e6d2df9a8753d65a7': 'int112', 'e64efe620012ecf67a6a08208071cfd55ea85c641860fa711388c041c80d72f6': 'int120', '9ce147531995c591b0b50012b20f7f6d0dea75281159a58b8637542388f14626': 'int128', 'e86307cdc23d5574d14f14c07d08814d980276c4b92d6d51e6f6497a807607c8': 'int136', 'a099bc2413531106e46903e9bd7f34d43b6d124631398348d1d5f368baeb8032': 'int144', '467c5dc3035b08b8eda1206c6049fd8eb86db17119be0ca51d0de6f99bf7f548': 'int152', '8d1591cfd32ad19c215c6295623aea4eec85442fc5c4601cda6f7e0a038186ba': 'int160', '4ec3ba770fb8428f5ce8590bc4b28663359570e0193206f9364399c06e768241': 'int168', '7f02f13368f9b374a15f81ad02096044b4c26fa5127a1fa37aeed8e392bd6edd': 'int176', '6e348e9e7927772dff9da0764845053058a54199928284bfe6decb7ac09d40d7': 'int184', 'a88a4735393a2bbb1c23c083874e1d0636d3e87851b6f20a6d2115f5ea540ba0': 'int192', '96a6ed04a9960ed29f91a03141a1256a7e6204eb90c319d76a91ec4aa02bbc2f': 'int200', 'cbab2a67020e790d89db09e426191c44c8c05d9f93dc1f8cc32dda14929f40e5': 'int208', '7c11167a36b8ef38fc546598e268c0964bb2cb21377e6cb80e217bcb6ecb8c67': 'int216', 'f238e8301c28c0dac41fcc9bd2e2d659096a02384c2ffd9b1430ac584c95691e': 'int224', 'd6e7a41c23f4209ee7bed2dbe1d4774884aaf836b11d0c93a84b8eb44878dbd3': 'int232', '81031c58ed866f2ba7f5ac8c702cedc31ed6b4a08cd1d540c988018b0ca5b845': 'int240', '8695741cd0cb852f381bcfad35ffa6af9b0f4d1634247d0b2589ad84233dc590': 'int248', '8b0c34a52f9e28d78caaa7066cd047b398dae74941a208b77777420f492bd7e1': 'int256'}
approval_hash = {'611d0801b9a936d7e62d45aa93e967f00a929991de32d84517019e3dcf9eef5d': 'uint8', '0a9d294fd4bd42bb30e96cba2b478d149a783fba3c729b1e5c42bec89d95b85a': 'uint16', 'b3ba96ffca58a5c0843f7fa57ac208298b3b86e7feed3d33a9f706270c2626e9': 'uint24', 'e26b9b29b95cb706aaebdd86a3524de879b8590b0ba7e61b104f54196bab2031': 'uint32', '4c3c5c1dcab266f9cbc926f6e78bcd8f584e9dc3d081f3fcc0e7d78958a86369': 'uint40', '4796d4e837f21da69df41f03f3e0a8d62bf832a6392dc107c5e4ab6162fc34f9': 'uint48', '4ed3c7595630c834d0daa2ff368f18fe007667949f4b54b1e191af11c61b6ad7': 'uint56', '16304dfea7f3fbabcf59225f0629cb307fecb8d5652b069080aa9be2c765d7d2': 'uint64', '2318f7d28490f7cee21d53e90848ad9cb2ddc35468fee892b94294a8ba3f28c4': 'uint72', '3212f41ec92f177d999db7467a64faeb241827d867f4f176dc2be61581122d1a': 'uint80', '9e7c8d7ae45ef86759782f7bebc2eb949dfb477bec28976151ae39c2999509f3': 'uint88', '19ed2b70d0b204384ff1671abf69ee2e07332f5827fb8ef9eaccefd3c4fd84f6': 'uint96', 'ac4baab1a1c0abe1ef1a20d8b649aeec8e1d58fd87cea8dead3290994d4abbc7': 'uint104', '2c2717f8c0c9abadb94086901ff3a5e3c416e2735086be753e96912ddd05cf58': 'uint112', 'bdd455a9c6236e658d0ef088cb976eda861c5a5ae1c6cd7f3cced3f40b4cdbf4': 'uint120', '444360fd9f99263247bc59eb6f6c9f5d7f1096ba7962aa22cb94c3f5b743eded': 'uint128', '4cbd576684a0d88e1eda10cdba47dbecbbcbb4d189e93e26d5d4e380f978d618': 'uint136', '2589c40a575d794a67d5a80b470a7781a46bfc7b8366a306c614e4cc2f4f422c': 'uint144', 'fd5dd4bbb12e80230ca445967fe3c2bc44df0f2855264f70db91e36eb79bf149': 'uint152', '621afae5277bf1254bd37441bf7675038b2d92e67e36528d50ece5edd980f66c': 'uint160', '40f6e77ac39abbf03c972224330b0ba8141e027d7e897417dbad3a0fb8f1e05b': 'uint168', 'c11ab962196b359249cad722175c1b5bf5cb11978203ff6d024d94376db7f53e': 'uint176', 'dea3fc7d6bda2134fdd0a80a5048a8e18a21123ab7602a96e6acafa6a71c0882': 'uint184', '28b2637e74d43adce90ce8a563f56362d98649573b41067d7c9791d27d172572': 'uint192', 'ae90dba1fd8e9c6d13db5e2b121ee33a4f8f00c08acd401a69a24c3a6ae961f2': 'uint200', '99315e87058049e818e24b3b1a3df7997e1aaedfccf2fbf0ef91d40e27ff7fd8': 'uint208', '7aac39111fb107ed22b8f218f5f9875ca36c89fa77d3d0d04671b73fa7a94de2': 'uint216', 'b9244d497d09501d52dac5a497c9984c496446e94a9d0b25b81d6e4c745a9937': 'uint224', 'fa1549e4470b16217f1640a3d9b9256ade6f391093ad06d7f3623110ffc9034b': 'uint232', 'a10a7a77144cd5dc9e7b671f64747886004404bd02e5793fd42795b80129f13f': 'uint240', 'e3e78edbddaa50bbc62ae668141bad4163a767a486bb9dc900ae35760a867202': 'uint248', '8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925': 'uint256', '1947fcfd1c8eae160c7ca1c8affe63589686ecdbb87a258806510501e488f480': 'int8', '37d66f019b45f660b9261b17e835866b935da926f56881ed8d74331b2e37b658': 'int16', 'e1812197073582e52673fcebab69b805a362d9a897ea9403e1d9e1c95997d0f0': 'int24', 'd7dc3a93fb6f3edcfa2cf33339b05f153f5ed077e3e345e60dd896d2e601e076': 'int32', '2f5b2046f7a840ce2f195bb06b361bf0d3b926bcdbad64b3d9c4044515c2348d': 'int40', '42b630f4dfe0ad7dd2c36d0932e6854307de3cff90496ac90ea1ed2a4562c4ed': 'int48', 'cecffb51bbd45f2f3b09fb2301afda04849e6f646ab97d90017f0c35a83ff29c': 'int56', '61df88c5062f70a3a49980efd761a155cabdf187e1cace20a98f85655ccdbac7': 'int64', 'eeacb6c03f31f9b6752cdedbfb0042fde0d2e00bd500d92d7e14503daa1fb208': 'int72', 'ab5b01ad1163a3cc4a5112cb4ae1335ab2f2ed8d8fb9a6fb8d39e1edb64eaacc': 'int80', 'b36c77c1f139a72ae511f910ea7b927ed5b366ff739e080846bc3d5d74493a69': 'int88', 'ca9055347a5ffd54d7d7e53f2cce0bb71812b5d0409558db343759583efe43b3': 'int96', 'df8dbb8d1c42cf6fdacf3c02e0b36be64fd74616cf8114866d55b898f4504349': 'int104', 'd77a66b5574966f4d3af1bf1f62250f66cfbd0c7a0564c2864fcfb594e41cc81': 'int112', '3a51815283643d21deed182a2871dcb3a674ce6e97f66abd3209b1763841d03d': 'int120', '62b2917683ac3406e3d9cfb4e95a047ae041fc4928b2b723e50cbaa04cca6216': 'int128', 'bc9e8fbdec1db655e7143c5a13848d9db39d701780345ae5cc9fe8c2e55d89d6': 'int136', '24a99c930a2787abb8ffbdcc6d1db5a44e9510f65fd1caa3928422cedfb7deb8': 'int144', 'be5d5a4d573fe6be806e178742dfd1e545f4e989efdfea48e520f4ad5a159975': 'int152', '0db6498167d89be3bfc62869d54b215d17ded3c55ba6d8abec7a00c399b688c0': 'int160', 'db29719e85079ee8dd509f9f95b2728a5842a2237e1bdd959264914b24f5df74': 'int168', '82cece37c7ba2bb254ea82dd96052d1c9f433c5c874019f6836c543acde81255': 'int176', 'f82536e2b93ffe7001f1bec1e1e4a223fa0bcb2c4ae0294b7e155e6c0e98bc89': 'int184', '12fd8185e5fefef133399d8d789f6f3db6cd6ea4c078dcb017105e8d2ce2556f': 'int192', 'fbdde4d2695291e10a7d05a942cbdf8336d27075cc428054d8234d596d77b7f0': 'int200', 'e85f62a051ae1b89e66d58f9c0cfa9282c4c732d37c1838e9217b7daf64e4534': 'int208', '0ac87ee9a1d376d59e62fac27da795fc55d3e9b88a8215f6d383e877280a20c4': 'int216', '4aee8d2b10ca88e143a1acc8dc445b35f3447f24cf7ca4066c846f0493ce8823': 'int224', 'c38731ddbb1d7560eee4fbe184a38a1e68e8b97190736138b9e219ed213c2562': 'int232', '2eb19f930d15a26a73aca8a321ac079f65469c955849067d916f30078ab8d21c': 'int240', '4ce85f62f0c56e3f407acc809bf5ab8260d71814a63300d1699142229cc96dd0': 'int248', 'ec06647eb3d581d530bd6914e5c859db8edbc5bfb6bffa5d4cf720b824295e0a': 'int256'}

#记录最终结果的全局字典：
ALLOWED = {}#contract-index-time
wcount = 0


#解析trace
def analy_trace(filename):
    global ALLOWED
    global wcount

    with open(datalog_path+filename, 'r') as f2:
        for line2 in f2:
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
            #记录两种event和sha3和sstore
            APPevent = {}
            Transevent = {}
            SHA3dic = {}
            SSTORE = {}
            Tmatch = {}

            #开始解析
            trace = ujson.loads(line2)
            txhash = eval(trace['LOG_txhash'])  #type str
            # blocknumber = eval(trace['LOG_blocknumber'])  #type str
            # time = eval(trace['LOG_timestamp'])  #type str
            #
            # #test
            # if txhash != 'd09f7389bb2ca1f47d6e485a32d446766078c7fbf3359b73c3b9f1a141ca8d0e':
            #     continue

            #opcode
            opinfos = list(eval(trace['LOG_opinfos']))
            for op in opinfos:
                opcode = eval(op)   #type dic
                log_type = opcode['log_type']

                '''
                最重要的是，这个里面的每一个log也是按顺序来的，一定要注意次序。
                整个代码的功能模块从这里开始分割；
                首先，维护栈和判断error是用到了 call,callend,create,createend，以及新增的create addr啥的；
                第二，利用LOGX来提取transfer approval两个event
                第三，利用sha3，sstore来进行map记录
                最后，将第二步和第三步的记录进行匹配，定位到allowed。调用函数matchmap
                '''

                '''
                关于error：由于error字段是在这一层的末尾，相当于是分析完了之后，发现了error,那就回滚这一层的操作。
                这个功能要如何实现呢？
                在判断mapping的时候，这个error跳过的意义不大，顶多会造成一些干扰。只是利用mapping进行数据解析的时候，对结果影响大。
                暂且搁置
                思路，如果这里不用for而是用range或者while,就可以指定访问哪一个，比如我到了callend,那么i+1就是下一个紧接着的json，就可以判断是不是失效的。但是还是不知如何回滚
                一个想法：如果遇到了error字段，那么就认为刚刚pop出去的那一层是无效的，那么无效层的内容就不做匹配。直接清空。
                '''

                #这里完全出错，需要poplayer，因为她有可能是 1 2 4 6这样的栈结构，并不是入一层出一层的。
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
                    if create_addr_flag == 0 and layer != 1:
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
                        #create_error_flag = 0

                if log_type == 'CREATE_F' or log_type == 'CREATE_R':
                    if create_error_flag == 0:
                        continue
                    elif create_error_flag == 1:
                        create_error_flag = 0
                        #create_addr_flag = 0
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

                        #进行存储。存储结构是为了便于后续的匹配。起码要包括层数信息。分成transfer和approval两种去记录；approval不需要合并。并且应该不会有重复。
                        if topic0 in transfer_hash:#这里进行叠加。同一层，key是msg.sender,是同一个人，from则可以改变。所以其实层数已经可以唯一标识这个allowed的key2了，不必验证具体的key2是谁。然后只需要用layer和from的tp就可以确定。
                            transtp = (layer, fromaddr)
                            if transtp not in Transevent:
                                Transevent[transtp] = 0
                            Transevent[transtp] -= inputdata

                        elif topic0 in approval_hash:#这里按照（层数，ad1,ad2,input）作为一个key存成字典，value可以是出现的次数，这样匹配出来一个双层的时候，做同样的key去查找就可以；
                            apptp = (layer, fromaddr, toaddr, inputdata)
                            # if apptp not in APPevent:
                            #     APPevent[apptp] = 0
                            APPevent[apptp] = 0

                '''
                这里不能遇到一个sstore就往回找，因为这里存在一个问题就是，你不知道当from分两次扣费的时候，allowed是分几次。所以每一层，需要合并。因此必须按照层数去记录
                问题来了。这个记录方式应该如何呢？
                第一个问题，如何找双层字典。
                第二个问题，如何记录才能把同一层的字典结果合并。approval不需要合并。所以可以直接查找
                '''
                #sha3+sstore找双层字典。
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

                    #这里到底怎么存，需要再考虑
                    sha3tp = (layer, keccak)
                    SHA3dic[sha3tp] = (mp_addr, mp_index)

                if log_type == 'SSTORE':
                    layer = txstack[-1]
                    if layer == 'ept':
                        continue
                    s_keccak = opcode['log_keccak']
                    log_prevalue = int(opcode['log_prevalue'])
                    log_value = int(opcode['log_value'])  #十进制
                    #balance = log_value - log_prevalue
                    ssttp = (layer, s_keccak)
                    if ssttp not in SSTORE:#有问题，如果出现这种，from地址分开扣了两次钱的情况，那么我们关心的是，最开始的prevalue，和最后的value
                        SSTORE[ssttp] = (log_prevalue, log_value)
                    else:
                        old_prevalue = SSTORE[ssttp][0]
                        SSTORE[ssttp] = (old_prevalue, log_value)

            if break_flag == 1:
                continue
            '''
            这里是对整个交易的event和map进行匹配。
            sha3解析出来的东西，是ad1,ad2,value,即allowed[ad1][ad2] = value。这里的value如果是app,差值为正数（这里出错了，可以是负数。并且approval直接赋值，不取差值）；如果是transfer，差值为负数
            有两种：
            第一种是第一次设置approval时候，value和app的事件内容直接匹配。这里应该也是差值的。
            app事件中，记录的依次是，ad1,ad2,value
            第二种是transferfrom发生的时候，交易额度和transfer匹配上。
            transfer事件中，记录的依次是，ad1,无关内容，value。问题来了，ad2的msg.sender怎么得到？（层数唯一确定它）假如是内部交易，msg.sender是上一层栈顶的合约；外部就需要额外提供了。
            
            匹配方式：
            当sstore的value-prevalue差值为正的时候，匹配app，为负匹配transferfrom的event；
            当某个balance匹配上了，然后拿到这个balance被sstore时候的offset，找到对应的sha3进行解析，得到内层的offset和ad2.匹配ad2是否一致。
            如果ad2一致，就去解析内层offset得到index和ad1.如果ad1也匹配。就说明可行。
            app:匹配他的tp是否存在
            trans:匹配叠加后的key-value是否一致。
            '''

            #寻找双层字典：sha3+sstore
            for stp in SSTORE:
                if stp not in SHA3dic:
                    continue
                stp_layer = stp[0]
                if stp_layer in Invalid_Layer:
                    continue
                inner_keccak = SHA3dic[stp][1]
                inner_tp = (stp_layer, inner_keccak)
                if inner_tp in SHA3dic:#说明是双层字典，记录他的，mapindex,ad1,ad2,value
                    mapindex = SHA3dic[inner_tp][1]
                    mapaddr1 = SHA3dic[inner_tp][0]
                    mapaddr2 = SHA3dic[stp][0]
                    mapprevalue = SSTORE[stp][0]
                    mapvalue = SSTORE[stp][1]
                    balance = mapvalue - mapprevalue

                    #最大的问题：如果是approval的sstore，那么allowed是直接赋值的，不需要取差值,不是的，可以修改，会产生差值，但是event只通知修改完的最终值；如果是transferfrom的，那就需要取差值。
                    '''
                    这里是否存在balance一样的index的问题呢？
                    index出现的原因是因为from和to分别要匹配上event,但是有可能来自不同index的被匹配上。allow里面：
                    approval默认不会出现重复，所以不需要分开，直接用关键信息存为tp即可.from to都有，应该不会出错
                    transfer里面，有可能from地址会进行两次扣钱，allow不知道会不会有两次，但是event会出现两次，所以还是应该叠加。现在event对于同一个from的进行了叠加，sstore对同一个地址进行了叠加
                    '''
                    #双层字典和event匹配，查看是否是allowed
                    #和app匹配
                    maptp = (stp_layer, mapaddr1, mapaddr2, mapvalue)
                    if maptp in APPevent:#找到了一个，根据层数，拿到对应的合约地址；然后记录mapindex.这个记录要靠全局变量
                        #记录mapindex
                        mapsc = LayerSC[stp_layer]
                        if mapsc not in ALLOWED:
                            ALLOWED[mapsc] = {}
                        if mapindex not in ALLOWED[mapsc]:
                            ALLOWED[mapsc][mapindex] = 0
                        ALLOWED[mapsc][mapindex] += 1


                    '''
                    这里的问题，如果是和transferfrom匹配。那么，add1 = from, addr2 = msg.sender。现在我们无法得知msg.sender，也就无法确定add2
                    在这里就会出纰漏，如果说。有一种双层字典，他的ad2不是msg.sender，出现了好几个ad2，那么keccak第二次就会不同，相当于同一个from地址的value不能叠加。
                    如此一来，和event匹配就失去了叠加的意义。也就是说，sstore存储的keccak,是包含了ad1+ad2两种信息的，如此一来，其实当匹配到双层字典的时候，应该给from叠加一次
                    '''
                    #和transfer匹配。这里不会出问题，虽然是按照层数+from。但是同一层addr2都是msg.sender,同一个人。没毛病.在这一步忘了记录Index而已。
                    maptp2 = (stp_layer, mapaddr1)
                    strmaptp2 = str(maptp2)+'#'+str(mapindex)
                    if strmaptp2 not in Tmatch:
                        Tmatch[strmaptp2] = 0
                    Tmatch[strmaptp2] += balance

            for key in Tmatch:
                b = key.split('#')
                mtp2 = eval(b[0])
                mapindex2 = b[1]
                if mtp2 in Transevent and Transevent[mtp2] == Tmatch[key]:
                    stp_layer2 = mtp2[0]
                    mapsc2 = LayerSC[stp_layer2]
                    if mapsc2 not in ALLOWED:
                        ALLOWED[mapsc2] = {}
                    if mapindex2 not in ALLOWED[mapsc2]:
                        ALLOWED[mapsc2][mapindex2] = 0
                    ALLOWED[mapsc2][mapindex2] += 1

        if len(ALLOWED) > 5000:
            wcount += 1
            wname = 'allowmap'+str(wcount)
            with open(findmap_path+wname, 'a') as f4:
                for key in ALLOWED:
                    f4.write(str(key)+'#'+str(ALLOWED[key])+'\n')
            ALLOWED.clear()

# #test
# datalog_path = 'F:/BC/WWW/data/testfile_10/'
# analy_trace('a918a9a97a7768c7d8048e4e19fa6d8dec49611d1449662388c1cfce64a798eb')
# exit()

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
            analy_trace(filename)
        except:
            print('error')
            with open(error_path+'error1.txt', 'a') as f3:
                f3.write(filename+'\n')

# 末尾结果记录
wcount += 1
wname = 'allowmap'+str(wcount)
with open(findmap_path+wname, 'a') as f4:
    for key in ALLOWED:
        f4.write(str(key)+'#'+str(ALLOWED[key])+'\n')

endtime = datetime.datetime.now()
print(endtime - starttime)

'''
一些意外情况：
1.文件名：2b5be71a7e9cd1cb704b83aa08ebd7ce1c804c1154b86f584764c7ba7ca12539
哈希：6ee36404efeee7a6a2cafa7160da9300a54e56ee06f3f97f61b73162d4123529
问题：该交易fail掉了，但是并没有outi。中间的第二层call也没有call_f
同理去检查了call_f的情况，发现当第一个action revert的时候，并没有记录outi。
我发现，有的create_f是有outi的，比如fe0e963212f7facd642b18c74e12b60d24a14c213878851c180f8bf9aeb823a9；进去看了下出错代码是bad instruction；应该就是没抓到revert
'''
