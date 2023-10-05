from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    price = models.IntegerField()
    image = models.ImageField(upload_to='upload/item')
    date = models.DateTimeField(auto_now_add=True)
    created = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

    def __str__(self) -> str:
        return self.name


class Conversation(models.Model):
    item = models.ForeignKey(Item, related_name='conversations', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='conversation')
    date = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-modified']


    def __str__(self) -> str:
        return self.item

class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    created = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.date

