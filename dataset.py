from torch.utils.data import Dataset
import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


class BallroomData(Dataset):
    """Face Landmarks dataset."""

    def __init__(self, transform=None):
        self.file_list_txt = "./BallroomData/allBallroomFiles"
        self.data_path = "./BallroomData/"
        self.ground_path = "ballroomGroundTruth"
        self.genres = ["ChaChaCha", "Jive", "Quickstep", "Rumba", "Samba", "Tango", "VienneseWaltz", "Waltz"]

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

        print(file)
        for genre in self.genres:
            if file.find(genre) != -1:
                return genre


if __name__ == "__main__":
    d = BallroomData()

    print(d.get_gt_bpm(0))
    print(d.get_genre(0))