import numpy as np
import librosa
import librosa.display
import scipy.signal


def delta_spectral(y: np.ndarray):
    D = librosa.stft(y, n_fft=1024)
    print(D.shape)
    D2 = np.abs(np.diff(D, axis=1))
    D3 = (D2 > 0).astype(float) * D2

    return D3


def novel_curve_delta_spectral(y: np.ndarray) -> np.ndarray:
    D = delta_spectral(y)

    return np.sum(D, axis=0)


def fourier_tempogram(y):
    D = librosa.stft(novel_curve_delta_spectral(y), n_fft=512, hop_length=128)
    return np.abs(D)


def ac_tempogram(y: np.ndarray) -> np.ndarray:
    D = delta_spectral(y) ** 2
    D = librosa.istft(D, win_length=2048, hop_length=2048)
    return D.reshape(1025, -1)


def get_tempo_distribu(dtempo):
    bill_srt = np.sort(dtempo)

    tempo_list = []
    tempo_cnt = []
    ln = 0
    bd = 0

    for i in range(len(bill_srt) - 1):
        if bill_srt[i] != bill_srt[i + 1]:
            bd_old = bd
            bd = i + 1
            tempo_list.append(bill_srt[i])
            tempo_cnt.append(bd - bd_old)
            ln += 1
    tempo_list.append(bill_srt[len(bill_srt) - 1])
    tempo_cnt.append(len(bill_srt) - bd)

    return tempo_list, tempo_cnt


# def get_two_tempo(tempo):
#     # boundary of tempo from my Metronome = 30 ~ 250
#     # 30*2 = 60
#     # 250/2 =125
#     if tempo < 30:
#         print("tempo < 30")
#         return tempo, tempo * 2
#     elif tempo > 250:
#         print("tempo > 250")
#         return tempo, tempo / 2
#     elif tempo <= 125:
#         return tempo, tempo * 2
#     elif tempo > 125:
#         return tempo, tempo / 2
#     else:
#         print("ERROR : tempo = ", tempo)
#         return tempo, tempo * 2


if __name__ == "__main__":
    from dataset import BallroomData
    import matplotlib.pyplot as plt

    d = BallroomData()
    aud, sr = d[1]

    # # test1
    # D = novel_curve_delta_spectral(aud)
    #
    # plt.imshow(D)
    # plt.show()
    #
    # test2
    D2 = novel_curve_delta_spectral(aud)

    plt.plot(D2)
    plt.show()
    #
    # # test3
    # D3 = ac_tempogram(aud)
    #
    # plt.plot(D3)
    # plt.show()

    # #test4
    # D4 = fourier_tempogram(aud)
    # plt.subplot(2, 1, 1)
    # librosa.display.specshow(D4)

    # # test5
    # D5 = ac_tempogram(aud)
    #
    # plt.subplot(2, 1, 2)
    # plt.imshow(D5)
    # plt.show()