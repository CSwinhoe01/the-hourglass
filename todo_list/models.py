from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class TaskQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user=user)

    def search(self, query: str):
        if not query:
            return self
        return self.filter(title__icontains=query)

class TaskManager(models.Manager.from_queryset(TaskQuerySet)):
    pass

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    category = models.ForeignKey(
        'Category',  # or 'todo_list.Category'
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks',
    )

    objects = TaskManager()  # enables .for_user() and .search()

    def __str__(self):
        return self.title