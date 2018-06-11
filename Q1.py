import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from dataset import BallroomData
from tempogram import fourier_tempogram
import librosa.display


dataset = BallroomData()

aud, sr = dataset[0]

D = fourier_tempogram(aud)

# plt.imshow(D)
librosa.display.specshow(D[20:,:])
plt.show()


# TODO: find peak (T1,T2)













