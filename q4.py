import librosa
import librosa.display
from dataset import BallroomData
from tempogram import get_tempo_distribu
from tempogram import fourier_tempogram
import time


def get_tempo_info(file_number, d):
    # # get data
    # d = BallroomData()

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


def ac_get_two_tempo(file_number, d):
    '''
    only for mir hw q1

    :param file_number:
    :return:
    '''
    # get info
    ground_truth_bpm, static_tempo, dynamic_tempo_list, dynamic_tempo_cnt = get_tempo_info(file_number, d)

    try:
        # cases of only ine guess
        if len(dynamic_tempo_cnt) == 1:
            if dynamic_tempo_list[0] > 125:
                t_1 = dynamic_tempo_list[0] / 2
                t_2 = dynamic_tempo_list[0]
            else:
                t_1 = dynamic_tempo_list[0]
                t_2 = dynamic_tempo_list[0] * 2
        else:
            idx_max = dynamic_tempo_cnt.index(max(dynamic_tempo_cnt))
            value_max = dynamic_tempo_list[idx_max]

            sec_cnt = dynamic_tempo_cnt.copy()
            sec_cnt[idx_max] = -1
            idx_sec = sec_cnt.index(max(sec_cnt))
            value_sec = dynamic_tempo_list[idx_sec]

            # make big and small
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
        print("ac_get_two_tempo ERROR", e)


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


def get_t_idx(t, sr_new, D):
    sr = sr_new
    hz_per_idx = sr / 2 / D.shape[0]  # /2 : knikes freq.
    bpm_per_idx = hz_per_idx * 60

    r = t / bpm_per_idx / 3.6

    idx = int(round(r, 0) - 40)

    return idx


def get_two_f_t(D, time, sr_new, t_1, t_2):
    t1_idx = get_t_idx(t_1, sr_new, D)
    t2_idx = get_t_idx(t_2, sr_new, D)

    t_idx = [t1_idx, t2_idx]

    for tempo in t_idx:
        peak_values = [D[40:, time][tempo] for tempo in t_idx]

    return peak_values[0], peak_values[1]


def ALOTC(t_1, t_2, gt):
    if abs((gt - t_1) / gt) <= 0.08 or abs((gt - t_2) / gt) <= 0.08:
        alotc = 1
    else:
        alotc = 0
    return int(alotc)


def p_score(t_1, t_2, f_t_1, f_t_2, gt):
    gt = int(gt)
    saliency = f_t_1 / (f_t_1 + f_t_2)

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
        data = BallroomData()
        genres = ["Cha Cha", "Jive", "Quickstep", "Rumba", "Samba", "Tango", "Viennese Waltz", "Slow Waltz"]
        genres_ALOTC = [0, 0, 0, 0, 0, 0, 0, 0]
        genres_ps = [0, 0, 0, 0, 0, 0, 0, 0]

        ans1_avg = [0, 0, 0, 0, 0, 0, 0, 0]
        ans2_avg = [0, 0, 0, 0, 0, 0, 0, 0]
        ans3_avg = [0, 0, 0, 0, 0, 0, 0, 0]

        g_id = 0
        for genre_name in genres:
            try:
                total_a = 0
                total_p = 0

                ans1_total = 0
                ans2_total = 0
                ans3_total = 0

                total_cnt = 0

                print(genre_name)
                rng_h, rng_t = qui_genre_rng(genre_name)

                for file_number in range(rng_h, rng_t):
                    try:

                        aud, sr = data[file_number]
                        D = fourier_tempogram(aud)
                        total_time = aud.shape[0] / sr

                        t_1, t_2, gt = ac_get_two_tempo(file_number, data)
                        alotc = ALOTC(t_1, t_2, gt)

                        p = 0
                        avg_p = 0
                        for ttt in range(D.shape[1]):
                            ft1, ft2 = get_two_f_t(D, ttt, total_time, t_1, t_2)
                            p += p_score(t_1, t_2, ft1, ft2, gt)

                        avg_p += p / D.shape[1]

                        ans1 = t_2 / t_1
                        ans2 = t_1 / gt
                        ans3 = t_2 / gt

                        total_a += alotc
                        total_p += avg_p

                        ans1_total += ans1
                        ans2_total += ans2
                        ans3_total += ans3

                        total_cnt += 1

                        print("id =%4d" % file_number, ", gt =%3d" % gt, ", t1 = %8.4f" % t_1, ", t2 =%8.4f" % t_2, end=' . ')
                        print("P-score = %4.4f" % avg_p, ", ALOTC = %d" % alotc,end=' . ')
                        print("t1/t2 = %4.4f" % ans1, ", t1/gt = %4.4f" % ans2, ", t2/gt = %4.4f" % ans3)


                    except Exception as e:
                        print("- - - file number %d error :" % file_number, e, " - - -")
                print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -",
                      genre_name, end=' : ')
                apple = total_p / total_cnt
                banana = total_a / total_cnt

                print("avg.P-score = %4.4f" % apple,
                      ", avg.ALOTC = %4.4f" % banana)

                genres_ALOTC[g_id] = apple
                genres_ps[g_id] = banana


                ans1_avg[g_id] = ans1_total / total_cnt
                ans2_avg[g_id] = ans2_total / total_cnt
                ans3_avg[g_id] = ans3_total / total_cnt
                print("- - - - - - - - - - - - - - - - - - - - - - - - - - - "
                      "- - - - - - - - - - - - - - - - - -",
                      "avg.t2/t1 = %4.4f" % ans1_avg[g_id])
                print("- - - - - - - - - - - - - - - - - - - - - - - - - - - "
                      "- - - - - - - - - - - - - - - - - -",
                      "avg.t1/gt = %4.4f" % ans2_avg[g_id])
                print("- - - - - - - - - - - - - - - - - - - - - - - - - - - "
                      "- - - - - - - - - - - - - - - - - -",
                      "avg.t2/gt = %4.4f" % ans3_avg[g_id])






                g_id += 1

            except Exception as e:
                print(genre_name, "genre error :", e)
    except Exception as e:
        print("main error :", e)

    for genre_idx in range(len(genres)):
        print("%15s" % genres[genre_idx],
              ": avg.P-score = %4.4f" % genres_ps[genre_idx],
              ", avg.ALOTC = %4.4f"% genres_ALOTC[genre_idx],
              "avg.t2/t1 = %4.4f" % ans1_avg[genre_idx],
              "avg.t1/gt = %4.4f" % ans2_avg[genre_idx],
              "avg.t2/gt = %4.4f" % ans3_avg[genre_idx])



    tEnd = time.time()
    print("runTime = ", tEnd - tStart)
