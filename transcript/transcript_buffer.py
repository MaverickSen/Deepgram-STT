from transcript.utterance import Utterance


class TranscriptBuffer:

    def __init__(self):
        self.utterances: list[Utterance] = []

    def append(self, utterance: Utterance):
        self.utterances.append(utterance)

    def clear(self):
        self.utterances.clear()

    def get_utterances(self) -> list[Utterance]:
        return self.utterances

    def get_text(self) -> str:
        return " ".join(
            utterance.text.strip()
            for utterance in self.utterances
        )