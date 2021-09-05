from speechRecognition import tts
from speechRecognition import stt

def selectExercise():
    tts.q.queue.clear()
    tts.q.put("어떤 운동을 진행하시겠습니까? (1: 스쿼트, 2: 숄더프레스, 3: 레터럴레이즈)")
    exercise = int(stt.sttFunction())

    global exerciseCode
    exerciseCode = 0
    
    if(exercise == 1):
        tts.q.queue.clear()
        tts.q.put("스쿼트 운동을 시작합니다.")
        exerciseCode = 1
    elif(exercise == 2):
        tts.q.queue.clear()
        tts.q.put("숄더프레스 운동을 시작합니다.")
        exerciseCode = 2
    elif(exercise == 3):
        tts.q.queue.clear()
        tts.q.put("레터럴 레이즈 운동을 시작합니다.")
        exerciseCode = 3


def isReady(keypoint):
    # keypoint[15][0]: 왼쪽 발목 y좌표, keypoint[1][0]: 왼쪽 눈 y좌표
    height = keypoint[15][0]-keypoint[1][0]
    MAX_LIMIT = 320
    MIN_LIMIT = 250

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
