import io


from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


from .models import Scientist, Category


# class ScientistModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content


# class ScientistSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     content = serializers.CharField()
#     time_create = serializers.DateTimeField(read_only=True)
#     time_update = serializers.DateTimeField(read_only=True)
#     is_published = serializers.BooleanField(default=True)
#     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    

#     def create(self, validated_data):
#         return Scientist.objects.create(**validated_data)
    

#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.content = validated_data.get('content', instance.content)
#         instance.is_published = validated_data.get('is_published', instance.is_published)
#         instance.category = validated_data.get('category', instance.category)
#         instance.save()
#         return instance


class ScientistSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Scientist
        fields =  "__all__" # так можно указать все поля. Можно и некоторые - ['title', 'content', 'time_create']


# def encode():
#     model = ScientistModel('Владимир Сурдин', 'Астроном')
#     model_sr = ScientistSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)


# def decode():
#     stream = io.BytesIO(b'{"title":"\xd0\x92\xd0\xbb\xd0\xb0\xd0\xb4\xd0\xb8\xd0\xbc\xd0\xb8\xd1\x80 \xd0\xa1\xd1\x83\xd1\x80\xd0\xb4\xd0\xb8\xd0\xbd","content":"\xd0\x90\xd1\x81\xd1\x82\xd1\x80\xd0\xbe\xd0\xbd\xd0\xbe\xd0\xbc"}')
#     data = JSONParser().parse(stream)
#     serializer = ScientistSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)
