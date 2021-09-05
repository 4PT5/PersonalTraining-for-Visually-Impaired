import math
import imageDetect
from speechRecognition import tts

CNT = 0


def getDegree(key1, key2, key3):
    x = math.atan((key1[0] - key2[0]) / (key1[1] - key2[1])) - \
        math.atan((key3[0] - key2[0]) / (key3[1] - key2[1]))
    return x*180/math.pi


def setting(exCode):
    global up_left_LIMIT, up_right_LIMIT, cnt_flag
    global down_left_LIMIT1, down_right_LIMIT1, down_left_LIMIT2, down_right_LIMIT2
    up_arr = imageDetect.main(exCode)
    down_arr = imageDetect.main(exCode+0.5)

    # 어께 - 팔꿈치 - 손목
    up_left_LIMIT = getDegree(up_arr[5], up_arr[7], up_arr[9])
    up_right_LIMIT = getDegree(up_arr[6], up_arr[8], up_arr[10])

    # 손목 - 어깨 기울기
    up_left_slope_LIMIT = up_arr[9][0]-up_arr[5][0] / up_arr[9][1]-up_arr[5][1]
    up_right_slope_LIMIT = up_arr[10][0]-up_arr[6][0] / up_arr[10][1]-up_arr[6][1]
    
    print("왼 손목-어깨 기울기: ", up_left_slope_LIMIT)
    print("오 손목-어깨 기울기: ", up_right_slope_LIMIT)

    down_left_slope_LIMIT = down_arr[9][0]-down_arr[5][0] / down_arr[9][1]-down_arr[5][1]
    down_right_slope_LIMIT = down_arr[10][0]-down_arr[6][0] / down_arr[10][1]-down_arr[6][1]
    
    print("왼 손목-어깨 기울기: ", down_left_slope_LIMIT)
    print("오 손목-어깨 기울기: ", down_right_slope_LIMIT)

    cnt_flag = True


def raiseDown(keypoint):
    # keypoint[5] : 왼쪽 어깨, keypoint[7] : 왼쪽 팔꿈치, keypoint[9] : 왼쪽 손목
    # keypoint[6] : 오른쪽 어깨, keypoint[8] : 오른쪽 팔꿈치, keypoint[10] : 오른쪽 손목

    value = 20


def raiseUp(keypoint):
    # keypoint[5] : 왼쪽 어깨, keypoint[7] : 왼쪽 팔꿈치, keypoint[9] : 왼쪽 손목
    # keypoint[6] : 오른쪽 어깨, keypoint[8] : 오른쪽 팔꿈치, keypoint[10] : 오른쪽 손목

    value = 20


def postureCorrection(keypoint):
    if(raiseDown(keypoint) and raiseUp(keypoint)):
        tts.q.put("레터럴 레이즈 자세를 잘 잡으셨어요!")
        return True
    else:
        return False


def leteralRaise_count(keypoint):
    left_angle = getDegree(keypoint[5], keypoint[7], keypoint[9])
    right_angle = getDegree(keypoint[6], keypoint[8], keypoint[10])
    value = 35
    global cnt_flag

    if():
        cnt_flag = False
        return True
    elif():
        cnt_flag = True
        return False


def counting(keypoint):
    if leteralRaise_count(keypoint):
        global CNT
        CNT += 1
        tts.q.queue.clear()
        tts.q.put("성공한 횟수 " + str(CNT))
        return True
    else:
        return False
