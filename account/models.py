from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
class UserManager(BaseUserManager):
    def create_user(self, email, name, tc,  bio=None, phone_number=None, social_media_links=None, website=None,linkedin=None,twitter=None, instagram=None,youtube=None,facebook=None,password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            tc=tc,
            bio=bio,
            phone_number=phone_number,
            social_media_links=social_media_links,
            website=website,
            linkedin=linkedin,
            twitter=twitter,
            instagram=instagram,
            youtube=youtube,
            facebook=facebook
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, tc, password):
        user = self.create_user(
            email=email,
            name=name,
            tc=tc,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    name = models.CharField(max_length=200)
    tc = models.BooleanField()
    bio = models.TextField(blank=True, null=True)  # New field
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    social_media_links = models.TextField(blank=True, null=True)
    website = models.TextField(blank=True, null=True)
    linkedin = models.TextField(blank=True, null=True)
    twitter = models.TextField(blank=True, null=True)
    instagram = models.TextField(blank=True, null=True)
    youtube = models.TextField(blank=True, null=True)
    facebook = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'tc']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class ProfileImage(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='profile_images')
    image = models.ImageField(upload_to='user_image/', null=True, blank=True)

    def __str__(self):
        return self.image.url
    
class course (models.Model):
    id = models.AutoField(primary_key=True)  # a unique
    title = models.CharField(max_length=255, default="")
    link = models.CharField(max_length=255, default="")
    description = models.TextField(default="")
    image = models.ImageField(upload_to="course/images" , default="")
    
    def __str__(self):
        return self.title


class certificate (models.Model):
    id = models.AutoField(primary_key=True)  
    certificate_title = models.CharField(max_length=255)
    link = models.CharField(max_length=255, default="")
    description = models.TextField()
    courses = models.ForeignKey(course, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.certificate_title


class TestModel(models.Model):
    id = models.AutoField(primary_key=True)
    certificate = models.ForeignKey(certificate, on_delete=models.CASCADE) 
    certification_overview = models.JSONField(null=True , blank=True)
    Delivery_Methods = models.JSONField(null=True , blank=True)
    steps = models.JSONField(null=True , blank=True)
    Enterprise_Solutions = models.JSONField(null=True , blank=True)
    faqs = models.JSONField(null=True , blank=True)
    learning_outcomes = models.JSONField(null=True , blank=True)
    certificationSteps = models.JSONField(null=True , blank=True)
    resources_data = models.JSONField(null=True , blank=True)





class TrainingCalendar(models.Model):
    id = models.AutoField(primary_key=True)  
    
    certificate = models.ForeignKey(certificate, on_delete=models.CASCADE)
    courses = models.ForeignKey(course, on_delete=models.CASCADE)  # Add default value here
    LIVE_ONLINE = 'Live online'
    SELF_PLACED = 'Self-placed'
    DELIVERY_CHOICES = [
        (LIVE_ONLINE, 'Live online'),
        (SELF_PLACED, 'Self-placed'),
    ]
    delivery = models.CharField(
        max_length=255,
        choices=DELIVERY_CHOICES,
        null=False,
        blank=False,
    )
    start_date = models.DateField(default="")
    end_date = models.DateField(default="")
    time_zone = models.CharField(default="" , max_length=255)
    MRP = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f"{self.courses.title} - {self.certificate.certificate_title} - {self.delivery} "

        


    