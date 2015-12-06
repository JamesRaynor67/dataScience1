import re
import requests
import math

def getResponse(fileText):
    url = 'http://www.nlab.ci.i.u-tokyo.ac.jp/~nakayama/ds15/report1/upload.php'
    head = {'Authorization': 'Basic ZHNsZWN0dXJlOmRAdHNjLzE1','Content-Type': 'multipart/form-data;boundary=---------------------------1227245055187469359795215995'}
    data = '''
-----------------------------1227245055187469359795215995
Content-Disposition: form-data; name="upfile"; filename="result.txt"
Content-Type: text/plain

%s
-----------------------------1227245055187469359795215995
Content-Disposition: form-data; name="stname"

sakamotogakawai
-----------------------------1227245055187469359795215995
Content-Disposition: form-data; name="up"

upload
-----------------------------1227245055187469359795215995--

'''
    return requests.post(url, data=data % fileText, headers=head)

def getScore(_valueList):
    fileText = "\n".join(_valueList)
    response = getResponse(fileText)
    regularExp = re.compile(r'(\d+).(\d+)')
    score = regularExp.search(response.text)
    if score is None:
        print('Score not found')
        return None
    else:
        return float(score.group())

def biSearchOneAnswer(lowValue, highValue, index, _valueList):
    if lowValue == highValue:
        return str(lowValue)
    else:
        tmpValueList = _valueList[:]
        tmpValueList[index] = str(lowValue)
        lowScore = getScore(tmpValueList)
        tmpValueList[index] = str(highValue)
        highScore = getScore(tmpValueList)

        if abs(lowScore - highScore) < 0.0001:
            return str(int(math.ceil((lowValue+highValue)/2)))
        else:
            if lowScore < highScore:
                return biSearchOneAnswer(lowValue, int(math.ceil((lowValue+highValue)/2)), index, _valueList)
            else:
                return biSearchOneAnswer(int(math.floor((lowValue+highValue)/2)), highValue, index, _valueList)

def searchAllAnswer(_modifyList, _valueList):
    maxShare = int(pow(2,18))
    minShare = 0
    bestAnswerList = _valueList[:]
    for i in range(len(_valueList)):
        if _modifyList[i] == 1:
            bestAnswerList[i] = biSearchOneAnswer(minShare, maxShare, i, _valueList)
            print('#:{id}, bestSocre:{bestScoreValue}, originalSocre:{originalSocre}, diff:{diff}'.format(id=i, bestScoreValue=bestAnswerList[i], originalSocre=_valueList[i], diff=int(float(_valueList[i])-float(bestAnswerList[i]))))
    return bestAnswerList

fr=open('result.txt')
originalFileText = fr.read()
fr.close()

valueList = originalFileText.split()
modifyList = [0 for i in range(len(valueList))]

oldScore = getScore(valueList)
tmpValueList = valueList[:]
#for i in range(len(valueList)):
for i in range(2015):
    tmpValueList[i] = '0'
    newScore = getScore(tmpValueList)
    print('#:{id}, modified:{modified}, newSocre:{newScoreValue}, oldSocre:{oldScoreValue}'.format(id=i, modified=1 if newScore != oldScore else 0,\
     newScoreValue=newScore, oldScoreValue=oldScore))
    if newScore != oldScore:
        modifyList[i] = 1
        oldScore = newScore

bestAnswerList = searchAllAnswer(modifyList, valueList)
with open("bestAnswer.txt", "w") as text_file:
    print("\n".join(bestAnswerList), file=text_file)
