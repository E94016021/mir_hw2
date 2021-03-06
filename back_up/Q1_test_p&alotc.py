import os
import numpy as np
from dataset import BallroomData
from tempogram import fourier_tempogram
import librosa.display
import scipy.signal
from tempogram import get_tempo_distribu


def f_get_two_tempo_total(tempo_list, tempo_cnt):
    '''
    only for mir hw q1

    :param file_number:
    :return:
    '''
    try:
        # cases of only ine guess
        if len(tempo_cnt) == 1:
            if tempo_list[0] > 125:
                t_1 = tempo_list[0]
                t_2 = tempo_list[0] / 2
            else:
                t_1 = tempo_list[0] * 2
                t_2 = tempo_list[0]
        else:
            idx_max = tempo_cnt.index(max(tempo_cnt))
            value_max = tempo_list[idx_max]

            sec_cnt = tempo_cnt.copy()
            sec_cnt[idx_max] = -1
            idx_sec = sec_cnt.index(max(sec_cnt))
            value_sec = tempo_list[idx_sec]
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

            return t_1, t_2
    except Exception as e:
        print(e)


def f_get_two_tempo(D, t, sr_new):
    peaks = scipy.signal.find_peaks_cwt(D[40:, t], widths=np.arange(1, 10))

    peak_values = [D[40:, t][peak] for peak in peaks]
    pair = list(zip(peaks, peak_values))
    pair.sort(key=lambda x: x[1], reverse=True)

    T1_idx = pair[0][0] + 40  # <40 bpm not usual
    T2_idx = pair[1][0] + 40

    T1_intensity = pair[0][1]  # F(n,t_1)
    T2_intensity = pair[1][1]

    sr = sr_new
    hz_per_idx = sr / 2 / D.shape[0]  # /2 : knikes freq.
    bpm_per_idx = hz_per_idx * 60
    # y= ax+b

    a = 3.6  # empirical
    b = 0
    '''
    click is truth
    171/47.67487108013937 = 3.586795226201168
    160/44.8704668989547 = 3.5658198155216287
    134/37.85945644599303 = 3.539406335406653
    120/32.95174912891986 =3.641688322234855
    78/too dirty (drum sounds)
    60/32.95174912891986
    '''

    # print("bpm_per_idx = ", end='')
    # print(bpm_per_idx)

    # TODO: find peak (T1,T2)

    return (T1_idx * bpm_per_idx * a + b, T2_idx * bpm_per_idx * a + b), (T1_intensity, T2_intensity)


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


def ALOTC(t_1, t_2, gt):
    gt = int(gt)
    if abs((gt - t_1) / gt) <= 0.08 or abs((gt - t_2) / gt) <= 0.08:
        p = 1
    else:
        p = 0
    return p


if __name__ == "__main__":

    d = BallroomData()
    # for test
    clicks = ["60.mp3", "78.mp3", "120.mp3", "134.mp3", "160.mp3", "171.mp3"]

    for name in clicks:
        print(name)
        aud, sr = librosa.load(os.path.join(".", "click", name))
        gt = name.split(".mp3")[0]

        total_time = aud.shape[0] / sr

        D = fourier_tempogram(aud)

        s = D.shape[1]  # 2048 22050

        f_tempo_list = []

        for t in range(D.shape[1]):
            # get every most tempo and list them
            f_tempo_list.append(f_get_two_tempo(D, t, total_time)[0][0])

        # get t1 t2 by using the most exist
        tempo_list, tempo_cnt = get_tempo_distribu(f_tempo_list)
        t_1, t_2 = f_get_two_tempo_total(tempo_list, tempo_cnt)

        print("gt =", gt, "t1 =", t_1, " t2 =", t_2)

        # calculat saliency
        ps = []

        for time in range(D.shape[1]):
            # fet ft
            ft1, ft2 = get_two_f_t(D, time, total_time, t_1, t_2)
            # get p-score
            ps.append(p_score(t_1, t_2, ft1, ft2, gt))

        # print ps list
        print(ps)

        # get the p-score ave,
        p_total = sum(ps)
        p_overall = p_total / D.shape[1]
        alotc = ALOTC(t_1, t_2, gt)

        print("p_sum =", p_total, "time =", D.shape[1])
        print("P-score =", p_overall)
        print("ALOTC-score=", alotc)
        print(".")
