from transcript.transcript_buffer import TranscriptBuffer
from transcript.utterance import Utterance


class TranscriptManager:

    def __init__(self):

        # Final transcript segments.
        self.committed_buffer = TranscriptBuffer()

        # Most recent partial transcript.
        self.working_transcript = None

        # Indicates whether the most recently committed
        # final transcript marked the end of the user's speech.
        self.speech_final = False

    # ---------------------------------------------------------
    # Update current partial transcript
    # ---------------------------------------------------------

    def update_partial(
        self,
        text: str,
        speech_final: bool = False,
    ):

        self.working_transcript = Utterance(
            text=text
        )

        self.speech_final = speech_final

    # ---------------------------------------------------------
    # Commit final transcript
    # ---------------------------------------------------------

    def commit_final(
        self,
        text: str,
        speech_final: bool = False,
    ):

        utterance = Utterance(
            text=text
        )

        self.committed_buffer.append(
            utterance
        )

        self.working_transcript = None

        self.speech_final = speech_final

    # ---------------------------------------------------------
    # Return final transcript objects
    # ---------------------------------------------------------

    def get_final_utterances(self) -> list[Utterance]:

        return self.committed_buffer.get_utterances()

    # ---------------------------------------------------------
    # Return current conversation as objects
    # ---------------------------------------------------------

    def get_current_conversation(self) -> list[Utterance]:

        conversation = list(
            self.committed_buffer.get_utterances()
        )

        if self.working_transcript:

            conversation.append(
                self.working_transcript
            )

        return conversation

    # ---------------------------------------------------------
    # Return committed transcript as one string
    # ---------------------------------------------------------

    def get_final_text(self) -> str:

        return self.committed_buffer.get_text()

    # ---------------------------------------------------------
    # Return current transcript including latest partial
    # ---------------------------------------------------------

    def get_current_text(self) -> str:

        text = self.committed_buffer.get_text()

        if self.working_transcript:

            if text:
                text += " "

            text += self.working_transcript.text

        return text

    # ---------------------------------------------------------
    # Check whether the latest final result completed speech
    # ---------------------------------------------------------

    def is_speech_final(self) -> bool:

        return self.speech_final

    # ---------------------------------------------------------
    # Clear transcript state
    # ---------------------------------------------------------

    def clear(self):

        self.committed_buffer.clear()

        self.working_transcript = None

        self.speech_final = False