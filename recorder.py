import contextlib
import time
import pyaudio
import wave
from typing import Callable, Tuple


@contextlib.contextmanager
def new_stream(*args, **kwds) -> Tuple[pyaudio.Stream, Callable]:
    p = pyaudio.PyAudio()
    stream = p.open(**kwds)

    def save_data(data: list, configs: dict, save_loc: str) -> str:
        filename = f'{save_loc}/sentence_{int(time.time())}.wav'

        with wave.open(filename, 'wb') as wf:
            data = b''.join(data)
            wf.setnchannels(configs['channels'])
            wf.setsampwidth(p.get_sample_size(configs['format']))
            wf.setframerate(configs['rate'])
            wf.writeframes(data)

            return filename

        raise RuntimeError(f'Fail to store {filename}')

    yield stream, save_data
    stream.close()
    p.terminate()
