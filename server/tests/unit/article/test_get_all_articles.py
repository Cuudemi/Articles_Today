import pytest
from src.db import SessionLocal
from src.models.article import Article
from src.repositories.article import ArticleRepository
from tests.unit.fixtures import setup_database

def test_get_all_articles_positive(setup_database):
    """Проверка возврата всех статей."""
    with SessionLocal() as session:
        article1 = Article(
            name="Article 1",
            id_source=1,
            content="Content 1",
            url="http://example1.com",
            theme_name="Разработка"
        )
        article2 = Article(
            name="Article 2",
            id_source=1,
            content="Content 2",
            url="http://example2.com",
            theme_name="Разработка"
        )
        session.add_all([article1, article2])
        session.commit()

    articles = ArticleRepository.get_all_articles()

    assert len(articles) == 2
    assert articles[0].name == "Article 1"
    assert articles[1].name == "Article 2"

def test_get_all_articles_empty(setup_database):
    """Проверка возврата пустого списка, если статьи отсутствуют."""
    articles = ArticleRepository.get_all_articles()

    assert len(articles) == 0
