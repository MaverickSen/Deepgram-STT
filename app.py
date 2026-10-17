
from stt.deepgram_client import DeepgramStreamingClient
from transcript.transcript_manager import TranscriptManager
from transcript.final_transcript_log import FinalTranscriptLog


def main():
    transcript_manager = TranscriptManager()
    final_transcript_log = FinalTranscriptLog()

    def on_final_transcript(query: str):
        if not query.strip():
            return

        # Store the complete utterance in memory.
        final_transcript_log.append(query)

        # No additional printing here.
        # TranscriptHandler already prints [FINAL] segments.

    deepgram_client = DeepgramStreamingClient(
        transcript_manager=transcript_manager,
        on_final_transcript=on_final_transcript,
    )

    try:
        deepgram_client.start()
    except KeyboardInterrupt:
        print("\nStopped listening.")


if __name__ == "__main__":
    main()
