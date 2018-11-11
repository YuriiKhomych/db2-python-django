from django.db import models
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=60, null=False, blank=False)
    body = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='author',
        on_delete=models.CASCADE
    )
    post_image = models.FileField(upload_to='post_images/',
                              blank=True, null=True)
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      related_name='liked')
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} | {self.body} | {self.author} | {self.liked_by}'


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="comment_author",
                               on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments",
                             null=True, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ("author", "post")

    def __str__(self):
        return f"{self.author} | {self.post}"
