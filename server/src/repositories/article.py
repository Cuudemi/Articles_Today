from src.repositories.source import SourceRepository
from fastapi import HTTPException
from src.schemas.article import ModelArticleWithID, ModelArticle
from src.Parser import get_articles_by_theme_url
from src.db import SessionLocal
from src.models.article import Article
from src.models.source import Source
from sqlalchemy import select

class ArticleRepository:

    @classmethod
    def add_today_best_articles(cls, theme: str) -> int:
        """
        Добавляет лучшие статьи на сегодня для указанной темы. Парсит статьи с помощью функции
        `get_articles_by_theme_url`, затем сохраняет их в базу данных.
        
        :param theme: Тема, для которой нужно получить статьи.
        :return: Количество добавленных статей.
        """
        i = 0
        # получаем нужную ссылку
        id_sourse = SourceRepository.get_id_sourse_by_theme(theme)
        url_sourse = SourceRepository.get_sourse_by_id(id_sourse).url

        articles = get_articles_by_theme_url.main(url_sourse)

        article = articles[0]

        for article in articles:
            new_article = ModelArticleWithID(
                id=int(article["id"]),
                name=article["name"],
                id_source=id_sourse,
                content=" ".join(article.get("content", [])),
                url=article["url"],
                theme_name=article["theme"]
            )
            ArticleRepository.add_article(new_article)
            i = i + 1
        return i

    @classmethod
    def add_article(cls, article: ModelArticle) -> Article:
        """
        Добавляет новую статью в базу данных.
        
        :param article: Объект модели статьи для добавления в БД.
        :return: Добавленная статья.
        """
        with SessionLocal() as session:
            data = article.model_dump()
            new_article = Article(**data)
            session.add(new_article)

            session.flush()
            session.commit()

            return new_article

    @classmethod
    def get_all_articles(cls) -> list[Article]:
        """
        Получает все статьи из базы данных.
        
        :return: Список всех статей в базе данных.
        """ 
        with SessionLocal() as session:
            query = select(Article)
            result = session.execute(query)

            return result.scalars().all()

    @classmethod
    def update_article(
            cls,
            id: int,
            name: str = None,
            id_source: int = None,
            content: str = None,
            url: str = None,
            theme: str = None,
    ) -> Article:
        """
        Обновляет существующую статью по её ID.
        
        :param id: ID статьи, которую нужно обновить.
        :param name: Новое имя статьи.
        :param id_source: Новый ID источника.
        :param content: Новый контент статьи.
        :param url: Новый URL статьи.
        :param theme: Новая тема статьи.
        :return: Обновленная статья.
        """
        with SessionLocal() as session:
            query = select(Article).where(Article.id == id)
            returned_article = session.scalar(query)

            # Если статья не найдена
            if not returned_article:
                raise HTTPException(status_code=404, detail=f"Article with ID {id} not found.")

            # Проверка существования источника, если id_source передан
            if id_source is not None:
                source_query = select(Source).where(Source.id == id_source)
                source = session.scalar(source_query)
                if not source:
                    raise HTTPException(status_code=404, detail=f"Source with ID {id_source} not found.")

            if name is not None:
                returned_article.name = name
            if id_source is not None:
                returned_article.id_source = id_source
            if content is not None:
                returned_article.content = content
            if url is not None:
                returned_article.url = url
            if theme is not None:
                returned_article.theme = theme

            session.flush()
            session.commit()

            return returned_article

    @classmethod
    def delete_article(cls, id: int) -> Article:
        """
        Удаляет статью по её ID.
        
        :param id: ID статьи для удаления.
        :return: Удалённая статья.
        """
        with SessionLocal() as session:
            # Проверяем, существует ли статья
            returned_article = session.query(Article).filter(Article.id == id).first()
            if not returned_article:
                raise HTTPException(status_code=404, detail=f"Article with ID {id} not found.")
            
            query = select(Article).where(Article.id == id)
            returned_article = session.scalar(query)

            session.delete(returned_article)

            session.flush()
            session.commit()

            return returned_article