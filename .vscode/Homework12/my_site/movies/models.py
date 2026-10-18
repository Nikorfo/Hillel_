from django.db import models
from django.db.models import Q
 
 
class Studio(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name="Назва")
    country = models.CharField(max_length=60, blank=True, default="", verbose_name="Країна")
    founded_year = models.PositiveSmallIntegerField(null=True, blank=True)
 
    def __str__(self):
        return self.name
 
    class Meta:
        ordering = ["name"]
        verbose_name = "Студія"
        verbose_name_plural = "Студії"
 
 
class Actor(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    birth_date = models.DateField(null=True, blank=True)
 
    class Meta:
        ordering = ["last_name", "first_name"]
 
    def __str__(self):
        return self.full_name
 
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
 
 
class Movie(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft"
        RELEASED = "released"
        ARCHIVED = "archived"
 
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, default="")
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    duration_min = models.PositiveSmallIntegerField(null=True, blank=True)
 
    actors = models.ManyToManyField(Actor, blank=True, related_name="movies")
    studio = models.ForeignKey(
        Studio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="movies",
    )
 
    status = models.CharField(max_length=10, choices=Status, default=Status.DRAFT)
 
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.title
 
    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status", "-updated_at"])]
        constraints = [
            models.CheckConstraint(condition=~Q(title=""), name="movie_title_not_empty")
        ]
# Create your models here.
