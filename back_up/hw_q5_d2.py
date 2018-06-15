import librosa
import librosa.display
from dataset import BallroomData
from tempogram import get_tempo_distribu
import time


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

    # # --- print info ---
    # print("filename = ", wav_name)
    # print("gt = ", aaagt_bpm)
    # print("static = ", aaatempo[0])
    # print("----- guess ------ ------")
    # dis_lan = len(aaatempo_cnt)
    # for i in range(dis_lan):
    #     print("%18.14f" % aaatempo_list[i], "%6d" % aaatempo_cnt[i])
    #     # print(str(aaatempo_list[i]), str(aaatempo_cnt[i]))
    # print("----- ----- ------ ------\n\n")
    # # --- ----- ---- ---

    return aaagt_bpm, aaatempo, aaatempo_list, aaatempo_cnt


def ac_get_two_tempo(file_number):
    '''
    only for mir hw q1

    :param file_number:
    :return:
    '''
    # get info
    ground_truth_bpm, static_tempo, dynamic_tempo_list, dynamic_tempo_cnt = get_tempo_info(file_number)

    try:
        # cases of only ine guess
        if len(dynamic_tempo_cnt) == 1:
            if dynamic_tempo_list[0] > 125:
                t_1 = dynamic_tempo_list[0]
                t_2 = dynamic_tempo_list[0] / 2
            else:
                t_1 = dynamic_tempo_list[0] * 2
                t_2 = dynamic_tempo_list[0]
        else:
            idx_max = dynamic_tempo_cnt.index(max(dynamic_tempo_cnt))
            value_max = dynamic_tempo_list[idx_max]

            sec_cnt = dynamic_tempo_cnt.copy()
            sec_cnt[idx_max] = -1
            idx_sec = sec_cnt.index(max(sec_cnt))
            value_sec = dynamic_tempo_list[idx_sec]
            # TODO: why lists connnect ? why dynamic_tempo_cnt change with sec_cnt?

            if value_max >= value_sec:
                t_1 = value_sec
                t_2 = value_max
            else:
                t_1 = value_max
                t_2 = value_sec
            #
            # print(dynamic_tempo_cnt)
            # print(sec_cnt)
            # print(idx_max)
            # print(idx_sec)
            # print(".")

            return t_1, t_2, ground_truth_bpm
    except Exception as e:
        print(e)


def qui_genre_rng(name):
    # TODO: return tuple can't fit in for range QQ
    '''
    use like this (eg.Tango)

    h, t = d.genre_rng("Tango")
    for file_number in range(h, t):
        print("%4d" % file_number, d.files[file_number])

    :param name:
    :return:
    '''
    if name == "Jive":
        return 0, 60
    elif name == "Quickstep":
        return 60, 142
    elif name == "Tango":
        return 142, 228
    elif name == "Waltz" or name == "Slow Waltz":
        return 228, 338
    elif name == "Slow Waltz":
        return 228, 338
    elif name == "VienneseWaltz" or name == "Viennese Waltz":
        return 338, 403
    elif name == "Samba":
        return 403, 489
    elif name == "ChaChaCha" or name == "Cha Cha":
        return 489, 600
    elif name == "Rumba":
        return 600, 698
    else:
        print("!! Wrong Genre Name !!")
        return 0, 0


def relative_saliency_of_t1(t_1, t_2):
    # TODO: unclear
    s_1 = t_1 / (t_1 + t_2)
    return s_1


def ALOTC_d2(t_1, t_2, gt):
    t_1, t_2 = t_1 / 2, t_2 / 2
    if abs((gt - t_1) / gt) <= 0.08 or abs((gt - t_2) / gt) <= 0.08:
        p = 1
    else:
        p = 0
    return p


def p_score_d2(t_1, t_2, gt):
    t_1, t_2 = t_1 / 2, t_2 / 2
    gt = int(gt)
    saliency = t_1 / (t_1 + t_2)

    if abs((gt - t_1) / gt) <= 0.08:
        tt1 = 1
    else:
        tt1 = 0
    if abs((gt - t_2) / gt) <= 0.08:
        tt2 = 1
    else:
        tt2 = 0
    p = saliency * tt1 + (1 - saliency) * tt2

    return p


if __name__ == '__main__':
    tStart = time.time()
    try:
        # d = BallroomData()
        genres = ["Cha Cha", "Jive", "Quickstep", "Rumba", "Samba", "Tango", "Viennese Waltz", "Slow Waltz"]
        genres_ALOTC = [0, 0, 0, 0, 0, 0, 0, 0]
        g_id = 0
        for genre_name in genres:
            try:
                total_p = 0
                total_cnt = 0
                print(genre_name)
                rng_h, rng_t = qui_genre_rng(genre_name)

                for file_number in range(rng_h, rng_t):
                    try:
                        t_1, t_2, gt = ac_get_two_tempo(file_number)
                        p = ALOTC_d2(t_1, t_2, gt)
                        total_p += p
                        total_cnt += 1

                        print("%4d" % file_number, "%18.14f" % t_1, "%18.14f" % t_2, "%3d" % gt, end='')
                        print(" - - - - %1d" % p)

                    except Exception as e:
                        print("- - - file number %d error :" % file_number, e, " - - -")
                print("- - - - - - - - - - - - - - - - - - - - - - ", genre_name,
                      "ave. ALOTC-score =", total_p / total_cnt)
                print(rng_t, rng_h, total_cnt)
                print("fail files cnt =", rng_t - rng_h - total_cnt)

                genres_ALOTC[g_id] = total_p / total_cnt
                g_id += 1

            except Exception as e:
                print(genre_name, "genre error :", e)
    except Exception as e:
        print("main error :", e)

    print(genres)
    print(genres_ALOTC)
    tEnd = time.time()
    print("runTime = ", tEnd - tStart)
