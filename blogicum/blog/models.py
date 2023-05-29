from datetime import date
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet


User = get_user_model()


class BaseModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
        )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True
        )

    class Meta:
        abstract = True


class Location(BaseModel):
    name = models.CharField(
        max_length=256,
        verbose_name='Название места'
        )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name


class Category(BaseModel):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
        )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, '
                   'дефис и подчёркивание.')
        )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title


class PublicPostsManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().select_related(
            'location',
            'category',
            'author'
        ).filter(
            pub_date__lte=date.today(),
            is_published=True,
            category__is_published=True
        )


class Post(BaseModel):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
        )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем '
                   '— можно делать отложенные публикации.')
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации')
    location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение'
        )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
        )

    objects = models.Manager()
    public_objects = PublicPostsManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self) -> str:
        return f'{self.text} ({self.pub_date.strftime("%d.%m.%Y")})'
