from django.db import models
from django.utils.text import slugify
from accounts.models import CustomUser as User
from django.db.models import Q
from django.utils import timezone
from django.urls import reverse
from utils.images import resize_image
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Nome'))
    slug = models.SlugField(unique=True, blank=True)
    color = models.CharField(
        max_length=7,
        default="#FFFFFF",
        help_text=_("Escolha uma cor em formato hexadecimal"),
        verbose_name=_('Cor')
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class PostManager(models.Manager):
    """
    Post object manager
    """
    def get_posts(self):
        return self.filter(published=True).order_by('-published_at')
    
    def get_search(self, search_value) -> filter:
        """
        get posts by search value
        """
        return self.filter(
            Q(description__icontains=search_value) |
            Q(title__icontains=search_value) |
            Q(content__icontains=search_value) |
            Q(category__name__icontains=search_value)
        ).filter(published=True).order_by('-published_at')


class Post(models.Model):

    objects = PostManager()

    title = models.CharField(max_length=100, verbose_name=_('Titulo'))
    cover = models.ImageField(upload_to='posts/%Y/%m')
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(
        max_length=255,
        verbose_name=_('Descrição')
    )
    content = models.TextField(verbose_name=_('Contéudo'))
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('autor')
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Categoria')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Criado em')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Atualizado em')
    )
    published_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Publicado em')
    )
    published = models.BooleanField(
        default=False,
        verbose_name=_('publicado')
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        current_cover_name = str(self.cover.name)
        super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        if cover_changed:
            resize_image(self.cover, 900)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})
