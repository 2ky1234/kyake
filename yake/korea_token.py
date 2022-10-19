import os
from konlpy.tag import Komoran
komoran = Komoran()

def split_sentences(text):
    text_value = []

    from regex import compile, DOTALL, UNICODE, VERBOSE
    _compile = lambda count: compile(SEGMENTER_REGEX.format(count), UNICODE | VERBOSE)
    SENTENCE_TERMINALS = '.!?\u203C\u203D\u2047\u2048\u2049\u3002' \
                        '\uFE52\uFE57\uFF01\uFF0E\uFF1F\uFF61'
    "The list of valid Unicode sentence terminal characters."
    SEGMENTER_REGEX = r"""
    (                       # A sentence ends at one of two sequences:
        [%s]                # Either, a sequence starting with a sentence terminal,
        [\'\u2019\"\u201D]? # an optional right quote,
        [\]\)]*             # optional closing brackets and
        \s+                 # a sequence of required spaces.
    |                       # Otherwise,
        \n{{{},}}           # a sentence also terminates at [consecutive] newlines.
    )""" % SENTENCE_TERMINALS
    #SHORT_SENTENCE_LENGTH = 55
    #short_sentence_length = SHORT_SENTENCE_LENGTH
    "Length of either sentence fragment inside brackets to assume the fragment is not its own sentence."
    # Define that two or more line-breaks split sentences:
    MAY_CROSS_ONE_LINE = _compile(2)
    "A segmentation pattern where two or more newline chars also terminate sentences."
    # This can be increased/decreased to heighten/lower the likelihood of splits inside brackets.


    for s in MAY_CROSS_ONE_LINE.split(text):
        if len(s.strip()) > 1:
            text_value.append(s.split(' '))

    
    return text_value

def split_multi(text):
    # stopword.txt 읽어오기 위한 path 및 파일이름
    language = 'ko'
    path = 'C:/Users/BIG-LGY/Documents/GitHub/pke_u/yake_korea_ver/yake/StopwordsList/'
    txt = '/stopwords_{}.txt'.format(language)

    try:
        f = open(path + txt, encoding='UTF-8')
        ExistStopwords = set(f.read().split())
    except FileNotFoundError:
        ExistStopwords = [None]

    ExistStopwords = list(ExistStopwords)
    f.close()

    # text_list = text.split()

    SpecialToken = r"""#"$%&'‘“()*+,-/:;<=>[\]^_`{|}~"""
    exclude = set(SpecialToken)
    # list로 주어지면 합쳐서 str 문자열로 전환 함수
    def list2str(TokenList):
        NewTokenList = []
        
        if type(TokenList) is list:
            NewTokenList = ' '.join(str(x) for x in TokenList)

        return NewTokenList

    # 특수문자 제거 함수
    def str2token(TokenList):
        NewTokenList = []

        for i in TokenList:
            if i in exclude:
                TokenList = TokenList.replace(i, ' ')

        NewTokenList = TokenList.split()
        return NewTokenList

    # 입력받은 text 형태에 따라
    if type(text) is not str:
        token_list = list2str(text)
    elif type(text) is str:
        token_list = text

    token_list = str2token(token_list)
    token_list = ' '.join(token_list)
    text_list = token_list.split()

    # 조사 제거
    def deljosa(word:str):
        '''
        한국어 조사와 어말어미의 출현빈도 조사
        상위 70개 통합 조사의 상대적 출현빈도
        KT Data Set 99.8% 커버 조사
        '''
        if word[-4:] in ['으로부터',"으로서의"]:
            return word[:-4]
        elif word[-3:] in ['에서는','으로써','에서의','로부터','으로는',
                        "에서도","까지의","이라는","으로의","이라고"
                        ,"보다는","로서의","만으로"]:
            return word[:-3]
        elif word[-2:] in ['으로','에서','하고','이다','과를','보다','에는'
                        ,'이나','로서','에게','까지','과는','만을',"대로"
                        ,"이고","에도","과의","로의","이며","로써","로는"
                        ,"만이","와의","마다","와는","이라","에만","라고"
                        ,"처럼","부터","로도",'토록']:
            return word[:-2]
        elif word[-1:] in ['을',"의","를","에","은","이","는","과","로","가"
                        ,"와","고","여","도","다","든","라","나","만","며"
                        ,"께","요"]:
            return word[:-1]
        #print( word[:-3])
        return word


    def split_text(text):
        nano = []
        isstopword = []

        for i in text_list:    
            # 1. N + N
            if komoran.pos(i)[0][1] in ['NNG','NNP','NNB','NR','NP']:
                if len(komoran.pos(i))>1 and komoran.pos(i)[1][1] in ['NNG','NNP','NNB','NR','NP']:
                    nano.append(komoran.pos(i)[0][0] + komoran.pos(i)[1][0])
                else :
                    nano.append(komoran.pos(i)[0][0])

            # 2. V + XSV
            elif komoran.pos(i)[0][1] in ['VV', 'VA', 'VX', 'VC', 'XR']:
                if len(komoran.pos(i))>1 and komoran.pos(i)[1][1] == 'XSV':
                    nano.append(komoran.pos(i)[0][0] + komoran.pos(i)[1][0])
                else:
                    nano.append(komoran.pos(i)[0][0])
                    
            # 3. MM + N
            elif komoran.pos(i)[0][1] in ['MM']:
                if len(komoran.pos(i))>1 and komoran.pos(i)[1][1] in ['NNG','NNP','NNB','NR','NP']:
                    nano.append(komoran.pos(i)[0][0] + komoran.pos(i)[1][0])
                else:
                    nano.append(komoran.pos(i)[0][0])
                    
            # # 4. MA stopword 처리
            # elif komoran.pos(i)[0][1] in ['MAG', 'MAJ']:
            #     # print('stopword처리부분')
            #     nano.append(komoran.pos(i)[0][0])

            # 5. XPN + N, XPN + V + XSV
            elif komoran.pos(i)[0][1] == 'XPN':
                if len(komoran.pos(i))>1 and komoran.pos(i)[1][1] in ['NNG','NNP','NNB','NR','NP']:
                    nano.append(komoran.pos(i)[0][0] + komoran.pos(i)[1][0])
                elif len(komoran.pos(i))>1 and komoran.pos(i)[1][1] in ['VV', 'VA', 'VX', 'VC', 'XR']:
                    if len(komoran.pos(i))>2 and komoran.pos(i)[2][1] in ['XSV']:
                        nano.append(komoran.pos(i)[0][0] + komoran.pos(i)[1][0] + komoran.pos(i)[2][0])
                    else :
                        nano.append(komoran.pos(i)[0][0] + komoran.pos(i)[1][0])   
                else :
                    nano.append(komoran.pos(i)[0][0])
            
            # 6. XR + XSN
            elif komoran.pos(i)[0][1] == 'XR':
                if len(komoran.pos(i))>1 and komoran.pos(i)[1][1] == 'XSN':
                    nano.append(komoran.pos(i)[0][0] + komoran.pos(i)[1][0])
                else:
                    nano.append(komoran.pos(i)[0][0])

            # 7. NA가 나오면 뒤에 TOP10 조사 제거
            elif komoran.pos(i)[0][1] == 'NA':
                nano.append(deljosa(komoran.pos(i)[0][0]))

            # 8. SL,SH + N, SL,SH + V + XSV
            elif komoran.pos(i)[0][1] in ['SL', 'SH']:
                if len(komoran.pos(i))>1 and komoran.pos(i)[1][1] in ['NNG','NNP','NNB','NR','NP']:
                    nano.append(komoran.pos(i)[0][0] + komoran.pos(i)[1][0])       
                elif len(komoran.pos(i))>1 and komoran.pos(i)[1][1] in ['VV', 'VA', 'VX', 'VC', 'XR']:
                    if len(komoran.pos(i))>2 and komoran.pos(i)[2][1] in ['XSV']:
                        nano.append(komoran.pos(i)[0][0] + komoran.pos(i)[1][0] + komoran.pos(i)[2][0])
                    else :
                        nano.append(komoran.pos(i)[0][0] + komoran.pos(i)[1][0])    
                else :
                    nano.append(komoran.pos(i)[0][0])

            # 9. SN + N, SN + SW,                 SN + SF + SN, SN + SF + SN + SW, SN + SF + SN + N
            elif komoran.pos(i)[0][1] in ['SN']:
                if len(komoran.pos(i))>1 and komoran.pos(i)[1][1] in ['NNG','NNP','NNB','NR','NP']:
                    nano.append(komoran.pos(i)[0][0] + komoran.pos(i)[1][0])    
                elif len(komoran.pos(i))>1 and komoran.pos(i)[1][1] in ['SW']:
                    nano.append(komoran.pos(i)[0][0] + komoran.pos(i)[1][0])
                elif len(komoran.pos(i))>2 and komoran.pos(i)[1][1] in ['SF']:
                    if len(komoran.pos(i))>3 and komoran.pos(i)[2][1] in ['SN']:
                        if len(komoran.pos(i))>4 and komoran.pos(i)[3][1] in ['SW']:
                            nano.append(komoran.pos(i)[0][0] + komoran.pos(i)[1][0] + komoran.pos(i)[2][0] + komoran.pos(i)[3][0])
                        elif len(komoran.pos(i))>4 and komoran.pos(i)[3][1] in ['NNG','NNP','NNB','NR','NP']:
                            nano.append(komoran.pos(i)[0][0] +komoran.pos(i)[1][0] + komoran.pos(i)[2][0] + komoran.pos(i)[3][0])
                        else :
                            nano.append(komoran.pos(i)[0][0] + komoran.pos(i)[1][0] + komoran.pos(i)[2][0])
                else :
                    nano.append(komoran.pos(i)[0][0])

            # 10. stopwords
            elif komoran.pos(i)[0][1] not in ['NNG','NNP','NNB','NR','NP', 'VV', 'VA', 'VX', 'VC', 'XPN', 'XR', 'MM', 'NA', 'SL', 'SH', 'SN', 'SF', 'SP', 'SS', 'SE', 'SO', 'SW']:
                isstopword.append(komoran.pos(i)[0][0])
                nano.append(komoran.pos(i)[0][0])
            # 11. 나머지
            else :
                nano.append(komoran.pos(i)[0][0])

        # stopword 업데이트
        isstopword = list(set(isstopword))

        if os.path.exists(path + txt) == False:
            file = open(path+txt, 'w+', encoding='UTF-8')
        else:
            file = open(path+txt, 'a+', encoding='UTF-8')

        for i in isstopword:
            if i not in ExistStopwords:
                file.write(i)
                file.write('\n')

        file.close()

        return nano

    if type(text) is not str:
        token_list = list2str(text)
    elif type(text) is str:
        token_list = text

    token_list = str2token(token_list)
    token_list = ' '.join(token_list)
    token_list = split_text(token_list)

    return token_list


# # 다른 py 파일에서 import로 활용하면 OK
# new_text = split_sentences(text)

# total_value = []
# for w in range(len(new_text)):
#     total_value.append(split_multi(' '.join(new_text[w])))

# print(total_value)