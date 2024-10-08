from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from utils.rands import slugify_new
from django.db.models import Q
from utils.images import resize_image


class Technology(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='portfolio/tecnology/icons')

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        current_icon_name = str(self.icon.name)
        super().save(*args, **kwargs)
        icon_changed = False

        if self.icon:
            icon_changed = current_icon_name != self.icon.name

        if icon_changed:
            resize_image(self.icon, 100)
        return super().save(*args, **kwargs)


class ProjectManager(models.Manager):
    """ Project object manager """
    def get_projects(self):
        return self.filter(is_published=True).order_by('-id')
    
    def get_search(self, search_value) -> filter:
        """
        get projects by search value
        """
        return self.filter(
            Q(name__icontains=search_value) |
            Q(description__icontains=search_value) |
            Q(technologies__name__icontains=search_value)
        ).filter(is_published=True).order_by('-id').distinct()


class Project(models.Model):

    objects = ProjectManager()
    
    name = models.CharField(max_length=255, verbose_name=_('Nome'))
    description = models.CharField(max_length=255, verbose_name=_('Descrição'))
    cover = models.ImageField(upload_to='projects/%Y/%m', verbose_name=_('Capa'))
    app_link = models.URLField(default='', blank=True, verbose_name=_('Link da aplicação'))
    repository_link = models.URLField(default='', blank=True, verbose_name=_('link do repositório'))
    slug = models.SlugField(unique=True, blank=True)
    is_published = models.BooleanField(default=True, verbose_name=_('Está publicado?'))
    technologies = models.ManyToManyField(Technology, blank=True, verbose_name=_('Tecnologias'))

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Project_detail", kwargs={"pk": self.pk})
    
    def save(self, *args, **kwargs):
        if not self.app_link and not self.repository_link:
            self.is_published = False

        if not self.slug:
            self.slug = slugify_new(self.name)

        current_cover_name = str(self.cover.name)
        super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        if cover_changed:
            resize_image(self.cover, 900)

        super().save(*args, **kwargs)
