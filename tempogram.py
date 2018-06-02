import numpy as np
import librosa


def f_tempogram(y: np.ndarray):
    D = librosa.stft(y)
    print(D.shape)
    D2 = np.abs(np.diff(D, axis=1))
    D3 = (D2 > 0).astype(float) * D2

    return D3


def delta_spectral(y: np.ndarray) -> np.ndarray:
    D = f_tempogram(y)

    return np.sum(D, axis=0)


def ac_tempogram(y: np.ndarray) -> np.ndarray:
    D = f_tempogram(y) ** 2

    return librosa.istft(D)


if __name__ == "__main__":
    from dataset import BallroomData
    import matplotlib.pyplot as plt

    d = BallroomData()
    aud, sr = d[1]

    #test1
    D = f_tempogram(aud)

    plt.imshow(D)
    plt.show()

    # test2
    D2 = delta_spectral(aud)

    plt.plot(D2)
    plt.show()

    # test3
    D3 = ac_tempogram(aud)

    plt.plot(D3)
    plt.show()
