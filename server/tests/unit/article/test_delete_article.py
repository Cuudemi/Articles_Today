import pytest
from fastapi import HTTPException
from src.repositories.article import ArticleRepository
from src.schemas.article import ModelArticle
from tests.unit.fixtures import setup_database
from src.models.article import Article
from src.db import SessionLocal

def test_delete_article_positive(setup_database):
    """Проверка успешного удаления статьи."""

    article_data = ModelArticle(
        name="Article to delete",
        id_source=1,
        content="Content",
        url="http://delete.com",
        theme_name="Разработка"
    )

    new_article = ArticleRepository.add_article(article_data)
    deleted_article = ArticleRepository.delete_article(id=new_article.id)

    assert deleted_article.name == "Article to delete"
    assert deleted_article.id == new_article.id

    with SessionLocal() as session:
        assert session.query(Article).filter_by(id=new_article.id).first() is None


def test_delete_article_not_found(setup_database):
    """Проверка ошибки при удалении несуществующей статьи."""
    with pytest.raises(HTTPException) as exc:
        ArticleRepository.delete_article(id=99)

    assert exc.value.status_code == 404
    assert "Article with ID 99 not found" in str(exc.value.detail)
