import pytest

from src.backend.utils.enums import ErrorMessages
from tests.integration_tests.conftest import (
    skip_total_word_count,
    skip_average_note_length,
    skip_common_words,
    skip_longest_notes,
    skip_shortest_note
)

# ----------------------------TOTAL WORD COUNT----------------------------------------------------
@pytest.mark.skipif(skip_total_word_count, reason="The flag 'skip_total_word_count' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_total_word_count_success(client, prepare_data):
    """Test calculating the total word count of all notes via the /analytic/total_words endpoint"""

    response = await client.get("/analytic/total_words")

    assert response.status_code == 200
    assert isinstance(response.json(), int)
    assert response.json() > 0


@pytest.mark.skipif(skip_total_word_count, reason="The flag 'skip_total_word_count' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_total_word_count_error(client):
    """Test retrieving the total word count when no notes are available via the /analytic/total_words endpoint"""

    response = await client.get("/analytic/total_words")

    assert response.status_code == 404
    assert response.json()["detail"] == ErrorMessages.NOT_FOUND_MULTI
# ----------------------------TOTAL WORD COUNT----------------------------------------------------


# ----------------------------AVERAGE NOTE LENGTH----------------------------------------------------
@pytest.mark.skipif(skip_average_note_length, reason="The flag 'skip_average_note_length' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_average_note_length_success(client, prepare_data):
    """Test calculating the average length of notes via the /analytic/length endpoint"""

    response = await client.get("/analytic/length")

    assert response.status_code == 200
    assert isinstance(response.json(), float)
    assert response.json() > 0


@pytest.mark.skipif(skip_average_note_length, reason="The flag 'skip_average_note_length' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_average_note_length_error(client):
    """Test retrieving the average note length when no notes are available via the /analytic/length endpoint"""

    response = await client.get("/analytic/length")

    assert response.status_code == 404
    assert response.json()["detail"] == ErrorMessages.NOT_FOUND_MULTI
# ----------------------------AVERAGE NOTE LENGTH----------------------------------------------------


# ----------------------------COMMON WORDS----------------------------------------------------
@pytest.mark.skipif(skip_common_words, reason="The flag 'skip_common_words' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_most_common_words_success(client, prepare_data):
    """Test retrieving the most common words used across all notes via the /analytic/common_words endpoint"""

    response = await client.get("/analytic/common_words?min_count=2")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "note" in response.json()


@pytest.mark.skipif(skip_common_words, reason="The flag 'skip_common_words' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_most_common_words_error(client):
    """Test retrieving the most common words with an invalid minimum count via the /analytic/common_words endpoint"""

    response = await client.get("/analytic/common_words?min_count=1")

    assert response.status_code == 404
    assert response.json()["detail"] == ErrorMessages.NOT_FOUND_MULTI
# ----------------------------COMMON WORDS----------------------------------------------------


# ----------------------------LONGEST NOTES----------------------------------------------------
@pytest.mark.skipif(skip_longest_notes, reason="The flag 'skip_longest_notes' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_longest_notes_success(client, prepare_data):
    """Test retrieving the longest notes via the /analytic/longest endpoint"""

    response = await client.get("/analytic/longest?top_n=1")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


@pytest.mark.skipif(skip_longest_notes, reason="The flag 'skip_longest_notes' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_longest_notes_error(client):
    """Test retrieving the longest notes when no notes are available via the /analytic/longest endpoint"""

    response = await client.get("/analytic/longest?top_n=1")

    assert response.status_code == 404
    assert response.json()["detail"] == ErrorMessages.NOT_FOUND_MULTI
# ----------------------------LONGEST NOTES----------------------------------------------------


# ----------------------------SHORTEST NOTES----------------------------------------------------
@pytest.mark.skipif(skip_shortest_note, reason="The flag 'skip_shortest_note' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_shortest_notes_success(client, prepare_data):
    """Test retrieving the shortest notes via the /analytic/shortest endpoint"""

    response = await client.get("/analytic/shortest?top_n=1")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


@pytest.mark.skipif(skip_shortest_note, reason="The flag 'skip_shortest_note' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_shortest_notes_error(client):
    """Test retrieving the shortest notes when no notes are available via the /analytic/shortest endpoint"""

    response = await client.get("/analytic/shortest?top_n=1")

    assert response.status_code == 404
    assert response.json()["detail"] == ErrorMessages.NOT_FOUND_MULTI
# ----------------------------SHORTEST NOTES----------------------------------------------------
