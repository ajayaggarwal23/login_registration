from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
PW_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}')

class UserManager(models.Manager):
    def create_user(self, data):
        errors = []
        try:
            user_check = Userentry.objects.get(email=data['email'])
            print user_check
            if user_check.email == data['email']:
                errors.append("Email Already Registered -- Try a New Email Address")
        except:
            pass
        if not EMAIL_REGEX.match(data['email']):
            errors.append("Not a valid email address")
        if any(i.isdigit() for i in data['first']):
            errors.append("No numbers in First Name")
        if any(i.isdigit() for i in data['last']):
                errors.append("No numbers in Last name")
        if len(data['first']) < 2:
            errors.append("First Name Must Be 2 or more characters")
        if len(data['last']) < 2:
            errors.append("Last Name Must Be 2 or more characters")
        # if not PW_REGEX.match(data['passwd']):
        #     errors.append("Password Minimum 8 characters and atleast 1 Alphabet, 1 Number and 1 Special Character")
        if len(data['passwd']) < 8:
            errors.append("Password Must Be atleast 8 characters")
        if len(data['passwdconf']) < 8:
            errors.append("Password Confirmation Must Be atleast 8 characters")
        if data['passwd'] != data['passwdconf']:
            errors.append("Passwords Must Match")
        if errors:
            return (False, errors)
        else:
            hashed = bcrypt.hashpw(data['passwd'].encode(), bcrypt.gensalt())
            new_entry = Userentry.objects.create(email=data['email'], first=data['first'], last=data['last'], passwd=hashed)
            return (True, new_entry)

    def check_user(self, data):
        errors = []
        try:
            returned = Userentry.objects.get(email=data['email'])
            if bcrypt.checkpw(data['passwd'].encode(), returned.passwd.encode()):
                return (True, returned)
        except:
            errors.append("Not a valid email address or password")
            return (False, errors)


class Userentry(models.Model):
    email = models.EmailField(max_length=255)
    first = models.CharField(max_length=255)
    last = models.CharField(max_length=255)
    passwd = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
