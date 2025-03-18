import pytest

from tests.integration_tests.conftest import (
    note_query_skip_create,
    note_query_skip_gets,
    note_query_skip_update,
    note_query_skip_delete
)

# ----------------------------CREATE NOTE SUCCESS----------------------------------------------------
@pytest.mark.skipif(note_query_skip_create, reason="The flag 'note_query_skip_create' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_create_note_success(note_repo):
    """Tests creating a note and checks if the ID is returned."""
    data = {
        "title": "Project Update: March 2025",
        "content": "Today, we successfully integrated the new recommendation engine.",
        "summarization": "Integration of AI recommendation engine completed.",
        "version_number": 1,
    }
    note_id = await note_repo.create(data)
    assert isinstance(note_id, int)
    note = await note_repo.get_by_id(note_id)

    assert note is not None
    assert note.id == 1
    assert note.title == "Project Update: March 2025"
    assert note.content == "Today, we successfully integrated the new recommendation engine."
    assert note.summarization == "Integration of AI recommendation engine completed."
    assert note.version_number == 1
# ----------------------------CREATE NOTE SUCCESS----------------------------------------------------


# ----------------------------GET ALL NOTES SUCCESS----------------------------------------------------
@pytest.mark.skipif(note_query_skip_gets, reason="The flag 'note_query_skip_gets' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_notes_success(create_data, note_repo):
    """Tests retrieving all notes with different dataset sizes."""
    result = await note_repo.get_all()

    assert len(result) == 2
    assert isinstance(result, list)

    for idx, note in enumerate(result):
        assert note.id == create_data[idx]["id"]
        assert note.title == create_data[idx]["title"]
        assert note.content == create_data[idx]["content"]
        assert note.summarization == create_data[idx]["summarization"]
        assert note.version_number == create_data[idx]["version_number"]
# ----------------------------GET ALL NOTES SUCCESS----------------------------------------------------

# ----------------------------UPDATE NOTE SUCCESS----------------------------------------------------
@pytest.mark.skipif(note_query_skip_update, reason="The flag 'note_query_skip_update' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_update_note_success(create_data, note_repo):
    """Tests updating a note and version increment."""
    note = await note_repo.get_by_id(create_data[0]["id"])
    assert note.version_number == 1

    await note_repo.put(note, {"title": "Updated", "content": "New content"})
    updated_note = await note_repo.get_by_id(create_data[0]["id"])

    assert updated_note.title == "Updated"
    assert updated_note.content == "New content"
    assert updated_note.version_number == 2
# ----------------------------UPDATE NOTE SUCCESS----------------------------------------------------

# ----------------------------DELETE NOTE SUCCESS----------------------------------------------------
@pytest.mark.skipif(note_query_skip_delete, reason="The flag 'note_query_skip_delete' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_delete_note_success(create_data, note_repo):
    """Tests deleting a note."""
    note = await note_repo.get_by_id(create_data[0]["id"])
    assert note is not None
    await note_repo.delete(note)
    deleted_note = await note_repo.get_by_id(create_data[0]["id"])
    assert deleted_note is None
# ----------------------------DELETE NOTE SUCCESS----------------------------------------------------
