def selectExercise():
    print("어떤 운동을 진행하시겠습니까? (1: 스쿼트, 2: 런지, 3: 숨쉬기)")
    exercise = int(input())
    if(exercise == 1):
        print("스쿼트 운동을 시작합니다.")
        return 1
    elif(exercise == 2):
        print("런지 운동을 시작합니다.")
        return 2
    elif(exercise == 3):
        print("숨쉬기 운동을 시작합니다.")
        return 3


def isReady(keypoint):
    # keypoint[15][0]: 왼쪽 발목 y좌표, keypoint[1][0]: 왼쪽 눈 y좌표
    height = keypoint[15][0]-keypoint[1][0]
    MAX_LIMIT = 550
    MIN_LIMIT = 450

    if MIN_LIMIT <= height <= MAX_LIMIT:
        print("ready: ok")
        return True
    elif height > MAX_LIMIT:
        print("ready: 뒤로 가주세요")
        return False
    elif height < MIN_LIMIT:
        print("ready: 앞으로 가주세요")
        return False


def isSide(keypoint):
    # keypoint[11][1]: 왼쪽 골반 x좌표, keypoint[12][1]: 오른쪽 골반 x좌표
    pelvis = abs(keypoint[11][1] - keypoint[12][1])
    limit = 20

    if pelvis <= limit:
        print("side: 측면")
        return True
    else:
        print("side: 정면")
        return False
