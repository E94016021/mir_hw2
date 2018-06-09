import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from dataset import BallroomData
from tempogram import get_tempo_distribu


def get_tempo_info(file_number):
    # get data
    d = BallroomData()

    # wav name
    wav_name = d.file_name(file_number)
    # ground truth
    aaagt_bpm = d.get_gt_bpm(file_number)
    # load file for librosa
    y, sr = d[file_number]

    onset_env = librosa.onset.onset_strength(y, sr=sr)
    # Static tempo
    aaatempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)

    # Dynamic tempo
    dtempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr, aggregate=None)
    # Dynamic tempo distribution
    zapple = get_tempo_distribu(dtempo)
    aaatempo_list = zapple[0]
    aaatempo_cnt = zapple[1]

    # --- print info ---
    print("filename = ", wav_name)
    print("gt = ", aaagt_bpm)
    print("static = ", aaatempo[0])
    print("----- guess ------ ------")
    dis_lan = len(aaatempo_cnt)
    for i in range(dis_lan):
        print("%18.14f" % aaatempo_list[i], "%6d" % aaatempo_cnt[i])
        # print(str(aaatempo_list[i]), str(aaatempo_cnt[i]))
    print("----- ----- ------ ------\n\n")
    # --- ----- ---- ---

    return aaagt_bpm, aaatempo, aaatempo_list, aaatempo_cnt


if __name__ == '__main__':

    d = BallroomData()
    total = 0

    for file_number in range(len(d) - 1):
        # ground truth
        aaagt_bpm = d.get_gt_bpm(file_number)
        if aaagt_bpm == 176:
            # wav name
            wav_name = d.file_name(file_number)
            # ground truth
            aaagt_bpm = d.get_gt_bpm(file_number)
            # load file for librosa
            y, sr = d[file_number]

            onset_env = librosa.onset.onset_strength(y, sr=sr)
            # Static tempo
            aaatempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)

            # Dynamic tempo
            dtempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr, aggregate=None)
            # Dynamic tempo distribution
            zapple = get_tempo_distribu(dtempo)
            aaatempo_list = zapple[0]
            aaatempo_cnt = zapple[1]

            # --- print info ---
            print("filename = ", wav_name)
            print("gt = ", aaagt_bpm)
            print("static = ", aaatempo[0])
            print("----- guess ------ ------")
            dis_lan = len(aaatempo_cnt)
            for i in range(dis_lan):
                print("%18.14f" % aaatempo_list[i], "%6d" % aaatempo_cnt[i])
                # print(str(aaatempo_list[i]), str(aaatempo_cnt[i]))
            print("----- ----- ------ ------\n\n")
            # --- ----- ---- ---
            total +=1
    print("total = ",total)

    # # -----------
    # # test
    # for i in range(10):
    #     a, b, c, d = get_tempo_info(i)
    # # -----------

    # # get data
    # d = BallroomData()
    #
    # file_number = 1

    #
    # # wav name
    # wav_name = d.file_name(file_number)
    # # ground truth
    # aaagt_bpm = d.get_gt_bpm(file_number)
    # # load file for librosa
    # y, sr = d[file_number]
    #
    # onset_env = librosa.onset.onset_strength(y, sr=sr)
    # # Static tempo
    # aaatempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
    # print(".")
    #
    # # Dynamic tempo
    # dtempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr, aggregate=None)
    # # Dynamic tempo distribution
    # zapple = get_tempo_distribu(dtempo)
    # aaatempo_list = zapple[0]
    # aaatempo_cnt = zapple[1]

    print(".")
