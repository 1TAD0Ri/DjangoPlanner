from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class todo(models.Model):
    # ForeignKey to link each todo item to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Field to store the name of the todo item
    todo_name = models.CharField(max_length=1000)

    # Model-level validation to ensure todo_name is not empty
    def clean(self):
        if not self.todo_name.strip():
            raise ValidationError("Task name cannot be empty")

    # Override the save method to perform validation before saving
    def save(self):
        self.full_clean()  # Ensure model validation before saving
        super(todo, self).save()

    # Field to store the completion status of the todo item
    status = models.BooleanField(default=False)

    # Method to represent the object as a string
    def __str__(self):
        return self.todo_name
