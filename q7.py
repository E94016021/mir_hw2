import numpy as np
from dataset import BallroomData
import librosa.display


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


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


if __name__ == '__main__':

    dataset = BallroomData()
    # dataset = StdData()

    P_total = []
    R_total = []
    F_total = []
    genres = ["Cha Cha", "Slow Waltz"]
    for genre in genres:
        rng_h, rng_t = qui_genre_rng(genre)
        print(genre)
        for song_id in range(rng_h,rng_t):

            aud, sr = dataset[0]

            bpm = librosa.beat.tempo(aud)
            beats_gt, beats_num = dataset.get_gg(song_id)
            print("bpm =", bpm, "gt =", dataset.get_gt_bpm(song_id), end=',')

            onset_frames = librosa.onset.onset_detect(y=aud, sr=sr)
            librosa.frames_to_time(onset_frames, sr=sr)
            o_env = librosa.onset.onset_strength(aud, sr=sr)
            # o_env = scipy.signal.medfilt(o_env,3)
            o_env = sigmoid(o_env * 0.5)

            tempo, beats = librosa.beat.beat_track(onset_envelope=o_env, sr=sr)

            times = librosa.frames_to_time(np.arange(len(o_env)), sr=sr)
            onset_frames = librosa.onset.onset_detect(onset_envelope=o_env, sr=sr)

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

            print("P:%4.4f" % P, "R:%4.4f" % R, "F:%4.4f" % F)

        print("\nP: %4.4f R: %4.4f F: %4.4f" % (np.average(P_total), np.average(R_total), np.average(R_total)))
