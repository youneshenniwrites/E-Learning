from rest_framework import serializers

from ..models import Subject, Course, Module


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']


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
