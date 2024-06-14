from django.db import models
from django.urls import reverse


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('moviereviewapp:categorylist', args=[self.slug])


class Movies(models.Model):

    title=models.CharField(max_length=250)
    slug = models.SlugField(max_length=200)
    category=models.ForeignKey(Category, related_name='movies', on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    desc=models.TextField()
    actors=models.TextField()
    release_date=models.DateField()
    poster=models.ImageField(upload_to='gallery')
    utube_link=models.URLField(max_length=250)
    login_user=models.IntegerField()

    class Meta:
        verbose_name = 'movie'
        verbose_name_plural = 'movies'

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('moviereviewapp:categorylist', args=[self.category.slug, self.slug])


class Details(models.Model):

    movie_title=models.ForeignKey(Movies,on_delete=models.CASCADE)
    review=models.TextField()
    rating=models.DecimalField(max_digits=2,decimal_places=1)


    def __str__(self):
        return f"{self.movie_title.title} - {self.rating}"




