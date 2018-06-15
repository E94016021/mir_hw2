import numpy as np
from by_exeex.dataset import BallroomData
import librosa.display


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


dataset = BallroomData()
# dataset = StdData()

P_total = []
R_total = []
F_total = []


for song_id in range(len(dataset)):

    genre = dataset.get_genre(song_id)

    if genre != "Waltz":
        print(genre)
        continue

    aud, sr = dataset[0]

    bpm = librosa.beat.tempo(aud)
    beats_gt, beats_num = dataset.get_gg(song_id)
    print(bpm, dataset.get_gt_bpm(song_id))

    onset_frames = librosa.onset.onset_detect(y=aud, sr=sr)
    librosa.frames_to_time(onset_frames, sr=sr)
    o_env = librosa.onset.onset_strength(aud, sr=sr)
    # o_env = scipy.signal.medfilt(o_env,3)
    o_env = sigmoid(o_env * 0.5)

    tempo, beats = librosa.beat.beat_track(onset_envelope=o_env, sr=sr)

    times = librosa.frames_to_time(np.arange(len(o_env)), sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=o_env, sr=sr)

    # plt.figure()
    #
    # plt.title('Power spectrogram')
    #
    # plt.plot(times, o_env, label='Onset strength')
    #
    # plt.vlines(times[beats], 0, 1, alpha=0.5, color='r',
    #            linestyle='--', label='Beats')
    # plt.vlines(beats_gt, 0, 1, alpha=0.5, color='g',
    #            linestyle='--', label='Beats_GT')
    #
    # plt.axis('tight')
    # plt.legend(frameon=True, framealpha=0.75)
    # plt.show()

    beats = times[beats]


    def check_70ms(t, beats):
        idx = np.where(np.logical_and((t - 0.070) < beats, (t + 0.070) > beats))
        try:
            x = idx[0][0]
            return True
        except IndexError:
            return False

    TP = 0
    FN = 0
    FP = 0

    for beat in beats:
        if check_70ms(beat, beats_gt):
            TP += 1
        else:
            FP += 1

    for beat_gt in beats_gt:

        if check_70ms(beat_gt, beats):
            TP += 1
        else:
            FN += 1
    TP /= 2

    # print(TP, FP, FN)

    P = TP / (TP + FP)
    R = TP / (TP + FN)
    F = 2 * P * R / (P + R)

    P_total.append(P)
    R_total.append(R)
    F_total.append(F)


    print("P:", P, "R", R, "F", F)


print("P: %f R: %f F: %f" % (np.average(P_total),np.average(R_total),np.average(R_total)))