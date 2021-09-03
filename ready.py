from speechRecognition import tts


def selectExercise():
    tts.q.queue.clear()
    tts.q.put("어떤 운동을 진행하시겠습니까? (1: 스쿼트, 2: 런지, 3: 숨쉬기)")
    exercise = int(input())
    if(exercise == 1):
        tts.q.queue.clear()
        tts.q.put("스쿼트 운동을 시작합니다.")
        return 1
    elif(exercise == 2):
        tts.q.queue.clear()
        tts.q.put("숄더프레스 운동을 시작합니다.")
        return 2
    elif(exercise == 3):
        tts.q.queue.clear()
        tts.q.put("숨쉬기 운동을 시작합니다.")
        return 3


def isReady(keypoint):
    # keypoint[15][0]: 왼쪽 발목 y좌표, keypoint[1][0]: 왼쪽 눈 y좌표
    height = keypoint[15][0]-keypoint[1][0]
    MAX_LIMIT = 550
    MIN_LIMIT = 450

    if MIN_LIMIT <= height <= MAX_LIMIT:
        tts.q.queue.clear()
        tts.q.put("ready: ok")
        return True
    elif height > MAX_LIMIT:
        tts.q.queue.clear()
        tts.q.put("ready: 뒤로 가주세요")
        return False
    elif height < MIN_LIMIT:
        tts.q.queue.clear()
        tts.q.put("ready: 앞으로 가주세요")
        return False


def isSide(keypoint):
    # keypoint[11][1]: 왼쪽 골반 x좌표, keypoint[12][1]: 오른쪽 골반 x좌표
    pelvis = abs(keypoint[11][1] - keypoint[12][1])
    limit = 20

    if pelvis <= limit:
        tts.q.queue.clear()
        tts.q.put("side: 측면")
        return True
    else:
        tts.q.queue.clear()
        tts.q.put("side: 정면")
        return False
