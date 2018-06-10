# %matplotlib inline
import seaborn
import numpy, scipy, matplotlib.pyplot as plt, IPython.display as ipd
import librosa, librosa.display

if __name__ == "__main__":

    plt.rcParams['figure.figsize'] = (13, 5)

    x, sr = librosa.load('download.wav')
    ipd.Audio(x, rate=sr)

    hop_length = 200 # samples per frame
    onset_env = librosa.onset.onset_strength(x, sr=sr, hop_length=hop_length, n_fft=2048)

    frames = range(len(onset_env))
    t = librosa.frames_to_time(frames, sr=sr, hop_length=hop_length)

    plt.plot(t, onset_env)
    plt.xlim(0, t.max())
    plt.ylim(0)
    plt.xlabel('Time (sec)')
    plt.title('Novelty Function')
    plt.show()

    S = librosa.stft(onset_env, hop_length=1, n_fft=512)
    fourier_tempogram = numpy.absolute(S)

    librosa.display.specshow(fourier_tempogram, sr=sr, hop_length=hop_length, x_axis='time')

    #ac
    n0 = 100
    n1 = 500
    plt.plot(t[n0:n1], onset_env[n0:n1])
    plt.xlim(t[n0], t[n1])
    plt.xlabel('Time (sec)')
    plt.title('Novelty Function')

    tmp = numpy.log1p(onset_env[n0:n1])
    r = librosa.autocorrelate(tmp)

    plt.plot(t[:n1-n0], r)
    plt.xlim(t[0], t[n1-n0])
    plt.xlabel('Lag (sec)')
    plt.ylim(0)

    plt.plot(60/t[:n1-n0], r)
    plt.xlim(20, 200)
    plt.xlabel('Tempo (BPM)')
    plt.ylim(0)

    # librosa.feature.tempogram implements an autocorrelation tempogram
    tempogram = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr, hop_length=hop_length, win_length=400)
    librosa.display.specshow(tempogram, sr=sr, hop_length=hop_length, x_axis='time', y_axis='tempo')

    print(".")
