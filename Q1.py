import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from dataset import BallroomData, StdData
from tempogram import fourier_tempogram
import librosa.display
import scipy.signal


def get_T1T2(D, t,sr_new):
    peaks = scipy.signal.find_peaks_cwt(D[20:, t], widths=np.arange(1, 10))

    peak_values = [D[20:, t][peak] for peak in peaks]
    pair = list(zip(peaks, peak_values))
    pair.sort(key=lambda x: x[1], reverse=True)

    T1_idx = pair[0][0] + 19
    T2_idx = pair[1][0] + 19

    T1_intensity = pair[0][1]
    T2_intensity = pair[1][1]


    sr = sr_new
    hz_per_idx = sr/2/D.shape[0]
    bpm_per_idx = hz_per_idx * 60
    #y= ax+b

    a = 1.8181818
    b = 2.6363636

    print(bpm_per_idx)

    # TODO: find peak (T1,T2)

    return ((T1_idx*bpm_per_idx*a+b)*0.5, (T2_idx*bpm_per_idx*a+b)*0.5), (T1_intensity, T2_intensity)



dataset = BallroomData()
# dataset = StdData()

song_id = 300


#50

aud, sr = dataset[song_id]
total_time = aud.shape[0] / sr

sr_new = sr/2048


D = fourier_tempogram(aud)

for t in range(D.shape[1]):
    if t == 20:
        librosa.display.specshow(D[20:, :])
        plt.show()
    print(get_T1T2(D,t,total_time))
print(dataset.get_genre(song_id))
print(dataset.get_gt_bpm(song_id))

