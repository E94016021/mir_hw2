import librosa
import librosa.display
from by_exeex.dataset import BallroomDataGenre
from by_exeex.tempogram import get_tempo_distribu, ALOTC
import time


def get_tempo_info(d):
    """
    :param d: {'aud': aud, 'sr': sr, 'genre': self.get_genre(idx), 'bpm': self.get_gt_bpm(idx)}
    :return:
    """
    
    # ground truth
    tempo = d['bpm']
    
    # load file for librosa
    y, sr = d['aud'], d['sr']

    onset_env = librosa.onset.onset_strength(y, sr=sr)
    # Static tempo
    tempo_pred_static = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)

    # Dynamic tempo
    tempo_pred_dynamic = librosa.beat.tempo(onset_envelope=onset_env, sr=sr, aggregate=None)

    # Dynamic tempo distribution
    tempo_pred_dynamic_dist = get_tempo_distribu(tempo_pred_dynamic)
    tempo_cnt = tempo_pred_dynamic_dist[1]

    return tempo, tempo_pred_static, tempo_pred_dynamic, tempo_cnt


def ac_get_two_tempo(d):
    '''
    only for mir hw q1

    :param file_number:
    :return:
    '''

    # get info
    ground_truth_bpm, static_tempo, dynamic_tempo_list, dynamic_tempo_cnt = get_tempo_info(d)

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

        return t_1, t_2, ground_truth_bpm


if __name__ == '__main__':
    tStart = time.time()
    total_p = 0
    genres = ["ChaChaCha", "Jive", "Quickstep", "Rumba", "Samba", "Tango", "VienneseWaltz", "Waltz"]
    
    # store ALOTC score by dict
    genre_ALOTC = {}
    file_count = 0

    for genre in genres:

        d = BallroomDataGenre(genre, ret_dict=True)
        for file_number, gg in enumerate(d):

            # gg is a data dict, include aud, sr, bpm, genre... information
            data = ac_get_two_tempo(gg)

            if data is not None:
                p = ALOTC(*data)
            else:
                print("fail")
                continue
            total_p += p
            file_count += 1
            print("%4d" % file_number, data, end='')
            print(" - - - - %1d" % p, flush=True)

        genre_ALOTC[genre] = total_p / file_count

        print("- - - - - - - - - - - - - - - - - - - - - - ")
        print(genre, "ave. ALOTC-score =", genre_ALOTC)
        print("fail files cnt =", len(d) - file_count)

    print(genre_ALOTC)
    tEnd = time.time()
    print("runTime = ", tEnd - tStart)
