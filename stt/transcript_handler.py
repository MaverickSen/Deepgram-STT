from typing import Callable

from deepgram.listen.v1.types import ListenV1Results

class TranscriptHandler:
    def __init__(
        self,
        transcript_manager,
        on_final_transcript: Callable[[str], None] | None = None,
    ):
        self.transcript_manager = transcript_manager
        self.on_final_transcript = on_final_transcript

    def on_message(self, message):
        if not isinstance(message, ListenV1Results):
            return

        alt = message.channel.alternatives[0]
        transcript = alt.transcript.strip()

        if not transcript:
            return

        if message.is_final:
            self.transcript_manager.commit_final(
                text=transcript
            )

            print(f"\n[FINAL] {transcript}")

            # speech_final indicates that Deepgram considers
            # the speaker's utterance complete.
            if message.speech_final:
                complete_query = (
                    self.transcript_manager.get_current_text()
                )

                self.transcript_manager.clear()

                if (
                    complete_query
                    and self.on_final_transcript
                ):
                    self.on_final_transcript(
                        complete_query
                    )

        else:
            self.transcript_manager.update_partial(
                text=transcript
            )