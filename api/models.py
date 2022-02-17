from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class ExtraInfo(models.Model):
    genre = {
        (0, 'unknown'),
        (1, 'horror'),
        (2, 'sci-fi'),
        (3, 'drama'),
        (4, 'comedy'),
    }

    duration = models.IntegerField()
    film_genre = models.IntegerField(choices=genre, default=0)

    def __str__(self):
        return f'{self.film_genre} - {self.duration}'


class Film(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=256)
    premiere = models.BooleanField(default=False)
    release_date = models.DateField(null=True, blank=True)
    year = models.IntegerField()
    imdb_rating = models.DecimalField(max_digits=4, decimal_places=2,
                                      null=True, blank=True)
    extra_info = models.OneToOneField(ExtraInfo, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.my_name()

    def my_name(self):
        return f'{self.title} ({self.year})'


class Review(models.Model):
    description = models.TextField(default='')
    stars = models.IntegerField(default=5)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='reviews')


class Actor(models.Model):
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    films = models.ManyToManyField(Film)




