import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from dataset import BallroomData, StdData
from tempogram import fourier_tempogram
import librosa.display
import scipy.signal


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


dataset = BallroomData()
# dataset = StdData()

song_id = 10

aud, sr = dataset[0]

bpm = librosa.beat.tempo(aud)
beats_gt = dataset.get_gg(song_id)
print(bpm, dataset.get_gt_bpm(song_id))

onset_frames = librosa.onset.onset_detect(y=aud, sr=sr)
librosa.frames_to_time(onset_frames, sr=sr)
o_env = librosa.onset.onset_strength(aud, sr=sr)
# o_env = scipy.signal.medfilt(o_env,3)
o_env = sigmoid(o_env * 0.5)

tempo, beats = librosa.beat.beat_track(onset_envelope=o_env, sr=sr)

times = librosa.frames_to_time(np.arange(len(o_env)), sr=sr)
onset_frames = librosa.onset.onset_detect(onset_envelope=o_env, sr=sr)

plt.figure()
plt.title('Power spectrogram')

# D = librosa.stft(aud)
# ax1 = plt.subplot(2, 1, 1)
# librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max),
#                          x_axis='time', y_axis='log')
# plt.subplot(2, 1, 2, sharex=ax1)

plt.plot(times, o_env, label='Onset strength')

# plt.vlines(times[onset_frames], 0, o_env.max(), color='r', alpha=0.9,
#            linestyle='--', label='Onsets')

plt.vlines(times[beats], 0, 1, alpha=0.5, color='r',
           linestyle='--', label='Beats')

beats = np.array(beats)
beat_onset_strength = o_env[beats]+o_env[beats+1]+o_env[beats-1]



# peaks = scipy.signal.find_peaks_cwt(beat_onset_strength, widths=np.arange(1,2))

l = len(beat_onset_strength)

peaks = [i for i in range(1, l - 1)
         if beat_onset_strength[i] > beat_onset_strength[i - 1] and
         beat_onset_strength[i] > beat_onset_strength[i + 1]]

# plt.plot(beat_onset_strength)
# plt.scatter(peaks, beat_onset_strength[peaks])

down_beats = beats[peaks]

# plt.vlines(times[down_beats], 0, 1, alpha=0.5, color='r',
#            linestyle='--', label='Beats')



plt.vlines(beats_gt, 0, 1, alpha=0.5, color='g',
           linestyle='--', label='Beats')


plt.axis('tight')
plt.legend(frameon=True, framealpha=0.75)
plt.show()
