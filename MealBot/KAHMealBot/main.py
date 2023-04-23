import tweepy
# 트위터 api
from neispy import Neispy
# 교육청 api
from datetime import datetime
# 현재 시간 가져오기 위함
import sys

# twitter developer에서 아래의 값들을 구할 수 잇음.
# https://developer.twitter.com/en
# 트위터 Consumer Keys
apikey = 'WwxGR0uarHBtkMQyhHnU2v9Rv'
apisecret = 'hKWh82mXxeauj5W4nyVsKOiV1xR9YG1JjTAKA0pPGiFsDA7OQS'
# 트위터 Authentication Tokens
access_token = '1390944695530885126-ZZtkZXRBnNAu7QpOG7aESPKnDcrmt1'
access_token_secret = 'RvAXnxswqGa1uhjIvqlYbL3KTlnxR870Dse8RQms3YuxR'

# tweepy 설정
# 이부분은 그냥 tweepy에서 하라는데로 한 것..
auth = tweepy.OAuthHandler(apikey, apisecret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

#학교 이름, 변경하지 말것
name = "한국애니메이션고등학교"

# 트위터에 트윗하는 함수
# message : 트윗할 내용 
def Twit(message):
    print(message)
    try:
        api.update_status(message)
        # tweepy로 트윗
    except Exception as e: 
        print(e)
        # Exception 발생 시 터미널에 출력

# 급식 정보를 가져오는 함수
# pMealtime : 급식의 index를 받아옴 
# 그러나 위탁급식으로 인해 점심밖에 제공되지 않음, 0으로 고정
def GetMeal(pMealtime):

    # neispy 설정 
    neis = Neispy.sync()

    scinfo = neis.schoolInfo(SCHUL_NM=name)
    AE = scinfo[0].ATPT_OFCDC_SC_CODE  
    SE = scinfo[0].SD_SCHUL_CODE  

    Year = datetime.today().strftime("%Y")
    Month = datetime.today().strftime("%m")
    Date = datetime.today().strftime("%d")

    # 최종적으로 출력될 값
    # 원래는 아침 점심 저녁을 전부 출력해줬으나
    # 위탁급식으로 변경 후 neispy에서 아침 / 저녁을 가져올 수 없어서
    # 점심으로 고정해놨음.
    outputString = ('{}년 {}월 {}일\n한국애니메이션고등학교 점심입니다.\n'.format(Year,Month,Date))

    try:
        mealData = neis.mealServiceDietInfo(AE, SE, MLSV_YMD=int(datetime.today().strftime("%Y%m%d")))
        mealString = mealData[pMealtime].DDISH_NM.replace("<br/>", "\n")
        outputString += mealString
    except Exception as e:
        # neispy에서 가끔 api 문제가 생김
        # 이 경우 출력값을 비우고 에러를 터미널에 출력
        print(e)
        outputString = ""

    return outputString

def main():
    # 인자로 run이 들어온 경우에만 출력
    # heroku에서는 앱이 업로드되면 일단 실행됨
    # 그러므로 scehduler에 의해서만 실행 가능하도록 인자를 설정
    # C++의 char* argv[], C#의 string args[] 같은거라고 생각하면 편함. 
    arg = sys.argv[sys.argv.__len__()-1] 
    if arg == 'run':
        Twit(GetMeal(0))
    elif arg == 'test':
        Twit('Testing')

# main함수 실행
main()