import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

'''
example from librosa
https://librosa.github.io/librosa/generated/librosa.feature.tempogram.html

'''

if __name__ == "__main__":
    # example
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Compute local onset autocorrelation
    # y, sr = librosa.load(librosa.util.example_audio_file())
    y, sr = librosa.load("./BallroomData/ChaChaCha/Albums-Cafe_Paradiso-05.wav")
    hop_length = 512
    oenv = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
    tempogram = librosa.feature.tempogram(onset_envelope=oenv, sr=sr, hop_length=hop_length)

    # - - - - - - - - - - - - - -

    s_max = 0
    tempo_from_g = -1
    for x in range(1, len(tempogram)):
        gram = tempogram[x]
        s = sum(tempogram[x])
        if s > s_max:
            s_max = s
            tempo_from_g = x

    # - - - - - - - - - - - - - - - -

    # Compute global onset autocorrelation
    ac_global = librosa.autocorrelate(oenv, max_size=tempogram.shape[0])
    ac_global = librosa.util.normalize(ac_global)

    # Estimate the global tempo for display purposes
    # librosa.beat.tempo(ac_size=8.0) default length (in seconds) of the auto-correlation window
    tempo = librosa.beat.tempo(onset_envelope=oenv, sr=sr, hop_length=hop_length)[0]
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    plt.figure(figsize=(8, 8))
    plt.subplot(4, 1, 1)
    plt.plot(oenv, label='Onset strength')
    plt.xticks([])
    plt.legend(frameon=True)
    plt.axis('tight')
    plt.subplot(4, 1, 2)

    # We'll truncate the display to a narrower range of tempi
    librosa.display.specshow(tempogram, sr=sr, hop_length=hop_length, x_axis='time', y_axis='tempo')
    plt.axhline(tempo, color='w', linestyle='--', alpha=1, label='Estimated tempo={:g}'.format(tempo))
    plt.legend(frameon=True, framealpha=0.75)
    plt.subplot(4, 1, 3)
    x = np.linspace(0, tempogram.shape[0] * float(hop_length) / sr, num=tempogram.shape[0])
    plt.plot(x, np.mean(tempogram, axis=1), label='Mean local autocorrelation')
    plt.plot(x, ac_global, '--', alpha=0.75, label='Global autocorrelation')
    plt.xlabel('Lag (seconds)')
    plt.axis('tight')
    plt.legend(frameon=True)
    plt.subplot(4, 1, 4)

    # We can also plot on a BPM axis
    freqs = librosa.tempo_frequencies(tempogram.shape[0], hop_length=hop_length, sr=sr)
    plt.semilogx(freqs[1:], np.mean(tempogram[1:], axis=1), label='Mean local autocorrelation', basex=2)
    plt.semilogx(freqs[1:], ac_global[1:], '--', alpha=0.75, label='Global autocorrelation', basex=2)
    plt.axvline(tempo, color='black', linestyle='--', alpha=.8, label='Estimated tempo={:g}'.format(tempo))
    plt.legend(frameon=True)
    plt.xlabel('BPM')
    plt.axis('tight')
    plt.grid()
    plt.tight_layout()
    plt.show()

    print(".")
