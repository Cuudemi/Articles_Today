import pytest
from fastapi import HTTPException
from src.repositories.source import SourceRepository
from tests.unit.fixtures import setup_database

def test_get_source_by_id_positive(setup_database):
    """Проверка получения источника по ID."""
    source = SourceRepository.get_sourse_by_id(1)

    assert source.name == "Test Source"
    assert source.theme == "Test Theme"
    assert source.url == "Test url"


def test_get_source_by_id_not_found(setup_database):
    """Проверка ошибки при получении несуществующего источника."""
    with pytest.raises(HTTPException) as exc:
        SourceRepository.get_sourse_by_id(99)

    assert exc.value.status_code == 404
    assert "No source found" in str(exc.value.detail)
