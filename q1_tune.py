import os
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from dataset import BallroomData
from tempogram import fourier_tempogram
import librosa.display
import scipy.signal


def f_get_two_tempo(D, t, sr_new):
    peaks = scipy.signal.find_peaks_cwt(D[40:, t], widths=np.arange(1, 10))

    peak_values = [D[40:, t][peak] for peak in peaks]
    pair = list(zip(peaks, peak_values))
    pair.sort(key=lambda x: x[1], reverse=True)

    T1_idx = pair[0][0] + 40  # <40 bpm not usual
    T2_idx = pair[1][0] + 40

    T1_intensity = pair[0][1]  # F(n,t_1)
    T2_intensity = pair[1][1]

    sr = D.shape[1] / sr_new * 32
    hz_per_idx = sr / 2 / D.shape[0]
    bpm_per_idx = hz_per_idx * 60

    '''
    60/31.23999255259728 = 1.9206150545324514
    78/41.21020294172407 = 1.892735158579561
    120/63.809346490411464 = 1.8806022408963587
    134/71.12083410910445 = 1.8841173852718658
    160/84.4144479612735 = 1.8954101325569601
    171/90.39657419474958 = 1.8916646070192784
    mean = 1.8941907631427457   
    '''

    # y= ax+b
    a = 1.8941907631427457  # empirical
    b = 0


    # print("bpm_per_idx = ", end='')
    # print(bpm_per_idx)

    # TODO: find peak (T1,T2)

    return (T1_idx * bpm_per_idx * a + b, T2_idx * bpm_per_idx * a + b), (T1_intensity, T2_intensity)

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

        for t in range(D.shape[1]):
            print("f_get_two_tempo", end=' : ')
            print("- - - - - - - - - - - - - - - - - - - - - - - - - - "
                  "(t%d)" % t, f_get_two_tempo(D, t, total_time))

        # print("gt = ", end='')

        # print(dataset.get_gt_bpm(song_id))

        # librosa.display.specshow(D[40:, :])
        # plt.title(click)
        # plt.show()

        print(".")
