from rest_framework import serializers
from .models import ContentImage, Artist, Painting


class ContentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentImage
        fields = ('file', 'timestamp', 'style')


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name', 'years', 'genre', 'nationality', 'bio', 'wikipedia')


class PaintingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Painting
        fields = ('id', 'artist', 'path')