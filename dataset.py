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
