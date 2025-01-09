import pytest
import pydantic
from sqlalchemy.exc import IntegrityError
from src.repositories.article import ArticleRepository
from src.schemas.article import ModelArticle
from tests.unit.fixtures import setup_database

def test_add_article_positive(setup_database):
    """Проверка добавления новой статьи."""
    article_data = ModelArticle(
        name="Test Article",
        id_source=1,
        content="Sample content",
        url="http://example.com",
        theme_name="Разработка"
    )

    new_article = ArticleRepository.add_article(article_data)

    assert new_article.name == "Test Article"
    assert new_article.id_source == 1
    assert new_article.content == "Sample content"
    assert new_article.url == "http://example.com"
    assert new_article.theme_name == "Разработка"


def test_add_article_empty(setup_database):
    """Проверка ошибки при добавлении пустой статьи."""
    with pytest.raises(pydantic.ValidationError):
        ModelArticle()


def test_add_article_invalid_source(setup_database):
    """Проверка ошибки при добавлении статьи с несуществующим источником."""
    article_data = ModelArticle(
        name="Test Article",
        id_source=99,  # Несуществующий источник
        content="Sample content",
        url="http://example.com",
        theme_name="Разработка"
    )

    with pytest.raises(IntegrityError):
        ArticleRepository.add_article(article_data)
