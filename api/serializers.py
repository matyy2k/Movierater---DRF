from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Film, ExtraInfo, Review, Actor
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups', 'password']
        extra_kwargs = {'password': {'required': True, 'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)


class ExtraInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraInfo
        fields = ['duration', 'film_genre']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        # depth = 2
        # exclude = ('title')
        # read_only_fields = ('film', 'id')

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.stars = validated_data.get('stars', instance.stars)
        instance.save()

        return instance


class FilmSerializer(serializers.ModelSerializer):
    extra_info = ExtraInfoSerializer(many=False)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Film
        fields = ['id', 'title', 'description', 'premiere',
                  'release_date', 'year', 'imdb_rating', 'my_name',
                  'extra_info', 'reviews']
        read_only_fields = ('extra_info', 'reviews')


class FilmMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['id', 'title', 'year']


class ActorSerializer(serializers.ModelSerializer):
    films = FilmMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ['id', 'name', 'surname', 'films']

    # def create(self, validated_data):
    #     films = validated_data['films']
    #     del validated_data['films']
    #
    #     actor = Actor.objects.create(**validated_data)
    #
    #     for film in films:
    #         f = Film.objects.create(**film)
    #         actor.films.add(f)
    #
    #     actor.save()
    #     return actor






