import posenet
import tensorflow as tf
import cv2
import numpy as np

import time
import squat
import shoulderPress
import leteralRaise
import ready
from speechRecognition import tts
np.set_printoptions(threshold=np.inf, linewidth=np.inf)

args = {"model": 101, "scale_factor": 1.0, "notxt": True, "image_dir": './images',
        "output_dir": './output'}
position = ["코", "왼쪽눈", "오른쪽눈", "왼쪽귀", "오른쪽귀", "왼쪽어깨", "오른쪽어깨", "왼쪽팔꿈치", "오른쪽팔꿈치",
            "왼쪽손목", "오른쪽손목", "왼쪽골반부위", "오른쪽골반부위", "왼쪽무릎", "오른쪽무릎", "왼쪽발목", "오른쪽발목"]

# 척추상 : Spine At The Shoulder , 척추중 : Middle Of The Spine , 척추하 : Base Of Spine
spine_position = ["척추상", "척추중", "척추하"]


def getAverage(pos, n):
    x, y = 0, 0

    for i in range(n):
        x += pos[i][0]
        y += pos[i][1]

    return [x/n, y/n]


class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(1)

    def __del__(self):
        self.cap.release()


def gen(camera):
    with tf.compat.v1.Session() as sess:
        model_cfg, model_outputs = posenet.load_model(args['model'], sess)
        output_stride = model_cfg['output_stride']

        start = time.time()
        frame_count = 0
        cnt = 0
        cycle = 4
        init = True
        init2 = False
        init3 = False

        exerciseCode = ready.exerciseCode

        while True:
            cnt += 1
            input_image, display_image, output_scale = posenet.read_cap(
                camera.cap, scale_factor=args['scale_factor'], output_stride=output_stride)

            heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = sess.run(
                model_outputs,
                feed_dict={'image:0': input_image}
            )

            pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multi.decode_multiple_poses(
                heatmaps_result.squeeze(axis=0),
                offsets_result.squeeze(axis=0),
                displacement_fwd_result.squeeze(axis=0),
                displacement_bwd_result.squeeze(axis=0),
                output_stride=output_stride,
                max_pose_detections=10,
                min_pose_score=0.15)

            # 0:코, 1:왼쪽눈, 2:오른쪽눈, 3:왼쪽귀, 4:오른쪽귀", 5:왼쪽어깨, 6:오른쪽어깨
            # 7:왼쪽팔꿈치, 8:오른쪽팔꿈치, 9:왼쪽손목, 10:오른쪽손목, 11:왼쪽골반부위, 12:오른쪽골반부위
            # 13:왼쪽무릎, 14:오른쪽무릎, 15:왼쪽발목, 16:오른쪽발목
            # 17:척추상 = 5/6평균, 18:척추중 = 5/6/11/12평균 19:척추하 = 11/12평균

            spineTop = getAverage(
                [keypoint_coords[0][5], keypoint_coords[0][6]], 2)
            spineMiddle = getAverage(
                [keypoint_coords[0][5], keypoint_coords[0][6], keypoint_coords[0][11], keypoint_coords[0][12]], 4)
            spineBottom = getAverage(
                [keypoint_coords[0][11], keypoint_coords[0][12]], 2)

            spine_pos = [spineTop, spineMiddle, spineBottom]

            for i in range(3):
                tmp = np.array([[spine_pos[i]], [[0.0, 0.0]], [[0.0, 0.0]], [[0.0, 0.0]], [[0.0, 0.0]], [[
                    0.0, 0.0]], [[0.0, 0.0]], [[0.0, 0.0]], [[0.0, 0.0]], [[0.0, 0.0]]])
                keypoint_coords = np.concatenate(
                    (keypoint_coords, tmp), axis=1)
                keypoint_scores = np.concatenate(
                    (keypoint_scores, np.array([[1], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00], [0.00000000e+00]])), axis=1)

            keypoint_coords *= output_scale
            position.extend(spine_position)

            if cnt == 1:
                tts.q.put("10초 후에 시작합니다. 자리를 잡아주세요.")

            if cnt % cycle == 0:
                if init:
                    if cnt > 30 and ready.isReady(keypoint_coords[0]):
                        init = False
                        init2 = True
                        init3 = True

                elif init2:
                    if exerciseCode == 1 and ready.isSide(keypoint_coords[0]):
                        init2 = False
                        init3 = True
                        squat.setting(exerciseCode)
                        tts.q.put(
                            "스쿼트는 대표적인 하체운동이며, 준비자세는 ~ 하는 방법 ~. 준비 자세를 잡아주세요.")
                    elif exerciseCode == 2:
                        if init3:
                            shoulderPress.setting(exerciseCode)
                            tts.q.put(
                                "숄더프레스는 대표적인 어깨운동이며, 준비자세는 ~ 하는 방법 ~. 준비 자세를 잡아주세요.")
                            init3 = False
                        if shoulderPress.isDown(keypoint_coords[0]):
                            init2 = False
                            init3 = True
                            tts.q.queue.clear()
                            tts.q.put("숄더프레스를 1회 해주세요.")
                    elif exerciseCode == 3:
                        init2 = False
                        init3 = True
                        leteralRaise.setting(exerciseCode)
                        tts.q.put(
                            "리터럴 레이즈는 대표적인 어깨운동이며, 준비자세는 ~ 하는 방법 ~. 준비 자세를 잡아주세요.")

                elif init3:
                    if exerciseCode == 1:
                        if squat.postureCorrection(keypoint_coords[0]):
                            tts.q.queue.clear()
                            tts.q.put("10초 후 카운트를 시작합니다. 5회 반복해주세요.")
                            cnt = 2
                            init3 = False
                    elif exerciseCode == 2:
                        if shoulderPress.postureCorrection(keypoint_coords[0]):
                            tts.q.queue.clear()
                            tts.q.put("10초 후 카운트를 시작합니다. 5회 반복해주세요.")
                            cnt = 2
                            init3 = False
                    elif exerciseCode == 3:
                        if leteralRaise.postureCorrection(keypoint_coords[0]):
                            tts.q.queue.clear()
                            tts.q.put("10초 후 카운트를 시작합니다. 5회 반복해주세요.")
                            cnt = 2
                            init3 = False

                else:
                    if exerciseCode == 1:
                        if cnt == 30:
                            tts.q.put("시작해주세요.")
                        elif cnt > 30 and squat.counting(keypoint_coords[0]):
                            if squat.CNT == 5:
                                tts.q.put("스쿼트 5회를 마쳤습니다. 수고하셨습니다.")
                                break
                    elif exerciseCode == 2:
                        if cnt == 30:
                            tts.q.put("시작해주세요.")
                        elif cnt > 30 and shoulderPress.counting(keypoint_coords[0]):
                            if shoulderPress.CNT == 5:
                                tts.q.put("숄더프레스 5회를 마쳤습니다. 수고하셨습니다.")
                                break
                    elif exerciseCode == 3:
                        if cnt == 30:
                            tts.q.put("시작해주세요.")
                        elif cnt > 30 and leteralRaise.counting(keypoint_coords[0]):
                            if leteralRaise.CNT == 5:
                                tts.q.put("레터럴레이즈 5회를 마쳤습니다. 수고하셨습니다.")
                                break

            # TODO this isn't particularly fast, use GL for drawing and display someday...
            overlay_image = posenet.draw_skel_and_kp(
                display_image, pose_scores, keypoint_scores, keypoint_coords,
                min_pose_score=0.15, min_part_score=0.1)

            overlay_image = cv2.resize(overlay_image, dsize=(
                1240, 920), interpolation=cv2.INTER_AREA)

            frame_count += 1

            ret, jpeg = cv2.imencode('.jpg', overlay_image)
            frame = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
