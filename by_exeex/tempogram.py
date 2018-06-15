import numpy as np
import librosa
import librosa.display


def delta_spectral(y: np.ndarray):
    D = librosa.stft(y, n_fft=512)
    D2 = np.abs(np.diff(D, axis=1))
    D3 = (D2 > 0).astype(float) * D2

    return D3

def novel_curve_delta_spectral(y: np.ndarray) -> np.ndarray:
    D = delta_spectral(y)

    return np.sum(D, axis=0)

def fourier_tempogram(y):
    D = librosa.stft(novel_curve_delta_spectral(y), n_fft=512, hop_length=128)
    return np.abs(D)


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


def relative_saliency_of_t1(t_1, t_2):
    # TODO: unclear
    s_1 = t_1 / (t_1 + t_2)
    return s_1


def ALOTC(t_1, t_2, gt):
    if abs((gt - t_1) / gt) <= 0.08 or abs((gt - t_2) / gt) <= 0.08:
        p = 1
    else:
        p = 0
    return p



if __name__ == "__main__":
    from by_exeex.dataset import BallroomData
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
