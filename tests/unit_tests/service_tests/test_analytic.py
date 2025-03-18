import pytest

from tests.unit_tests.conftest import analytic_skip_word_count, analytic_skip_avg_note_length, analytic_skip_common_word, \
    analytic_skip_longest_note, analytic_skip_shortest_note
from tests.unit_tests.service_tests.conftest import analytics_service


# ----------------------------TOTAL WORD COUNT----------------------------------------------------
@pytest.mark.skipif(analytic_skip_word_count, reason="The flag 'analytic_skip_word_count' is active!")
@pytest.mark.parametrize(
    "expected_word_count",
    [12]
)
def test_get_total_word_count(analytics_service, expected_word_count):
    """Test that the 'get_total_word_count' method correctly calculates the total
       word count across all notes"""

    assert analytics_service.get_total_word_count() == expected_word_count
# ----------------------------TOTAL WORD COUNT----------------------------------------------------


# ----------------------------AVERAGE NOTE LENGTH----------------------------------------------------
@pytest.mark.skipif(analytic_skip_avg_note_length, reason="The flag 'analytic_skip_avg_note_length' is active!")
@pytest.mark.parametrize(
    "expected_avg_length",
    [4.0]
)
def test_get_average_note_length(analytics_service, expected_avg_length):
    """Test that the 'get_average_note_length' method correctly calculates the
        average word count per note."""

    assert analytics_service.get_average_note_length() == expected_avg_length
# ----------------------------AVERAGE NOTE LENGTH----------------------------------------------------


# ----------------------------COMMON WORDS----------------------------------------------------
@pytest.mark.skipif(analytic_skip_common_word, reason="The flag 'analytic_skip_common_word' is active!")
@pytest.mark.parametrize(
    "min_count, expected_common_words",
    [
        (2, {"note": 3})
    ]
)
def test_get_most_common_words(analytics_service, min_count, expected_common_words):
    """Test that the 'get_most_common_words' method correctly identifies the most
       common words in all notes, excluding stopwords, and only returns words that
       appear at least 'min_count' times."""

    assert analytics_service.get_most_common_words(min_count) == expected_common_words
# ----------------------------COMMON WORDS----------------------------------------------------


# ----------------------------LONGEST NOTES----------------------------------------------------
@pytest.mark.skipif(analytic_skip_longest_note, reason="The flag 'analytic_skip_longest_note' is active!")
@pytest.mark.parametrize(
    "top_n, expected_longest_notes",
    [
        (1, [{"content": "Another note with more words."}])
    ]
)
def test_get_longest_notes(analytics_service, top_n, expected_longest_notes):
    """Test that the 'get_longest_notes' method correctly identifies the top 'top_n'
       longest notes based on word count."""
    assert analytics_service.get_longest_notes(top_n) == expected_longest_notes
# ----------------------------LONGEST NOTES----------------------------------------------------


# ----------------------------SHORTEST NOTES----------------------------------------------------
@pytest.mark.skipif(analytic_skip_shortest_note, reason="The flag 'analytic_skip_shortest_note' is active!")
@pytest.mark.parametrize(
    "top_n, expected_shortest_notes",
    [
        (1, [{"content": "Short note."}])
    ]
)
def test_get_shortest_notes(analytics_service, top_n, expected_shortest_notes):
    """Test that the 'get_shortest_notes' method correctly identifies the top 'top_n'
        shortest notes based on word count."""
    assert analytics_service.get_shortest_notes(top_n) == expected_shortest_notes
# ----------------------------SHORTEST NOTES----------------------------------------------------
