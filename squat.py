import math
import imageDetect
import threading
import pyttsx3
import queue

CNT = 0


class TTSThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.daemon = True
        self.start()

    def run(self):
        tts_engine = pyttsx3.init()
        tts_engine.startLoop(False)
        t_running = True
        while t_running:
            if self.queue.empty():
                tts_engine.iterate()
            else:
                data = self.queue.get()
                if data == "exit":
                    t_running = False
                else:
                    tts_engine.say(data)
        tts_engine.endLoop()


q = queue.Queue()
tts_thread = TTSThread(q)


def getDegree(key1, key2, key3):
    x = math.atan((key1[0] - key2[0]) / (key1[1] - key2[1])) - \
        math.atan((key3[0] - key2[0]) / (key3[1] - key2[1]))
    return x*180/math.pi


def setting(exCode):
    global d_LIMIT, s_LIMIT, LIMIT, CNT, cnt_flag
    arr = imageDetect.main(exCode)
    d_LIMIT = ((arr[11][0]-arr[13][0])+(arr[12][0]-arr[14][0]))/2
    s_LIMIT = getDegree(arr[17], arr[18], arr[19])
    LIMIT = abs(getDegree(arr[12], arr[14], arr[16]) +
                getDegree(arr[11], arr[13], arr[15]))/2
    cnt_flag = True


def squat_down(keypoint):
    # keypoint[11][0] : 왼쪽 골반 y좌표, keypoint[13][0] : 왼쪽 무릎 y좌표
    # keypoint[12][0] : 오른쪽 골반 y좌표, keypoint[14][0] : 오른쪽 무릎 y좌표
    hip_knee_l = keypoint[11][0]-keypoint[13][0]
    hip_knee_r = keypoint[12][0]-keypoint[14][0]
    hip_knee = (hip_knee_l+hip_knee_r)/2
    value = 30
    isStand = d_LIMIT - value > hip_knee or hip_knee > d_LIMIT + value

    if(d_LIMIT - value <= hip_knee <= d_LIMIT + value):
        return True
    elif(hip_knee > d_LIMIT + value):
        q.queue.clear()
        q.put("1: 조금 일어나세요.")
        return False
    elif(-100 < hip_knee < d_LIMIT - value):
        q.queue.clear()
        q.put("1: 조금 더 앉으세요")
        return False
    else:
        return False


def squat_straight(keypoint):
    # keypoint[17] : 척수상, keypoint[18] : 척수중, keypoint[19] : 척추하
    value = 10
    angle = getDegree(keypoint[17], keypoint[18], keypoint[19])

    if s_LIMIT-value <= angle <= s_LIMIT+value:
        return True

    elif angle < s_LIMIT-value:
        q.queue.clear()
        q.put("2: 조금 더 허리를 세워주세요.")
        return False

    elif angle > s_LIMIT+value:
        q.queue.clear()
        q.put("2: 조금 더 허리를 구부려주세요.")
        return False


def squat_knee_angle(keypoint):
    # keypoint[12] : 오른쪽골반, keypoint[14] : 오른쪽무릎, keypoint[16] : 오른쪽발목
    # keypoint[11] : 왼쪽골반, keypoint[13] : 왼쪽무릎, keypoint[15] : 왼쪽발목
    right_angle = getDegree(keypoint[12], keypoint[14], keypoint[16])
    left_angle = getDegree(keypoint[11], keypoint[13], keypoint[15])
    angle = abs((right_angle + left_angle) / 2)

    if angle >= LIMIT:
        return True
    else:
        q.queue.clear()
        q.put("무릎이 발보다 더 나와있습니다.")
        return False


def squat_count(keypoint):
    # keypoint[11][0] : 왼쪽 골반 y좌표, keypoint[13][0] : 왼쪽 무릎 y좌표
    # keypoint[12][0] : 오른쪽 골반 y좌표, keypoint[14][0] : 오른쪽 무릎 y좌표
    hip_knee_l = keypoint[11][0]-keypoint[13][0]
    hip_knee_r = keypoint[12][0]-keypoint[14][0]
    hip_knee = (hip_knee_l+hip_knee_r)/2
    value = 35
    global cnt_flag

    if(cnt_flag and d_LIMIT - value <= hip_knee <= d_LIMIT + value):
        cnt_flag = False
        return True
    elif d_LIMIT - value > hip_knee or hip_knee > d_LIMIT + value:
        cnt_flag = True
        return False


def postureCorrection(keypoint):
    if(squat_down(keypoint) and squat_straight(keypoint) and squat_knee_angle(keypoint)):
        q.put("스쿼트 자세를 잘 잡으셨어요!")
        return True
    else:
        return False


def counting(keypoint):
    if squat_count(keypoint):
        global CNT
        CNT += 1
        q.queue.clear()
        q.put("성공한 횟수 " + str(CNT))
        return True
    else:
        return False
