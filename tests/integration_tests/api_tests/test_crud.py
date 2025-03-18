from random import randint

import pytest
from pydantic import ValidationError

from src.backend.utils.enums import ErrorMessages
from src.backend.utils.schemas import NoteGetSchemaResponse
from tests.integration_tests.conftest import (
    note_skip_create,
    note_skip_get,
    note_skip_gets,
    note_skip_update,
    note_skip_delete
)


# ----------------------------CREATE NOTE----------------------------------------------------
@pytest.mark.skipif(note_skip_create, reason="The flag 'note_skip_create' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_create_note_success(client):
    """Test creating a note successfully via the /post endpoint"""

    response = await client.post(
        url="/crud/post",
        json={
            "title": "Project Update: March 2025",
            "content": "Today, we made significant progress on the AI-powered resume screening project. We successfully integrated the new recommendation engine, which will enhance the accuracy of candidate suggestions. The team also completed a major update to the database, improving query speed and reliability. A few issues remain with data inconsistency, but the engineering team is already working on a solution. We expect to have this fixed by the end of the week. Next steps involve finalizing the API documentation and preparing for the internal demo scheduled for next month.",
        },
    )

    assert response.status_code == 201
    assert "note_id" in response.json()


@pytest.mark.skipif(note_skip_create, reason="The flag 'note_skip_create' is active!")
@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "note_data, expected_status, expected_error_message",
    [
        (
            {"title": "Test Note", "content": "Test content", "invalid_field": "test"},
            400,
            ErrorMessages.NOT_CONFORM_SCHEMA.value,
        ),
        (
            {"title": None, "content": "Test content"},
            400,
            ErrorMessages.NOT_CONFORM_SCHEMA.value,
        ),
        (
            {"title": "Test Note", "content": None},
            400,
            ErrorMessages.NOT_CONFORM_SCHEMA.value,
        ),
        (
            {"title": "", "content": "Test content"},
            400,
            ErrorMessages.TITLE_EMPTY.value,
        ),
        ({"title": "Test Note", "content": ""}, 400, ErrorMessages.CONTENT_EMPTY.value),
        ({"title": "", "content": ""}, 400, ErrorMessages.TITLE_EMPTY.value),
        (
            {"title": " ".join(["word"] * 101), "content": "Test content"},
            400,
            ErrorMessages.TITLE_TOO_LONG,
        ),
        (
            {"title": "Test Note", "content": " ".join(["word"] * 501)},
            400,
            ErrorMessages.CONTENT_TOO_LONG,
        ),
    ],
)
async def test_create_note_error(client, note_data, expected_status, expected_error_message):
    """Test creating a note with invalid data via the /post endpoint"""
    response = await client.post("/crud/post", json=note_data)

    assert response.status_code == expected_status
    assert expected_error_message in response.json()["detail"]
# ----------------------------CREATE NOTE----------------------------------------------------


# ----------------------------GET NOTE BY ID----------------------------------------------------
@pytest.mark.skipif(note_skip_get, reason="The flag 'note_skip_get' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_get_note_by_id_success(client, id):
    """Test retrieving a note by its ID via the /get/{id} endpoint"""
    get_response = await client.get(f"/crud/get/{id}")

    assert get_response.status_code == 200

    try:
        note_data = NoteGetSchemaResponse(**get_response.json())
        assert isinstance(note_data.id, int)
        assert isinstance(note_data.title, str) and note_data.title
        assert isinstance(note_data.content, str) and note_data.content
        assert isinstance(note_data.summarization, str)
        assert isinstance(note_data.version_number, int)
        assert isinstance(note_data.created_at, str) and note_data.created_at
        assert isinstance(note_data.updated_at, str) and note_data.updated_at
    except ValidationError as e:
        pytest.fail(f"Response data does not match expected schema: {e}")
    except AttributeError as e:
        pytest.fail(f"Failed to access note_data attributes: {str(e)}")
    except AssertionError as e:
        pytest.fail(f"Assertion error: {str(e)}")


@pytest.mark.skipif(note_skip_get, reason="The flag 'note_skip_get' is active!")
@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "note_id, expected_status, expected_detail",
    [
        (randint(10, 100), 404, ErrorMessages.NOT_FOUND_SINGLE.value),
        (None, 400, ErrorMessages.NOT_CONFORM_SCHEMA.value),
        ("invalid_id", 400, ErrorMessages.NOT_CONFORM_SCHEMA.value),
    ],
)
async def test_get_note_by_id_error(client, note_id, expected_status, expected_detail):
    """Test retrieving a note by ID with invalid or non-existent ID via the /get/{id} endpoint"""
    get_response = await client.get(f"/crud/get/{note_id}")

    assert get_response.status_code == expected_status
    assert "detail" in get_response.json()
    assert get_response.json()["detail"] == expected_detail
# ----------------------------GET NOTE BY ID----------------------------------------------------


# ----------------------------GET NOTE ALL----------------------------------------------------
@pytest.mark.skipif(note_skip_gets, reason="The flag 'note_skip_gets' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_notes_success(client, id):
    """Test retrieving all notes via the /get endpoint"""
    response = await client.get("/crud/get")
    assert response.status_code == 200
    notes = response.json()
    assert isinstance(notes, list)
    assert len(notes) == 1

    try:
        validated_notes = [NoteGetSchemaResponse(**note) for note in notes]

        for note in validated_notes:
            assert isinstance(note.id, int)
            assert isinstance(note.title, str) and note.title
            assert isinstance(note.content, str) and note.content
            assert isinstance(note.summarization, str)
            assert isinstance(note.version_number, int)
            assert isinstance(note.created_at, str) and note.created_at
            assert isinstance(note.updated_at, str) and note.updated_at
    except ValidationError as e:
        pytest.fail(f"Response data does not match expected schema: {e}")
    except AttributeError as e:
        pytest.fail(f"Failed to access note_data attributes: {str(e)}")
    except AssertionError as e:
        pytest.fail(f"Assertion error: {str(e)}")


@pytest.mark.skipif(note_skip_gets, reason="The flag 'note_skip_gets' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_get_notes_error(client):
    """Test retrieving all notes when no notes are available via the /get endpoint"""
    response = await client.get("/crud/get")
    assert response.status_code == 404
    detail = response.json()["detail"]
    assert detail == ErrorMessages.NOT_FOUND_MULTI.value
# ----------------------------GET NOTE ALL----------------------------------------------------


# ----------------------------UPDATE NOTE----------------------------------------------------
@pytest.mark.skipif(note_skip_update, reason="The flag 'note_skip_update' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_update_note_success(client, id):
    """Test updating a note successfully via the /update/{id} endpoint"""
    update_response = await client.put(f"/crud/update/{id}", json={"title": "Updated Title"})

    assert update_response.status_code == 204


@pytest.mark.skipif(note_skip_update, reason="The flag 'note_skip_update' is active!")
@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "note_id, update_data, expected_status, expected_response",
    [
        (1, {}, 400, {"detail": ErrorMessages.FIELDS_BOTH_EMPTY.value}),
        (1, {"title": ""}, 400, {"detail": ErrorMessages.TITLE_EMPTY.value}),
        (1, {"content": ""}, 400, {"detail": ErrorMessages.CONTENT_EMPTY.value}),
        (1, {"title": " ".join(["word"] * 101)}, 400, {"detail": ErrorMessages.TITLE_TOO_LONG.value}),
        (1, {"content": " ".join(["word"] * 501)}, 400, {"detail": ErrorMessages.CONTENT_TOO_LONG.value}),
        (9999, {"title": "Valid Title"}, 404, {"detail": ErrorMessages.NOT_FOUND_SINGLE}),
        (1, {"title": "Valid Title", "invalid_field": "test"}, 400, {"detail": ErrorMessages.NOT_CONFORM_SCHEMA.value}),
    ],
)
async def test_update_note_error(
        client,
        note_id,
        update_data,
        expected_status,
        expected_response
):
    """Test updating a note with invalid or incomplete data via the /update/{id} endpoint"""
    update_response = await client.put(f"/crud/update/{note_id}", json=update_data)

    assert update_response.status_code == expected_status
    assert update_response.json() == expected_response
# ----------------------------UPDATE NOTE----------------------------------------------------


# ----------------------------DELETE NOTE----------------------------------------------------
@pytest.mark.skipif(note_skip_delete, reason="The flag 'note_skip_delete' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_delete_note_success(client, id):
    """Test deleting a note successfully via the /delete/{id} endpoint"""
    delete_response = await client.delete(f"/crud/delete/{id}")

    assert delete_response.status_code == 204


@pytest.mark.skipif(note_skip_delete, reason="The flag 'note_skip_delete' is active!")
@pytest.mark.asyncio(loop_scope="session")
async def test_delete_note_error(client):
    """Test deleting a note that does not exist via the /delete/{id} endpoint"""
    note_id = randint(50, 100)
    delete_response = await client.delete(f"/crud/delete/{note_id}")

    assert delete_response.status_code == 404
    assert delete_response.json()["detail"] == ErrorMessages.NOT_FOUND_SINGLE.value
# ----------------------------DELETE NOTE----------------------------------------------------
