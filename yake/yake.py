# -*- coding: utf-8 -*-

"""Main module."""

import string
import os
import jellyfish
from .Levenshtein import Levenshtein

#from .datarepresentation import DataCore
from .datarepresentation_korea import DataCore

def jacc_for_word(s1, s2):
    """
    Jaccard Similarity Function.
    In this source, use 2 parameter via word.
    Return value is score of Jaccard Similarity.
    """
    if type(s1) and type(s2) == str:
        set1, set2 = set(list(''.join(s1.split()))), set(list(''.join(s2.split())))
    else:
        return print("please input the string type")

    if set1 == set2:    # 동일할 경우 1
        return 1#, print("Same Sentences")

    union = set(set1).union(set(set2))  # 합집합
    # print("합집합 = ", union)
    intersection = set(set1).intersection(set(set2))    # 교집합
    # print("교집합 = ", intersection)
    jaccardScore = len(intersection)/len(union)     # 자카드 유사도
    # print("자카드 유사도 = ", jaccardScore)

    return jaccardScore

def jacc_for_paragraph(s1, s2):   # input: str, str
    """
    Jaccard Similarity Function.
    In this source, use 2 parameter via paragraph.
    Return value is score of Jaccard Similarity.
    """
    if type(s1) and type(s2) == str:
        set1, set2 = set(s1.split()), set(s2.split())
    else:
        return print("please input the string type")

    if set1 == set2:    # 동일할 경우 1
        return 1#, print("Same Sentences")

    union = set(set1).union(set(set2))  # 합집합
    # print("합집합 = ", union)
    intersection = set(set1).intersection(set(set2))    # 교집합
    # print("교집합 = ", intersection)
    jaccardScore = len(intersection)/len(union)     # 자카드 유사도
    # print("자카드 유사도 = ", jaccardScore)

    return jaccardScore

def isParagraphReDuplicated(dataset, COpy):    # input: list(tuple)
    """
    Extense from Jaccard Similarity Function.
    In this function, use 2 parameter, list and (T or F). list is composed of tuple.
    Return value is set of list composed of tuple, except duplicated things.

    When COPY parameter set True, return value will minimized.
    """

    # dataset : [ ( float, <class> ), ( float, <class> ), ...,  ( float, <class> )]
    # class   : < yake.datarepresentation_korea.composed_word object at 0x144c09940 >
    # print(resultSet[0][1].origin_terms)   :   일회용품 사용이

    if COpy is True:
        copySet = dataset.copy()
    elif COpy is not True:
        copySet = dataset

    for x in range(len(dataset)):
        if dataset[x] in copySet:
            pass

        for y in range(len(dataset)):
            if x==y:
                pass
            elif dataset[y] in copySet:
                pass
            else:
                score = jacc_for_paragraph(dataset[x][1].origin_terms, dataset[y][1].origin_terms)
                if score >= 0.5:
                    try:
                        if dataset[x][1].H > dataset[y][1].H:
                            copySet.remove(dataset[x])
                        else:
                            copySet.remove(dataset[y])
                    except ValueError:
                        pass
    return copySet


    # for x in dataset:
    #     if x not in copySet:
    #         # print("해당 문장은 이미 제거되었습니다.")
    #         pass
    #     for y in dataset:
    #         # print("기준 문장: ",x, " : ","대상 문장: ",y)
    #         if x == y:
    #             pass

    #         elif y not in copySet:
    #             # print("해당 문장은 이미 제거되었습니다.")
    #             pass

    #         else:
    #             score = jacc_for_paragraph(x[0], y[0])  # "자존심 때문이라는 분석이"
    #             if score >= 0.5:                        #       "때문이라는 분석이 나왔다."
    #                 try:                                # 두 문단의 유사도가 0.5
    #                     if x[1] > y[1]:
    #                         # print("기준 문장: ",x, " : ","대상 문장: ",y)
    #                         # print("유사도 발견.   {}   제거".format(x))
    #                         copySet.remove(x)
    #                     else:
    #                         # print("기준 문장: ",x, " : ","대상 문장: ",y)
    #                         # print("유사도 발견.   {}   제거".format(y))
    #                         copySet.remove(y)
    #                 except ValueError:
    #                     # print("이미 지워진 문장입니다. \n")
    #                     pass
    # return copySet

def isWordReDuplicated(dataset, COpy):    # input: list(tuple)
    """
    Extense from Jaccard Similarity Function.
    In this function, use 2 parameter, list and (T or F). list is composed of tuple.
    Return value is set of list composed of tuple, except duplicated things.

    When COPY parameter set True, return value will minimized.
    """

    if COpy is True:
        copySet = dataset.copy()
    elif COpy is not True:
        copySet = dataset

    for x in dataset:
        if x not in copySet:
            # print("해당 문장은 이미 제거되었습니다.")
            pass
        for y in dataset:
            # print("기준 문장: ",x, " : ","대상 문장: ",y)
            if x == y:
                pass

            elif y not in copySet:
                # print("해당 문장은 이미 제거되었습니다.")
                pass

            else:
                score = jacc_for_word(x[0], y[0])  # "자존심 때문이라는 분석이"
                if score >= 0.5:                   #       "때문이라는 분석이 나왔다."
                    try:                           # 두 문단의 유사도: 8/14 = 대략 0.57
                        if x[1] > y[1]:
                            copySet.remove(x)
                        else:
                            copySet.remove(y)
                    except ValueError:
                        pass
                        # print("이미 지워진 문장입니다.")
    return copySet


def isUniqueText(dataset, COpy, Usage):
    """
    Function that removes a single word from the dataset if a phrase containing the word exists.
    Set Usage parameter True, when want to use this function.
    
    examples) '한' '한 나라' '나라의' '한 나라의 대통령' -> '한 나라' '한 나라의 대통령'
    """
    # dataset : [ ( float, <class> ) ]
    # class   : <  >
    # print(resultSet[0][1].origin_terms)   :   일회용품 사용이

    if Usage is True:
        if COpy is True:
            copySet = dataset.copy()
        elif COpy is not True:
            copySet = dataset

        for x in dataset:
            if ' ' in x[0]:
                pass

            for y in dataset:
                if x == y:
                    pass
                elif ' ' not in y[0]:
                    pass
                else:
                    try:
                        if x[0] in y[0].split():
                            copySet.remove(x)
                    except ValueError:
                        # print("이미 제거되었습니다")
                        pass
        return copySet

    else:
        return dataset

def isUniqueSentence(dataset, COpy, Usage):
    """
    Function that deletes a phrase from the dataset if a phrase containing the phrase exists.
    Set Usage parameter True, when want to use this function.

    examples) '한 나라' '나라의' '한 나라 국민' -> '나라의' '한 나라 국민'
    """

    if Usage is True:
        if COpy is True:
            copySet = dataset.copy()
        elif COpy is not True:
            copySet = dataset

        for x in dataset:
            if ' ' not in x[0]:
                pass

            for y in dataset:
                if x == y:
                    pass
                elif ' ' not in y[0]:
                    pass
                else:
                    try:
                        if x[0].split() in y[0].split():
                            copySet.remove(x)
                    except ValueError:
                        # print("이미 제거되었습니다")
                        pass
        return copySet
    else:
        return dataset


class KeywordExtractor(object):

    def __init__(self, lan="ko", n=3, dedupLim=0.9, dedupFunc='seqm', windowsSize=1, top=20, features=None, stopwords=None, COpy=True, Usage=False):
        self.lan = lan

        dir_path = os.path.dirname(os.path.realpath(__file__))

        local_path = os.path.join("StopwordsList", "stopwords_%s.txt" % lan[:2].lower())

        if os.path.exists(os.path.join(dir_path,local_path)) == False:
            local_path = os.path.join("StopwordsList", "stopwords_noLang.txt")
        
        resource_path = os.path.join(dir_path,local_path)
        self.resource_path = resource_path  # stopword 관리를 위한 변수 추가

        if stopwords is None:
            try:
                with open(resource_path, encoding='utf-8') as stop_fil:
                    self.stopword_set = set( stop_fil.read().lower().split("\n") )
            except:
                print('Warning, read stopword list as ISO-8859-1')
                with open(resource_path, encoding='ISO-8859-1') as stop_fil:
                    self.stopword_set = set( stop_fil.read().lower().split("\n") )
        else:
            self.stopword_set = set(stopwords)

        self.n = n
        self.top = top
        self.dedupLim = dedupLim
        self.features = features
        self.COpy = COpy
        self.Usage = Usage
        self.windowsSize = windowsSize
        if dedupFunc == 'jaro_winkler' or dedupFunc == 'jaro':
            self.dedu_function = self.jaro
            # print('self.dedu_function jaro 테스트 :', self.dedu_function)
        elif dedupFunc.lower() == 'sequencematcher' or dedupFunc.lower() == 'seqm':
            self.dedu_function = self.seqm
            # print('self.dedu_function seqm 테스트 :', self.dedu_function)
        else:
            self.dedu_function = self.levs
            # print('self.dedu_function levs 테스트 :', self.dedu_function)

    def jaro(self, cand1, cand2):
        """
        using jaro_winkler distance algorithm.
        completed by original yake!
        """
        return jellyfish.jaro_winkler(cand1, cand2 )

    def levs(self, cand1, cand2):
        """
        using levenshtein_distance algorithm.
        completed by original yake!
        """
        return 1.-jellyfish.levenshtein_distance(cand1, cand2 ) / max(len(cand1),len(cand2))

    def seqm(self, cand1, cand2):
        """
        using levenshtein_distance ratio algorithm.
        completed by original yake!
        """
        return Levenshtein.ratio(cand1, cand2)

    def extract_keywords(self, text):
        """
        Function for extract keywords.
        Return value is set of list composed of tuple, except duplicated things.
        """
        try:
            if not(len(text) > 0):
                return []

            text = text.replace('\n\t',' ')
            # print('self.stopword_set 출력 :',self.stopword_set)
            dc = DataCore(text=text, stopword_set=self.stopword_set, windowsSize=self.windowsSize, n=self.n)
            # 형태소 원형 변경본 -> 원본으로 변경하는 작업 
            dc.build_single_terms_features(features=self.features)
            # 원본은 dc.initial_sentences_str에 담겨있음 
            # 형태소 원형 변경본의 경우 dc.sentences_obj의 각칸마다 들어있음  
            
            #print('dc initial 테스트 :', dc.initial_sentences_str)
            #print('candidates 테스트 :',dc.sentences_obj)#[0][0][0][2].H)
            #print('이곳을 추출')
            dc.build_mult_terms_features(features=self.features)
            resultSet = []
            todedup = sorted([cc for cc in dc.candidates.values() if cc.isValid()], key=lambda c: c.H)
            # print('todedup 테스트 :', len(todedup)) # n-gram의 composed_word 들로 들어감
            
            # 이곳에 펼친 값을 붙이자
            
            if self.dedupLim >= 1.:
                return ([ (cand.H, cand.unique_kw) for cand in todedup])[:self.top]

            for cand in todedup:
                toadd = True
                for (h, candResult) in resultSet:
                    dist = self.dedu_function(cand.unique_kw, candResult.unique_kw)
                    # print('좌 cand, 우 candResult :',cand.unique_kw," / ",candResult.unique_kw)
                    # print('dist 테스트 :',dist)
                    if dist > self.dedupLim:
                        toadd = False
                        break
                if toadd:
                    resultSet.append( (cand.H, cand) )
                if len(resultSet) == self.top:
                    break

            # print("stopword 저장 위치: ", self.resource_path)
            # stopword 자동 수정 로직
            try:
                with open(self.resource_path, 'r+', encoding='utf-8') as f:
                    stopwordset = list(set( f.read().split("\n") ))
                    stopwordset.sort()
                    # print("stopword 리스트 test1: ", stopwordset)
                    f.truncate(0)
                    f.close()

                print("stopword 리스트: ", stopwordset)
                with open(self.resource_path, 'a+', encoding='utf-8') as ft:
                    for i in stopwordset:
                        ft.write(i)
                        ft.write('\n')
                    ft.close()

            except:
                print('Warning, read stopword list as ISO-8859-1')
                with open(self.resource_path, 'r+', encoding='ISO-8859-1') as f:
                    stopwordset = list(set( f.read().lower().split("\n") ))
                    stopwordset.sort()
                    # print("stopword 리스트 test1: ", stopwordset)
                    f.truncate(0)
                    f.close()

                # print("stopword 리스트 test2: ", stopwordset)
                with open(self.resource_path, 'a+', encoding='utf-8') as ft:
                    for i in stopwordset:
                        ft.write(i)
                        ft.write('\n')
                    ft.close()

            # beforeReturnSet = isUniqueText(resultSet, self.COpy, self.Usage) # [(cand.kw,h) for (h,cand) in resultSet]
            # middleReturnSet = isUniqueSentence(beforeReturnSet, self.COpy, self.Usage)
            # afterReturnSet = isParagraphReDuplicated(middleReturnSet, self.COpy)
            # finalReturnSet = isWordReDuplicated(afterReturnSet, self.COpy)
            # print(beforeReturnSet)
            # print(resultSet[0][1]) # .origin_terms)

            testset = isParagraphReDuplicated(resultSet, self.COpy)

            return [(cand.origin_terms,h) for (h,cand) in testset]  # [(cand.kw, h) for (h,cand) in resultSet]

        except Exception as e:
            print(f"Warning! Exception: {e} generated by the following text: '{text}' ")
            return []
        
        