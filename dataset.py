from torch.utils.data import Dataset
import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


class BallroomData(Dataset):
    """Face Landmarks dataset."""

    def __init__(self, transform=None, ret_dict=False):
        self.file_list_txt = "./BallroomData/allBallroomFiles"
        self.data_path = "./BallroomData/"
        self.ground_path = "ballroomGroundTruth"
        self.genres = ["ChaChaCha", "Jive", "Quickstep", "Rumba", "Samba", "Tango", "VienneseWaltz", "Waltz"]
        self.ret_dict = ret_dict

        with open(self.file_list_txt, newline='') as f:
            lines = f.readlines()

        self.files = [os.path.join(self.data_path, line[2:-1]) for line in lines]
        self.transform = transform

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):

        aud, sr = librosa.load(self.files[idx])

        if self.transform:
            aud = self.transform(aud)

        if self.ret_dict:
            return {'aud': aud, 'sr': sr, 'genre': self.get_genre(idx), 'bpm': self.get_gt_bpm(idx)}
        else:
            return aud, sr

    def get_gt_bpm(self, idx):

        f = self.files[idx]
        file = f.replace(".wav", ".bpm")
        text_file = os.path.join(self.ground_path, os.path.split(file)[-1])
        with open(text_file, newline='') as b:
            bpm = int(b.readline().split("\n")[0])
        return bpm

    def file_name(self, idx):
        f = self.files[idx].split("/")
        return f[len(f) - 1]

    def get_genre(self, idx):

        file = self.files[idx]

        # print(file)
        for genre in self.genres:
            if file.find(genre) != -1:
                return genre

    def get_gg(self, idx):
        folder = "BallroomAnnotations-Q7"
        file = os.path.split(self.files[idx])[-1].replace(".wav", ".beats")
        file_path = os.path.join(folder, file)

        beats = []
        beat_num = []

        with open(file_path, newline='') as b:

            for line in b.readlines():
                try:
                    beats.append(float(line.split(" ")[0]))
                    beat_num.append(int(line.split(" ")[1]))
                except ValueError:
                    beats.append(float(line.split("\t")[0]))
                    beat_num.append(int(line.split("\t")[1].replace('\n', '')))

        return beats, beat_num


class BallroomDataGenre(BallroomData):
    def __init__(self, genre, ret_dict=False):
        super(BallroomDataGenre, self).__init__(ret_dict=ret_dict)
        self.files = [file for file in self.files if file.find(genre) != -1]


class StdData(Dataset):
    """Face Landmarks dataset."""

    def __init__(self, transform=None):
        self.data_path = "./std_data"
        fs = os.listdir(self.data_path)

        self.files = [os.path.join(self.data_path, f) for f in fs]

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        aud, sr = librosa.load(self.files[idx])

        return aud, sr

    def get_gt_bpm(self, idx):
        a = self.files[idx]
        a = os.path.split(a)[-1]
        a = int(a.replace(".mp3", ""))

        return a


if __name__ == "__main__":
    d = BallroomData()
    dd = BallroomDataGenre("Waltz")

    # print(d.get_gt_bpm(2))
    # d.get_gg(0)
