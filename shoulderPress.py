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
    down_arr = imageDetect.main(exCode+1)

    # 어께 - 팔꿈치 - 손목
    up_left_LIMIT = getDegree(up_arr[5], up_arr[7], up_arr[9])
    up_right_LIMIT = getDegree(up_arr[6], up_arr[8], up_arr[10])

    # ㄱ : 팔꿈치 - 척추상 - 척추중
    down_left_LIMIT1 = getDegree(down_arr[7], down_arr[17], down_arr[18])
    down_right_LIMIT1 = getDegree(down_arr[8], down_arr[17], down_arr[18])
    # ㄴ : 손목 - 팔꿈치 - 척추상
    down_left_LIMIT2 = getDegree(down_arr[9], down_arr[7], down_arr[17])
    down_right_LIMIT2 = getDegree(down_arr[10], down_arr[8], down_arr[17])
    cnt_flag = True


def pressDown(keypoint):
    # keypoint[7] : 왼쪽팔꿈치, keypoint[17] : 척추상, keypoint[18] : 척추중
    # keypoint[8] : 오른쪽팔꿈치, keypoint[17] : 척추상, keypoint[18] : 척추중
    # keypoint[9] : 왼쪽손목, keypoint[7] : 왼쪽팔꿈치, keypoint[17] : 척추상
    # keypoint[10]  : 오른쪽손목, keypoint[8] : 오른쪽팔꿈치, keypoint[17] : 척추상

    # ㄱ : 팔꿈치 - 척추상 - 척추중
    left_angle_1 = getDegree(keypoint[7], keypoint[17], keypoint[18])
    right_angle_1 = getDegree(keypoint[8], keypoint[17], keypoint[18])
    # ㄴ : 손목 - 팔꿈치 - 척추상
    left_angle_2 = getDegree(keypoint[9], keypoint[7], keypoint[17])
    right_angle_2 = getDegree(keypoint[10], keypoint[8], keypoint[17])
    value = 20


def pressUp(keypoint):
    # keypoint[5] : 왼쪽어깨, keypoint[7] : 왼쪽팔꿈치, keypoint[9] : 왼쪽손목
    # keypoint[6] : 오른쪽어깨, keypoint[8] : 오른쪽팔꿈치, keypoint[10] : 오른쪽손목

    left_angle = getDegree(keypoint[5], keypoint[7], keypoint[9])
    right_angle = getDegree(keypoint[6], keypoint[8], keypoint[10])
    value = 20


def postureCorrection(keypoint):
    if(pressDown(keypoint) and pressUp(keypoint)):
        tts.q.put("숄드 프레스 자세를 잘 잡으셨어요!")
        return True
    else:
        return False


def shoulderPress_count(keypoint):
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
    if shoulderPress_count(keypoint):
        global CNT
        CNT += 1
        tts.q.queue.clear()
        tts.q.put("성공한 횟수 " + str(CNT))
        return True
    else:
        return False
