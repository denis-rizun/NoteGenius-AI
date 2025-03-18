import pytest

from src.thirdweb.analytic.service import NoteAnalyticsService


@pytest.fixture
def notes():
    """
    Fixture that returns a list of sample notes to be used in tests.

    Returns:
        list: A list of dictionaries, each representing a note with content.
    """
    return [
        {"content": "This is a simple note."},
        {"content": "Another note with more words."},
        {"content": "Short note."},
    ]


@pytest.fixture
def analytics_service(notes):
    """
    Fixture that returns an instance of NoteAnalyticsService initialized with sample notes.

    Returns:
        NoteAnalyticsService: An instance of the service for note analytics.
    """
    return NoteAnalyticsService(notes)