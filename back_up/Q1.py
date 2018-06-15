import librosa.display
import numpy as np
from dataset import BallroomData
from tempogram import fourier_tempogram
import librosa.display
import scipy.signal
from tempogram import get_tempo_distribu


def f_get_two_tempo_tatal(tempo_list, tempo_cnt):
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

    sr = sr_new
    hz_per_idx = sr / 2 / D.shape[0]  # /2 : knikes freq.
    bpm_per_idx = hz_per_idx * 60

    D = D[40:100, t]
    peaks = scipy.signal.find_peaks_cwt(D, widths=np.arange(1, 10))+40

    # peaks = [idx for idx in peaks if idx > 10 or idx <100]

    peak_values = [D[:, t][peak] for peak in peaks]
    pair = list(zip(peaks, peak_values))
    pair.sort(key=lambda x: x[1], reverse=True)

    T1_idx = pair[0][0]   # <40 bpm not usual
    T2_idx = pair[1][0]

    T1_intensity = pair[0][1]  # F(n,t_1)
    T2_intensity = pair[1][1]



    # print("bpm_per_idx = ", end='')
    # print(bpm_per_idx)

    # TODO: find peak (T1,T2)

    return (T1_idx * bpm_per_idx, T2_idx * bpm_per_idx ), (T1_intensity, T2_intensity)


'''
click is truth
171/47.67487108013937 = 3.586795226201168
160/44.8704668989547 = 3.5658198155216287
134/37.85945644599303 = 3.539406335406653
120/32.95174912891986 =3.641688322234855
78/too dirty (drum sounds)
60/32.95174912891986

'''

if __name__ == "__main__":
    d = BallroomData()

    song_id = 0

    # 50

    aud, sr = d[song_id]
    total_time = aud.shape[0] / sr

    D = fourier_tempogram(aud)

    s = D.shape[1]  # 2048 20050

    tempo_list = []

    for t in range(D.shape[1]):
        tempo_list.append(f_get_two_tempo(D, t, total_time)[0][0])
        # print("f_get_two_tempo", end=' : ')
        # print("- - - - - - - - - - - - - - - - - - - - - - - - - - "
        #       "(t%d)" % t, f_get_two_tempo(D, t, total_time))
    print(".")
    tempo_list, tempo_cnt = get_tempo_distribu(tempo_list)
    t_1, t_2 = f_get_two_tempo_tatal(tempo_list, tempo_cnt)
    print("t1 = ", t_1, " t2 = ", t_2)

    # print(dataset.get_genre(song_id))
    print("gt = ", end='')
    print(d.get_gt_bpm(song_id))

    librosa.display.specshow(D[20:, :])
    # plt.show()

    print(".")
