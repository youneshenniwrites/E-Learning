from rest_framework import serializers

from ..models import Subject, Course, Module, Content


class ItemRelatedField(serializers.RelatedField):
    '''
    Custom field to be used for
    the item generic foreign key
    '''

    def to_representation(self, value):
        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order', 'item']


class ModuleWithContentSerializer(serializers.ModelSerializer):
    '''
    Module serializer including its contents
    '''
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ['order', 'title', 'description', 'contents']


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']


class CourseWithContentSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'subject',
                    'title', 'slug',
                    'overview', 'created',
                    'owner', 'modules'
                    ]


class CourseSerializer(serializers.ModelSerializer):
    '''
    Nesting the ModuleSerializer
    '''

    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'subject',
                    'title', 'slug',
                    'overview', 'created',
                    'owner', 'modules'
                    ]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']
