import pytest
from fastapi import HTTPException
from src.repositories.article import ArticleRepository
from src.schemas.article import ModelArticle
from tests.unit.fixtures import setup_database
from src.models.article import Article
from src.db import SessionLocal

def test_update_article_positive(setup_database):
    """Проверка успешного обновления статьи."""
    with SessionLocal() as session:
        article = Article(
            id=1,
            name="Old Article",
            id_source=1,
            content="Old content",
            url="http://old.com",
            theme_name="Разработка"
        )
        session.add(article)
        session.commit()

    updated_article = ArticleRepository.update_article(
        id=1,
        name="Updated Article",
        content="Updated content"
    )

    assert updated_article.name == "Updated Article"
    assert updated_article.content == "Updated content"


def test_update_article_not_found(setup_database):
    """Проверка ошибки при обновлении несуществующей статьи."""
    with pytest.raises(HTTPException) as exc:
        ArticleRepository.update_article(id=99, name="New Name")

    assert exc.value.status_code == 404
    assert "Article with ID 99 not found" in str(exc.value.detail)


def test_update_article_invalid_source(setup_database):
    """Б8: Проверка ошибки при обновлении статьи с несуществующим источником."""
    article_data = ModelArticle(
        name="Test Article",
        id_source=1,
        content="Sample content",
        url="http://example.com",
        theme_name="Разработка"
    )

    new_article = ArticleRepository.add_article(article_data)

    new_id_source=99

    with pytest.raises(HTTPException) as exc:
        ArticleRepository.update_article(new_article.id, id_source=new_id_source)

    assert exc.value.status_code == 404
    assert f"Source with ID {new_id_source} not found." in str(exc.value.detail)