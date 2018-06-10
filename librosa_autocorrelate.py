import librosa
import matplotlib.pyplot as plt

y, sr = librosa.load(librosa.util.example_audio_file(), offset=20, duration=10)
k = librosa.autocorrelate(y)
plt.plot(y)
plt.title('y')
plt.subplot(4, 1, 1)
plt.plot(k)
plt.title('k')
plt.subplot(4, 1, 2)


odf = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512)
plt.plot(odf)
plt.title('odf')
plt.subplot(4, 1, 3)
ac = librosa.autocorrelate(odf, max_size=4 * sr / 512)
plt.plot(ac)
plt.title('ac')
plt.subplot(4, 1, 4)
plt.show()

print(".")
