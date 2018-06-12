import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from dataset import BallroomData
from tempogram import fourier_tempogram
import librosa.display
import scipy.signal


def f_get_two_tempo(D, t, sr_new):
    sr = D.shape[1] / sr_new * 32
    hz_per_idx = sr / 2 / D.shape[0]
    bpm_per_idx = hz_per_idx * 60

    peaks_idx = scipy.signal.find_peaks_cwt(D[40:, t], widths=np.arange(1, 20))+40
    peak_values = [D[:, t][peak] for peak in peaks_idx]

    peaks_idx2tempo = list((peaks_idx) * bpm_per_idx)

    peaks_idx2tempo_bu = list(peaks_idx2tempo.copy())
    peak_values_bu = list(peaks_idx2tempo.copy())
    pair_bu = list(zip(peaks_idx2tempo_bu, peak_values_bu))
    pair_bu.sort(key=lambda x: x[1], reverse=True)

    for idx in range(len(peaks_idx2tempo)):
        v = peaks_idx2tempo[idx]
        # if v < 40 or v > 200:
        if v > 180:
            peaks_idx2tempo[idx] = -1
            peak_values[idx] = -1

    peaks_idx2tempo = list(filter(lambda out: out != -1, peaks_idx2tempo))
    peak_values = list(filter(lambda out: out != -1, peaks_idx2tempo))
    # print("id2tempo\n",peaks_idx2tempo)
    # print("value\n",peak_values)

    pair = list(zip(peaks_idx2tempo, peak_values))
    pair.sort(key=lambda x: x[1], reverse=True)

    # if no tempo in rng
    if len(pair) < 2:
        print("bpm_per_idx = ", end='')
        print(bpm_per_idx)
        return (pair_bu[0][0], pair_bu[1][0]), (pair_bu[0][1], pair_bu[1][1])


    try:

        T1_tempo = pair[0][0]  # <40 bpm not usual
        T2_tempo = pair[1][0]

        T1_intensity = pair[0][1]  # F(n,t_1)
        T2_intensity = pair[1][1]

        print("bpm_per_idx = ", end='')
        print(bpm_per_idx)

        # TODO: find peak (T1,T2)

        return (T1_tempo, T2_tempo), (T1_intensity, T2_intensity)

    except Exception as e:
        print(e)


def ff_get_two_tempo(D, t, total_time):
    peaks = scipy.signal.find_peaks_cwt(D[20:50, t], widths=np.arange(1, 5))

    peak_values = [D[20:, t][peak] for peak in peaks]
    pair = list(zip(peaks, peak_values))
    pair.sort(key=lambda x: x[1], reverse=True)

    T1_idx = pair[0][0] + 19
    T2_idx = pair[1][0] + 19

    T1_intensity = pair[0][1]
    T2_intensity = pair[1][1]

    if T1_idx + 1 == T2_idx or T1_idx - 1 == T2_idx:
        T2_idx = pair[2][0] + 19
        T2_intensity = pair[2][1] + 19

    sr = D.shape[1] / total_time * 32
    hz_per_idx = sr / 2 / D.shape[0]
    bpm_per_idx = hz_per_idx * 60
    # y= ax+b

    print(bpm_per_idx)

    # TODO: find peak (T1,T2)

    return (T1_idx * bpm_per_idx, T2_idx * bpm_per_idx), (T1_intensity, T2_intensity)


if __name__ == "__main__":
    dataset = BallroomData()

    # song_id = 3
    # # 50
    # aud, sr = dataset[song_id]

    clicks = ["60.mp3", "78.mp3", "120.mp3", "134.mp3", "160.mp3", "171.mp3"]
    # clicks = ["78.mp3", "120.mp3", "134.mp3", "160.mp3", "171.mp3"]
    for click in clicks:
        print("click =", click)

        aud, sr = librosa.load(os.path.join(".", "click", click))

        total_time = aud.shape[0] / sr

        D = fourier_tempogram(aud)  # 2048 20050

        '''
        click is truth
        171/47.67487108013937 = 3.586795226201168
        160/44.8704668989547 = 3.5658198155216287
        134/37.85945644599303 = 3.539406335406653
        120/32.95174912891986 =3.641688322234855
        78/too dirty (drum sounds)
        60/32.95174912891986
    
        '''

        for t in range(D.shape[1]):
            print("f_get_two_tempo", end=' : ')
            print("- - - - - - - - - - - - - - - - - - - - - - - - - - "
                  "(t%d)" % t, f_get_two_tempo(D, t, total_time))

        # print("gt = ", end='')

        # print(dataset.get_gt_bpm(song_id))

        librosa.display.specshow(D[40:, :])
        plt.title(click)
        plt.show()

        print(".")
