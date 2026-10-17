import threading
import time
from typing import Callable

from dotenv import load_dotenv

from deepgram import DeepgramClient
from deepgram.core.events import EventType

from stt.microphone import Microphone
from stt.transcript_handler import TranscriptHandler


load_dotenv()


class DeepgramStreamingClient:
    def __init__(
        self,
        transcript_manager,
        on_final_transcript: Callable[[str], None] | None = None,
    ):
        self.client = DeepgramClient()
        self.microphone = Microphone()

        self.handler = TranscriptHandler(
            transcript_manager=transcript_manager,
            on_final_transcript=on_final_transcript,
        )

    def start(self):
        with self.client.listen.v1.connect(
            model="nova-3",
            encoding="linear16",
            sample_rate=16000,
            language="en",
            interim_results=True,
            punctuate=True,
            smart_format=True,
            endpointing=300,
        ) as connection:

            connection.on(
                EventType.OPEN,
                lambda _: print(
                    "Connected to Deepgram"
                ),
            )

            connection.on(
                EventType.MESSAGE,
                self.handler.on_message,
            )

            connection.on(
                EventType.ERROR,
                lambda e: print(
                    f"\nERROR: {e}"
                ),
            )

            connection.on(
                EventType.CLOSE,
                lambda _: print(
                    "\nConnection Closed."
                ),
            )

            threading.Thread(
                target=connection.start_listening,
                daemon=True,
            ).start()

            print(
                "Listening...\n"
            )

            try:
                while True:
                    audio = self.microphone.read()
                    connection.send_media(audio)

            except KeyboardInterrupt:
                print("\nStopping...")

                connection.send_finalize()

                time.sleep(1)

                connection.send_close_stream()

            finally:
                self.microphone.close()