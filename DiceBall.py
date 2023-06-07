import random
import time

isStart = True
#최대 라운드, 아웃카운트, 베이스 이미지 설정
MaxRound = 9
MaxOutCount = 3
baseimg = ["◆","○","○","○"]
outImg = ["_","_"]
base = [0,0,0,0]
strike = ["○","○"]
ball = ["○","○","○"]
#게임 진행중 바뀌는 변수 (라운드, 아웃카운트, 점수)
round = 1
strikeCount = 0
ballCount = 0
outCount = 0
computerScore = 0
playerScore = 0
pitchCount = 1
#주사위 변수 생성 함수
def radint():
    return random.randint(1,6)
    
#이미지 출력 함수
def attackImgPrint():
    print("-------------------------")
    print("|          ",baseimg[2],"          |")
    print("|          2nd          |")
    print("|",baseimg[3],"                 ",baseimg[1],"|")
    print("|3rd                 1st|")
    print("|          ",baseimg[0],"          |")
    print("|          Home         |")
    print("|  OUT",outImg[0],outImg[1]," | ROUND ",round," |")
    print("-------------------------")
    print("|         Score         |")
    print("| Computer : ",computerScore)
    print("|   Player : ",playerScore)

def increaseScore(player, score):
    global playerScore
    global computerScore
    if player == 1:
        playerScore += score
    else:
        computerScore += score
    return


#이미지 초기화 함수(공수교대/새 게임 시작) -> 정상 작동 확인
def initImg():
    global baseimg
    global outImg
    global strike
    global ball
    for i in range(1,3,1):
        baseimg[i] = "○"
    for i in range(2):
        outImg[i] = "_"
    for i in range(2):
        strike[i] = "○"
    for i in range(3):
        ball[i] = "○"

def initBallCount():
    global strikeCount
    global ballCount
    strikeCount = 0
    ballCount = 0

def changeGame():
    global base
    global outCount
    initBallCount()
    outCount = 0
    for i in range(1,4,1):
        base[i] = 0
    initImg()
    


#게임 초기화 함수(새 게임 시작)
def initGame():
    initImg()
    global computerScore
    global playerScore
    global round
    global strikeCount
    global ballCount
    computerScore = 0
    playerScore = 0
    round = 1
    strikeCount = 0
    ballCount = 0

#게임 이미지 변환 함수
def setAttackImg():
    global base
    global baseimg
    global outImg
    for i in range(4): #base 상황 업데이트
        if base[i] == 1:
            baseimg[i] = "●"
        elif base[i] == 0:
            baseimg[i] = "○"

    if outCount == 0: #outCount 상황 업데이트
        outImg[0] = "_"
        outImg[1] = "_"
    elif outCount == 1:
        outImg[0] = "X"
        outImg[1] = "_"
    elif outCount == 2:
        outImg[0] = "X"
        outImg[1] = "X"

    return

#타자 진출하는 상황
def single(player):   #안타 (모든 주자 +1)
    global base
    global outCount
    score = 0
    print("타자 안타를 칩니다!")
    for i in range(3,0,-1):
        if i == 3 and base[i] == 1: #3루에 주자가 있을때 Score+1
            score += 1
            continue
        elif i == 3 and base[i] == 0: #3루에 주자가 없을때 예외처리
            continue
        else: #i루에 사람이 존재한다면 1씩 진루
            if base[i] == 1:
                base[i+1] = 1
                base[i] = 0
    base[1] = 1 #타자 1루로 진출
    if score > 0:
        time.sleep(1)
        increaseScore(player,score)
        print(score,"점 획득!")
        
    return
def double(player):   #2루타 (모든 주자 +2)
    global base
    global outCount
    score = 0
    print("타자 2루타를 칩니다!")
    for i in range(3,0,-1):
        if (i == 3 or i == 2) and base[i] == 1: #2루,혹은 3루에 주자가 있을때 Score+1
            score += 1
            base[i] = 0
            continue
        elif (i == 3 or i == 2) and base[i] == 0: #2루,혹은 3루에 주자가 없을때 예외처리
            continue
        else: #i루에 사람이 존재한다면 2씩 진루
            if base[i] == 1:
                base[i+2] = 1
                base[i] = 0
    base[2] = 1 #타자 2루로 진출
    if score > 0:
        time.sleep(1)
        increaseScore(player,score)
        print(score,"점 획득!")
    return

def triple(player):   #3루타 (모든 주자 +3)
    global base
    global outCount
    score = 0
    print("타자 3루타를 칩니다!")
    for i in range(1,4,1):  #모든 베이스에 주자가 있다면 그 수 만큼 +1점
        if base[i] == 1:
            score += 1
    for i in range(1,4,1): # 주자가 있다면 모두 홈베이스까지 진출, 따라서 모든 베이스 0으로 초기화
        base[i] = 0
    base[3] = 1 #3루에 타자 진출
    if score > 0:
        time.sleep(1)
        increaseScore(player,score)
        print(score,"점 획득!")
    return
def homerun(player):  #홈런 (모든 주자 득점)
    global base
    global outCount
    score = 0
    print("☆★타자 홈런을 칩니다★☆")
    for i in range(1,4,1):  #모든 베이스에 주자가 있다면 그 수 만큼 +1점
        if base[i] == 1:
            base[i] = 0
            score += 1
    score += 1 #주자 득점
    time.sleep(1)
    increaseScore(player,score)
    print(score,"점 획득!")
    return

def walk(player):     #볼넷 (연속된 주자만 +1)
    global base
    global outCount
    score = 0
    linkedbase = 0
    print("볼넷!")
    for i in range(1,4,1): #연속된 주자의 수 체크
        if base[i] == 1:
            linkedbase += 1
        else: #연속된 주자가 없다면 break로 탈출
            break
    if linkedbase == 3: #만루인 상황
        score += 1
    elif linkedbase > 0: #만루가 아닌 상황에 연속된 주자들 1씩 진루
        for i in range(linkedbase,0,-1):
            base[i+1] = 1
            base[i] = 0
    base[1] = 1 #타자 1루로 진루
    if score > 0:
        time.sleep(1)
        increaseScore(player,score)
        print(score,"점 획득!")
    return
#타자 아웃되는 상황
def flyOut():   #플라이아웃 (타자 아웃, 주자 그대로) #flyout, groundout, strikeout 통용
    randNum = random.randint(1,7)
    if randNum <= 2:
        print("내야 뜬공! 아웃!")
    elif randNum <= 4:
        print("타자 플라이아웃!")
    else:
        print("플라이아웃!")
    global outCount
    outCount += 1
    return

def doublePlay(): #병살타 (가장 많이 진출한 주자 2명 아웃, 나머지 주자는 +1)
    global base
    global outCount
    outCount += 2
    checkbase = 0
    for i in range(1,4,1): #주자 체크
        if base[i] == 1:
            checkbase += 1
    if checkbase == 3: #주자가 3명인 경우 3,2루 주자 아웃
        print("병살타! 2루, 3루주자 아웃! ")
        base[3] = 0
        base[2] = 0
        outCount += 2
    elif checkbase == 2: #주자가 2명인경우
        outPlayer = 0
        print("병살타!", end="")
        for i in range(3,1,-1): #가장 많이 진출한 주자 2명 아웃
            if base[i] == 1 and outPlayer < 2: #주자가 있고 2명아웃시키지 않았다면 아웃처리, 
                print(i,"루, ", end="")
                base[i] = 0
                outPlayer += 1
                outCount += 1
        print("주자 아웃!\n")
    elif checkbase == 1: #주자가 1명만 있는경우
        for i in range (4): #타자와 주자 모두 아웃처리 후 아웃카운트 +2
            if base[i] == 1:
                print("병살타!",i,"루 주자, 타자 아웃!",end = "")
            base[i] = 0
        outCount += 2
    else:   #주자가 없는 경우
        print("타자 공을 쳤지만 아웃됩니다!")
        outCount += 1 #타자 아웃처리

def sacrificeFly(player): #타자아웃 -> 주자 +1
    global base
    global outCount
    score = 0
    print("희생 플라이!")
    for i in range(3,0,-1): #주자가 없는경우 타자 플라이아웃 처리
        if i == 1 and base[i] == 0:
            print("타자 플라이 아웃!")
            return
    for i in range(3,0,-1):
        if i == 3 and base[i] == 1: #3루에 주자가 있을때 Score+1
            score += 1
            base[i] = 0
            continue
        elif i == 3 and base[i] == 0: #3루에 주자가 없을때 예외처리
            continue
        else: #i루에 사람이 존재한다면 1씩 진루 ( i != 3 )
            if base[i] == 1:
                base[i+1] = 1
                base[i] = 0
    outCount += 1
    if score > 0:
        increaseScore(player,score)
        print(score,"점 획득!")
    return

#주자만 아웃되는 상황, 주자가 없다면 타자 아웃
def popOut():   #가장 높은 주자 아웃
    global base
    global outCount
    #주자 있는지 확인
    isBase = 0
    print("타자 쳤습니다!")
    for i in range(1,4,1):
        if base[i] == 1:
            isBase += 1
    if isBase == 0: #주자가 없다면
        print("타자 아웃!")
        outCount += 1 #아웃 1증가 후 리턴
        return
    for i in range(3,0,-1):
        if base[i] == 1:
            print(i,"루 주자 아웃!")
            base[i] = 0
            break
    for i in range(3,0,-1): #나머지 주자 1루씩 진출
        if base[i] == 1:
            base[i+1] = 1
            base[i] = 0
    base[1] = 1 #타자 1루 진출
    outCount += 1
    return

def getSmallerNum(dice1, dice2):
    if dice1<dice2:
        return dice1,dice2
    else:
        return dice2,dice1


def runGame(dice1, dice2):
    if (dice1 == 1):
        if(dice2 == 1): #홈런
            homerun(1)
        elif(dice2 == 2):
            double(1)
        elif(dice2 == 3):
            flyOut()
        elif(dice2 == 4):
            walk(1)
        elif(dice2 == 5):
            popOut()
        elif(dice2 == 6):
            single(1)
    elif (dice1 == 2):
        if(dice2 == 2):
            double(1)
        elif(dice2 == 3):
            popOut()
        elif(dice2 == 4):
            flyOut()
        elif(dice2 == 5):
            single(1)
        elif(dice2 == 6):
            flyOut()
    elif (dice1 == 3):
        if(dice2 == 3):
            walk(1)
        elif(dice2 == 4):
            triple(1)
        elif(dice2 == 5):
            popOut()
        elif(dice2 == 6):
            flyOut()
    elif (dice1 == 4):
        if(dice2 == 4):
            walk(1)
        elif(dice2 == 5):
            popOut()
        elif(dice2 == 6):
            flyOut()
    elif (dice1 == 5):
        if(dice2 == 5):
            double(1)
        elif(dice2 == 6):
            sacrificeFly(1)
    elif (dice1 == 6):
        if(dice2 == 6):
            homerun(1)
    
def showResult():
    print("--------------------")
    print("Score")
    print("Computer : ",computerScore)
    print("Player   : ",playerScore)
    print("--------------------")
    if computerScore > playerScore:
        print("Computer Win!")
    elif computerScore < playerScore:
        print("Player Win!")
    else:
        print("Draw!")

def attack():
    while(outCount < MaxOutCount):
        start = input("아무거나 입력하면 주사위가 굴러갑니다.")
        time.sleep(1)
        print("주사위를 굴립니다.")
        time.sleep(1)
        dice1 = radint()
        print("첫번째 숫자는:",dice1)
        time.sleep(1)
        dice2 = radint()
        print("두번째 숫자는:",dice2)
        time.sleep(1)
        dice1,dice2 = getSmallerNum(dice1,dice2)
        runGame(dice1,dice2)
        time.sleep(2)
        if outCount == 3:
            print("3아웃! 공수교대!")
            break
        setAttackImg()
        attackImgPrint()
    return

def setDefenseImg():
    global baseimg
    global outImg
    global strike
    global ball
    for i in range(4): #base 상황 업데이트
        if base[i] == 1:
            baseimg[i] = "●"
        elif base[i] == 0:
            baseimg[i] = "○"

    if outCount == 0: #outCount 상황 업데이트
        outImg[0] = "_"
        outImg[1] = "_"
    elif outCount == 1:
        outImg[0] = "X"
        outImg[1] = "_"
    elif outCount == 2:
        outImg[0] = "X"
        outImg[1] = "X"

    if strikeCount == 0:
        strike[0] = "○"
        strike[1] = "○"
    elif strikeCount == 1:
        strike[0] = "●"
        strike[1] = "○"
    elif strikeCount == 2:
        strike[0] = "●"
        strike[1] = "●"

    if ballCount == 0:
        ball[0] = "○"
        ball[1] = "○"
        ball[2] = "○"
    elif ballCount == 1:
        ball[0] = "●"
        ball[1] = "○"
        ball[2] = "○"
    elif ballCount == 2:
        ball[0] = "●"
        ball[1] = "●"
        ball[2] = "○"
    elif ballCount == 3:
        ball[0] = "●"
        ball[1] = "●"
        ball[2] = "●"
    return

def defenseImgPrint():
    print("-------------------------")
    print("|          ",baseimg[2],"          |")
    print("|          2nd          |")
    print("|",baseimg[3],"                 ",baseimg[1],"|")
    print("|3rd                 1st|")
    print("|          ",baseimg[0],"          |")
    print("|          Home         |")
    print("|STRIKE",strike[0],strike[1],"|BALL",ball[0],ball[1],ball[2],"|")
    print("|  OUT",outImg[0],outImg[1]," | ROUND ",round," |")
    print("-------------------------")
    print("|         Score         |")
    print("| Computer : ",computerScore)
    print("|   Player : ",playerScore)
    return

def pitchSelect():
    print("구종별 확률   Strike  Ball   Hit ")
    print("1. 패스트볼      40%   20%   40%")
    print("2. 슬라이더      38%   32%   30%")
    print("3. 체인지업      45%   10%   45%")
    print("4.   포크볼      35%   45%   20%")
    print("5.   커브볼      38%   32%   30%")
    while(True):
        ret = int(input("구종을 선택하세요:"))
        if ret == 1 or ret == 2 or ret == 3 or ret == 4 or ret == 5:
            break
        else:
            print("다시 선택해주세요.")
    return ret

def Strike():
    time.sleep(1)
    global strikeCount
    global outCount
    strikeCount += 1
    print("스트라이크!")
    if strikeCount == 3:
        time.sleep(1)
        print("타자 삼진 아웃!")
        initBallCount()
        outCount += 1
    return

def Ball():
    global ballCount
    time.sleep(1)
    global initBallCount
    ballCount += 1
    print("볼!")
    if ballCount == 4:
        time.sleep(1)
        print("포볼! 타자 1루로 진출")
        initBallCount()
        walk(2)
    return

def Foul():
    time.sleep(1)
    global strikeCount
    strikeCount += 1
    print("타자 공을 쳤지만 파울이 됩니다!")
    if strikeCount == 3:
        strikeCount = 2
    return

def Hit():
    time.sleep(1)
    randNum = random.randint(1,18)
    initBallCount()
    print("타자가 공을 쳤습니다!")
    time.sleep(1)
    if randNum <= 2:
        homerun(2)
    elif randNum <= 4:
        double(2)
    elif randNum <= 6:
        flyOut()
    elif randNum <= 8:
        popOut()
    elif randNum <= 10:
        single(2)
    elif randNum <= 11:
        doublePlay()
    elif randNum <= 13:
        flyOut()
    elif randNum <= 14:
        triple(2)
    elif randNum <= 15:
        sacrificeFly(2)
    else:
        Foul()
    return

def fastBall():
    randNum = random.randint(1,100)
    if randNum <= 40:
        Strike()
    elif randNum >= 41 and randNum <= 60:
        Ball()
    else:
        Hit()
    return

def slider():
    randNum = random.randint(0,100)
    if randNum <= 38:
        Strike()
    elif randNum >= 39 and randNum <= 70:
        Ball()
    else:
        Hit()
    return

def changeUp():
    randNum = random.randint(0,100)
    if randNum <= 45:
        Strike()
    elif randNum >= 46 and randNum <= 55:
        Ball()
    else:
        Hit()
    return

def forkBall():
    randNum = random.randint(0,100)
    if randNum <= 35:
        Strike()
    elif randNum >= 36 and randNum <= 80:
        Ball()
    else:
        Hit()
    return

def curveBall():
    randNum = random.randint(0,100)
    if randNum <= 38:
        Strike()
    elif randNum >= 39 and randNum <= 70:
        Ball()
    else:
        Hit()
    return

def defense():
    global pitchCount
    while(True):
        pitch = pitchSelect()
        if pitch == 1 or pitch == 2 or pitch == 3 or pitch == 4 or pitch ==5:
            print("제",pitchCount,"구 던집니다!", end="")
            pitchCount += 1
        if pitch == 1:
            print(" 패스트볼!")
            fastBall()
        elif pitch == 2:
            print(" 슬라이더!")
            slider()
        elif pitch == 3:
            print(" 체인지업!")
            changeUp()
        elif pitch == 4:
            print(" 포크볼!")
            forkBall()
        elif pitch == 5:
            print(" 커브볼!")
            curveBall()
        else:
            print("잘못 입력하였습니다.")
        if outCount == 3:
            print("3아웃! 공수교대!")
            break
        time.sleep(1)
        setDefenseImg()
        defenseImgPrint()
        time.sleep(2)
    return

while (isStart):
    ans = input("게임을 시작하시겠습니까? (예: Y / 아니요: N)")
    ans = ans.upper()
    if ans == "Y":
        while(True): #선공/후공 선택
            turn = int(input("선공/후공을 선택해주세요.(1.선공 / 2.후공)"))
            if turn == 1 or turn == 2:
                break
            print("잘못 입력하였습니다. 다시 입력해주세요.")
            time.sleep(2)
        while (round <= MaxRound):  #라운드 시작
            initImg()
            print("-------------")
            print(round, "라운드 시작")
            print("-------------")
            if turn == 1: #선공
                attack()  #아웃카운트가 3이 될때까지 공격 실행
                if computerScore > playerScore: #선공인데 컴퓨터스코어가 높은경우 9회초 종료
                    break
                changeGame()
                defense() #아웃카운트가 3이 될때까지 수비 실행
                round += 1
            else:         #후공
                defense() #수비
                if computerScore < playerScore: #후공인데 플레이어스코어가 높은경우 9회초 종료
                    break
                changeGame()
                attack()  #공격
                round += 1
            changeGame()
        print("게임이 종료되었습니다.")
        showResult()
    elif ans == "N":
        print("게임이 종료되었습니다.")
        break
    else:
        print("다시 입력해주세요.")