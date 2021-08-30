import math
import imageDetect

CNT = 0


def getDegree(key1, key2, key3):
    x = math.atan((key1[0] - key2[0]) / (key1[1] - key2[1])) - \
        math.atan((key3[0] - key2[0]) / (key3[1] - key2[1]))
    return x*180/math.pi


def setting():
    global d_LIMIT, s_LIMIT, LIMIT, CNT
    arr = imageDetect.main()
    d_LIMIT = arr[12][0]-arr[14][0]
    s_LIMIT = getDegree(arr[12], arr[18], arr[14]) # 상체-무릎 각도 limit
    LIMIT = abs(getDegree(arr[12], arr[14], arr[16]))

    print("카운트를 시작합니다. 5회 반복해주세요.")

# 런지 무릎 각도 (ㄱㄴ)
def lunge_knee_angle(keypoint, i):
    # keypoint[11] : 왼쪽골반, keypoint[13] : 왼쪽무릎, keypoint[15] : 왼쪽발목
    # +i (1) = 오른쪽
    angle = getDegree(keypoint[11+i], keypoint[13+i], keypoint[15+i])

    print("------------------")
    print("1. lunge_knee_angle")
    print("LIMIT")
    print(LIMIT)
    print(angle)
    if angle >= LIMIT:
        print("OK")
        return True
    else:
        print("무릎이 발보다 더 나와있습니다.")
        return False

# 상체 기울기 체크
def lunge_straight(keypoint, i):
    # keypoint[11] : 왼쪽골반, keypoint[18] : 척수중, keypoint[13] : 왼쪽 무릎
    value = 10 # testing 후 적당한 값 찾아야함
    angle = getDegree(keypoint[11+i], keypoint[18], keypoint[13+i])

    print("------------------")
    print("2. lunge_straight")
    print("s_LIMIT")
    print(s_LIMIT)
    print(angle)
    if s_LIMIT-value <= angle <= s_LIMIT+value:
        print("OK")
        return True
    elif angle < s_LIMIT-value:
        print("조금 더 허리를 세워주세요.")
        return False
    elif angle > s_LIMIT+value:
        print("조금 더 허리를 구부려주세요.")
        return False

        
# 무릎 발끝 위치 비교
def lunge_tiptoe(keypoint, i):
    # keypoint[11][0] : 왼쪽 골반 y좌표, keypoint[13][0] : 왼쪽 무릎 y좌표
    # +i (1) = 오른쪽
    hip_knee= keypoint[11+i][0]-keypoint[13+i][0]
    value = 30
    print("===================================================")
    print("3. lunge_down")
    print("d_LIMIT")
    print(d_LIMIT)
    print(hip_knee)
    if(hip_knee > d_LIMIT + value):
        print("조금 일어나세요.")
        return False
    elif(d_LIMIT - value <= hip_knee <= d_LIMIT + value):
        print("checkpoint #2 OK")
        return True
    else:
        print("조금 더 앉으세요")
        return False


def main(keypoint):
    for i in range (0,2):
        if lunge_knee_angle(keypoint, i) and lunge_straight(keypoint, i) and lunge_tiptoe(keypoint, i):
            return True
        else:
            return False
