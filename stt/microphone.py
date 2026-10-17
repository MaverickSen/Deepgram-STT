import pyaudio


class Microphone:

    RATE = 16000
    CHANNELS = 1
    CHUNK = 1024

    def __init__(self):

        self.audio = pyaudio.PyAudio()

        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
        )

    def read(self):

        return self.stream.read(
            self.CHUNK,
            exception_on_overflow=False,
        )

    def close(self):

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()