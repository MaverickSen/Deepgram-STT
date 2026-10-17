from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from threading import Lock


@dataclass(frozen=True)
class FinalTranscriptRecord:
    transcript_id: int
    text: str
    timestamp: str


class FinalTranscriptLog:
    def __init__(self):
        self._records: list[FinalTranscriptRecord] = []
        self._lock = Lock()

    def append(self, text: str) -> FinalTranscriptRecord:
        with self._lock:
            record = FinalTranscriptRecord(
                transcript_id=len(self._records) + 1,
                text=text,
                timestamp=datetime.now(timezone.utc).isoformat(),
            )
            self._records.append(record)
            return record

    def get_all(self) -> list[FinalTranscriptRecord]:
        with self._lock:
            return list(self._records)

    def export_records(self) -> list[dict]:
        return [
            asdict(record)
            for record in self.get_all()
        ]
