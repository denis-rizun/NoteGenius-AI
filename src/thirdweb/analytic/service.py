import numpy as np
import string
from collections import Counter
from src.config import stopwords


class NoteAnalyticsService:
    def __init__(self, notes: list[dict]):
        self.notes = notes

    def get_total_word_count(self) -> int:
        """Returns the total number of words across all notes."""
        return int(self._get_word_counts().sum())

    def get_average_note_length(self) -> float:
        """Returns the average word count per note."""
        word_counts = self._get_word_counts()
        return float(word_counts.mean()) if word_counts.size > 0 else 0.0

    def get_most_common_words(self, min_count=3) -> dict:
        """Returns the most common words across all notes, excluding stopwords."""
        words = self._extract_filtered_words()
        word_counter = Counter(words)
        return {
            word: count
            for word, count in word_counter.items()
            if count > min_count
        }

    def get_longest_notes(self, top_n=3) -> list[dict]:
        """Returns the top N the longest notes based on word count."""
        word_counts = self._get_word_counts()
        sorted_indices = np.argsort(word_counts)[-top_n:]
        return [self.notes[i] for i in sorted_indices[::-1]]

    def get_shortest_notes(self, top_n=3) -> list[dict]:
        """Returns the top N the shortest notes based on word count."""
        word_counts = self._get_word_counts()
        sorted_indices = np.argsort(word_counts)[:top_n]
        return [self.notes[i] for i in sorted_indices]

    def _get_word_counts(self) -> np.ndarray:
        """Helper method to get word counts for all notes."""
        return np.array(
            [len(note["content"].split()) for note in self.notes],
            dtype=int
        )

    def _extract_filtered_words(self) -> list[str]:
        """Helper method to extract words from notes and filter out stopwords."""
        all_words = " ".join(note["content"] for note in self.notes).split()
        return [
            word.lower().strip(string.punctuation)
            for word in all_words
            if word.lower() not in stopwords
        ]
