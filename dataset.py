import os
import librosa
import librosa.display


# import matplotlib.pyplot as plt
# import numpy as np
#
# from mir_hw2_q1 import get_two_tempo, ALOTC


class BallroomData():
    """Face Landmarks dataset."""

    def __init__(self, transform=None):
        file_list_txt = "./BallroomData/allBallroomFiles"
        data_path = "./BallroomData/"

        with open(file_list_txt, newline='') as f:
            lines = f.readlines()

        self.files = [os.path.join(data_path, line[2:-1]) for line in lines]
        self.transform = transform

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        aud, sr = librosa.load(self.files[idx])

        if self.transform:
            aud = self.transform(aud)
        return aud, sr

    def get_gt_bpm(self, idx):
        f = self.files[idx].split("/")
        text_file = str(f[len(f) - 1].split('.')[0]) + ".bpm"
        r = "./BallroomAnnotations/ballroomGroundTruth/"
        with open(r + text_file, newline='') as b:
            bpm = int(b.readline().split("\n")[0])
        return bpm

    def file_name(self, idx):
        f = self.files[idx].split("/")
        return f[len(f) - 1]

    def genre_rng(self, name):
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

    d = BallroomData()
    t = "Tango"
    h, t = d.genre_rng(t)
    for file_number in range(h, t):
        print("%4d" % file_number, d.files[file_number])

    # d = BallroomData
    # genres = ["Cha Cha", "Jive", "Quickstep", "Rumba", "Samba", "Tango", "Viennese Waltz", "Slow Waltz"]
    # for genre_name in genres:
    #     rng_h, rng_t = d.genre_rng(genre_name)
    #     # for file_number in range(rng_h, rng_t):
    #     #     t_1, t_2, gt = get_two_tempo(file_number)
    #     #     print(t_1, t_2, gt)
    #     #     p = ALOTC(t_1, t_2, gt)
    #     #     print(p)
