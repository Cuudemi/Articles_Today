import pytest
from fastapi import HTTPException
from src.repositories.source import SourceRepository
from src.schemas.source import ModelSource
from tests.unit.fixtures import setup_database

def test_add_source_positive(setup_database):
    """Проверка добавления нового источника."""
    source_data = ModelSource(
        name="New Source",
        theme="Technology",
        url="http://new-source.com"
    )

    new_source = SourceRepository.add_source(source_data)

    assert new_source.name == "New Source"
    assert new_source.theme == "Technology"
    assert new_source.url == "http://new-source.com"


def test_add_source_duplicate(setup_database):
    """Проверка ошибки при добавлении источника с уже существующим URL."""
    source_data = ModelSource(
        name="New Source",
        theme="Technology",
        url="Test url"
    )

    with pytest.raises(HTTPException) as exc:
        SourceRepository.add_source(source_data)

    assert exc.value.status_code == 400
    assert "Source with URL" in str(exc.value.detail)
