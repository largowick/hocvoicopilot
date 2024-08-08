from django.db import models

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    time_pub = models.DateTimeField()
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    vote = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text


from django.db import models
from django.contrib.auth.models import User



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='posts/images/', default='default.jpg')
    face_detection_results = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.title

    def has_faces_detected(self):
        return bool(self.face_detection_results)

class Item(models.Model):
    id_product = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return self.title
