from django.db import models
from ..users.models import User

# Create your models here.
class PostManager(models.Manager):
    def validate(self,form):
        errors=[]
        if len(form['content'])<1:
            errors.append("Post no contain any character")
        return errors
    def create_post(self, form,user_id):
        try:
            user=User.objects.get(id=user_id)
            self.create(
                content=form['content'],
                created_by=user
        )
        except:
            print("ERORR WHILE CREATING POST --> USER DOESN'T EXIST")
class Post(models.Model):
    content=models.TextField()
    created_by=models.ForeignKey(User, related_name="posts")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects=PostManager()