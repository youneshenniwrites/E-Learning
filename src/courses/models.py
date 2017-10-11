'''
The course data structure will look something like this
Subject 1
    Course 1
        Module 1
            Content 1 (image)
            Content 3 (text)
        Module 2
            Content 4 (text)
            Content 5 (file)
            Content 6 (video)
            ...
'''


from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Subject(models.Model):
    title   = models.CharField(max_length=200)
    slug    = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ('title', )


class Course(models.Model):
    '''
    each course belongs to an owner and a specific subject
    '''

    owner       = models.ForeignKey(User,
                            related_name='courses_created')
    subject     = models.ForeignKey(Subject,
                            related_name='courses')
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(max_length=200, unique=True)
    overview    = models.TextField()
    created     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ('-created', )


class Module(models.Model):
    '''
    each course is divided into several modules
    '''

    course      = models.ForeignKey(Course,
                                    related_name='modules')
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.title)


class Content(models.Model):
    '''
    a versatile data model to store
    diverse content by using GenericForeignKey
    to associate any kind or type of content
    '''

    module          = models.ForeignKey(Module,
                                        related_name='contents')
    content_type    = models.ForeignKey(ContentType,
                                        limit_choices_to={
                                        'model__in': ('text',
                                                        'video',
                                                        'image',
                                                        'file')
                                                        })
    object_id       = models.PositiveIntegerField()
    item            = GenericForeignKey('content_type', 'object_id')


class ItemBase(models.Model):
    '''
    an abstract model that provides the
    common fields for all content models
    '''

    owner       = models.ForeignKey(User,
                            related_name='%(class)s_related')
    title       = models.CharField(max_length=200)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        abstract = True


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    '''
    a url must be provided to embed a video
    '''

    url = models.URLField()
