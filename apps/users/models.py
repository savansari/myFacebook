from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX=re.compile(r'^[A-Za-z]+$')
# Create your models here.

class UserManager(models.Manager):
   def validate(self,form):
      errors=[]
      if len(form['first_name'])<3:
         errors.append("First Name must have at least 3 characters lenght")
      if len(form['last_name'])<3:
         errors.append("Last Name must have at least 3 characters lenght")
      if len(form['username'])<3:
         errors.append("Username must have at least 3 characters lenght")
      if not EMAIL_REGEX.match(form['email']):
         errors.append("Email must be valid")
      if len(form['password']) < 8:
         errors.append("Password must be at least 8 characters long")
      users=self.filter(email=form['email'])
      if len(users)>0:
         errors.append('email is in use')
      user_list = self.filter(username=form['username'])
      if len(user_list) > 0:
         errors.append("Username already in use")  
      if form['password']!= form['confirm']:
         errors.append("Password and confrim i snot matched")  
      return errors
   def create_user_with_hash(self,form):
      pw_hash=bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
      user=self.create(
         first_name = form['first_name'],
         last_name = form['last_name'],
         email = form['email'],
         username = form['username'],
         pw_hash = pw_hash
      )
      return user
   def FindUser(self, form):
      errors=[]
      print (form['email'])
      try:
         user=self.get(email=form['email'])
         print ("yes")
         if not bcrypt.checkpw(form['password'].encode(), user.pw_hash.encode()):
            errors.append("Email or password incorrect")
      except:
         print ("No")
         errors.append("Email or password incorrect")
      if len(errors) > 0:
         return (False, errors)
      else:
         return (True, user)
   def create_request(self, form,user_id):
      try:
         from_user=self.get(id=user_id)
         to_user=self.get(id=form['request_to'])
      except:
         print('Somethin going wrong')
      Request.objects.create(
         request_from=from_user,
         request_to=to_user
      )
   def delete_request(self, form, user_id):
      sent_by = self.get(id = user_id)
      sent_to = self.get(id = form['request_to'])
      requests = Request.objects.filter(request_from = sent_by).filter(request_to = sent_to)
      if requests:
         requests[0].delete()

class User(models.Model):
   first_name=models.CharField(max_length=255)
   last_name=models.CharField(max_length=255)
   username=models.CharField(max_length=255)
   email=models.CharField(max_length=255)
   pw_hash=models.CharField(max_length=500)
   created_at=models.DateTimeField(auto_now_add=True)
   updated_at=models.DateTimeField(auto_now=True)

   objects=UserManager()

   def __fullname__(self):
      return (self.first_name  + self.last_name)
 
class Request(models.Model):
  request_from = models.ForeignKey(User, related_name = "requests_sent")
  request_to = models.ForeignKey(User, related_name = "requests_received")
  
