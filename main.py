import posenet
import tensorflow as tf
import cv2
import argparse
import numpy as np

import time
import squat
import ready
from speechRecognition import tts
np.set_printoptions(threshold=np.inf, linewidth=np.inf)

# parser = argparse.ArgumentParser()
# parser.add_argument('--model', type=int, default=101)
# parser.add_argument('--cam_id', type=int, default=0)
# parser.add_argument('--cam_width', type=int, default=1280)
# parser.add_argument('--cam_height', type=int, default=720)
# parser.add_argument('--scale_factor', type=float, default=0.7125)
# parser.add_argument('--file', type=str, default=None,
#                     help="Optionally use a video file instead of a live camera")
# args = parser.parse_args()

args = {"model": 101, "scale_factor": 1.0, "notxt": True, "image_dir": './images',
        "output_dir": './output'}
position = ["코", "왼쪽눈", "오른쪽눈", "왼쪽귀", "오른쪽귀", "왼쪽어깨", "오른쪽어깨", "왼쪽팔꿈치", "오른쪽팔꿈치",
            "왼쪽손목", "오른쪽손목", "왼쪽골반부위", "오른쪽골반부위", "왼쪽무릎", "오른쪽무릎", "왼쪽발목", "오른쪽발목"]

# 철추상 : Spine At The Shoulder , 척추중 : Middle Of The Spine , 척추하 : Base Of Spine
spine_position = ["척추상", "척추중", "척추하"]

# spine position을 구하기 위해 평균 구하는 함수.


def getAverage(pos, n):
    x, y = 0, 0

    for i in range(n):
        x += pos[i][0]
        y += pos[i][1]

    return [x/n, y/n]


def main():
    with tf.Session() as sess:
        model_cfg, model_outputs = posenet.load_model(args['model'], sess)
        output_stride = model_cfg['output_stride']
        # 내장 캠 : 0 , 외장 캠 : 1
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 360)

        start = time.time()
        frame_count = 0
        cnt = 0
        cycle = 2
        init = True
        init2 = False
        init3 = False

        exerciseCode = ready.selectExercise()

        while True:
            cnt += 1
            input_image, display_image, output_scale = posenet.read_cap(
                cap, scale_factor=args['scale_factor'], output_stride=output_stride)

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

            if(cnt == 1):
                tts.q.put("10초 후에 시작합니다. 자리를 잡아주세요.")

            if (cnt % cycle == 0):
                if(init):
                    if(cnt > 30 and ready.isReady(keypoint_coords[0])):
                        init = False
                        init2 = True
                elif(init2):
                    if(ready.isSide(keypoint_coords[0])):
                        init2 = False
                        init3 = True
                        if exerciseCode == 1:
                            squat.setting(exerciseCode)
                            tts.q.put("스쿼트란,,,,,, 설명")
                            tts.q.put("자세를 잡아주세요")
                elif(init3):
                    if exerciseCode == 1:
                        if(squat.postureCorrection(keypoint_coords[0])):
                            tts.q.put("10초 후 카운트를 시작합니다. 5회 반복해주세요.")
                            cnt = 2
                            init3 = False
                else:
                    if exerciseCode == 1:
                        if(cnt == 30):
                            tts.q.put("시작해주세요.")
                        elif(cnt > 30 and squat.counting(keypoint_coords[0])):
                            if squat.CNT == 5:
                                tts.q.put("스쿼트 5회를 마쳤습니다. 수고하셨습니다.")
                                break

            # TODO this isn't particularly fast, use GL for drawing and display someday...
            overlay_image = posenet.draw_skel_and_kp(
                display_image, pose_scores, keypoint_scores, keypoint_coords,
                min_pose_score=0.15, min_part_score=0.1)

            overlay_image = cv2.resize(overlay_image, dsize=(
                640, 360), interpolation=cv2.INTER_AREA)
            cv2.imshow('posenet', overlay_image)
            frame_count += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        print('Average FPS: ', frame_count / (time.time() - start))


if __name__ == "__main__":
    main()
