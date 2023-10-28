from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator


class Testimonial(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    comment = models.TextField(max_length=440, blank=True, verbose_name='Отзыв')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='URL', unique=True)
    content = models.TextField(validators=[MinLengthValidator(255)], blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    banner_published = models.BooleanField(default=False, verbose_name='Опубликовать баннер')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья(ю)'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})


class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    inc = models.CharField(max_length=255, verbose_name='Include')
    slug = models.SlugField(max_length=255, verbose_name='URL', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Страница(у)'
        verbose_name_plural = 'Страницы'

    def get_absolute_url(self):
        return reverse('page', kwargs={'slug': self.slug})


class Email(models.Model):
    email = models.EmailField(verbose_name='Email')
    date = models.DateTimeField(verbose_name='Дата подписки', auto_now_add=True)

    class Meta:
        verbose_name = 'Подписчик(а)'
        verbose_name_plural = 'Подписчики'

    def __str__(self):
        return self.email
