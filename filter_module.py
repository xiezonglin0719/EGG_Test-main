import numpy as np
import scipy.signal as signal

def init_filter_state(n_channels, sfreq=1000, lowcut=1, highcut=40, order=4):
    """
    初始化带通滤波器和滤波器状态
    """
    nyq = 0.5 * sfreq
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    # 为每个通道准备初始状态
    zi_single = signal.lfilter_zi(b, a)
    zi = np.tile(zi_single, (n_channels, 1))  # (n_channels, 阶数)
    return b, a, zi

def realtime_eeg_filter_stateful(raw_data, b, a, zi):
    """
    对 (n_channels, n_samples) 的 EEG 数据进行带状态滤波
    返回 (filtered_data, zf)
    """
    filtered_data, zf = signal.lfilter(b, a, raw_data, axis=-1, zi=zi)
    return filtered_data, zf
