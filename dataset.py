from torch.utils.data import Dataset
import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


class BallroomData(Dataset):
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

d = BallroomData()

