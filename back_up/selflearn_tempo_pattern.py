import librosa.display
import numpy as np
from dataset import BallroomData
from tempogram import get_tempo_distribu

'''
check for my inspiration of dynamic tempo make ground truth

'''


def mix_distribu(dtempo1=([0], [0]), dtempo2=([0], [0])):
    tempo_list1, tempo_cnt1 = dtempo1
    tempo_list2, tempo_cnt2 = dtempo2

    tempo_list = tempo_list1 + tempo_list2
    tempo_list = np.sort(tempo_list)

    head = []

    # this for tempo only one guess
    mi = 0

    for mi in range(len(tempo_list) - 1):

        a = tempo_list[mi]
        b = tempo_list[mi + 1]
        tf = a != b
        if tf:
            head = head + [tempo_list[mi]]

    head_list = head + [tempo_list[mi]]
    head_cnt = []
    head_cnt[:len(head_list)] = [0] * len(head_list)

    for i in range(len(head_list)):
        for x in range(len(tempo_list1)):
            if head_list[i] == tempo_list1[x]:
                head_cnt[i] = head_cnt[i] + tempo_cnt1[x]
        for y in range(len(tempo_list2)):
            if head_list[i] == tempo_list2[y]:
                head_cnt[i] = head_cnt[i] + tempo_cnt2[y]

    return head_list, head_cnt


if __name__ == '__main__':
    total_of_total = 0

    d = BallroomData()

    for target_tempo in range(119, 123, 1):

        t_zapple = [], []
        total = 0
        print("target tempo = ", target_tempo)

        for file_number in range(len(d) - 1):
            # ground truth

            aaagt_bpm = d.get_gt_bpm(file_number)
            if aaagt_bpm == target_tempo:
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

                # total
                t_zapple = mix_distribu(t_zapple, zapple)

                # --- print single file info ---
                # -------------
                # ------
                # --
                # -
                #
                #
                #
                print("\n\nfilename = ", wav_name)
                print("static = ", aaatempo[0])
                print("----- guess ------ ------")
                dis_len = len(aaatempo_cnt)
                for i in range(dis_len):
                    print("%18.14f" % aaatempo_list[i], "%6d" % aaatempo_cnt[i])
                    # print(str(aaatempo_list[i]), str(aaatempo_cnt[i]))
                print("----- ----- ------ ------")
                #
                #
                # -
                # --
                # -----
                #-----------
                #--------------------------------

                total += 1
        #
        #
        # -
        # --
        # ----
        # -------
        # -------------
        # print target tempo info ----------
        print("\n---match bpm: %d 's " % target_tempo, "total = %d " % total)
        t_list = t_zapple[0]
        t_cnt = t_zapple[1]

        dis_len = len(t_cnt)
        for ti in range(dis_len):
            print("%18.14f" % t_list[ti], "%6d" % t_cnt[ti])
        # -----------------
        # ----------
        # ---
        # -
        #
        #
        total_of_total += total
    print("toatal of total = ", total_of_total)
