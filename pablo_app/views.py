import io

from PIL import Image
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from django.http import HttpResponse
from django.shortcuts import get_list_or_404, render

from .serializers import ContentImageSerializer, ArtistSerializer, PaintingSerializer
from .models import Artist, Painting
from .style_transfer.transfer import transfer_style


def index(request):
    return render(request, 'index.html')


class ContentImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        print(repr(request))

        print(repr(request.data))
        content_image_serializer = ContentImageSerializer(data=request.data)

        print(repr(content_image_serializer))

        print(content_image_serializer.is_valid())

        img = {}
        if content_image_serializer.is_valid():
            uploaded_content_image = content_image_serializer.save()
            file_name = uploaded_content_image.file.name
            style_image = uploaded_content_image.style

            print(uploaded_content_image, file_name, style_image)

            img = transfer_style("media/" + file_name,
                                 "pablo_app" + style_image)

            print(repr(img))

        try:
            with io.BytesIO() as byte_stream:
                img.save(byte_stream, format="JPEG")
                byte_stream.seek(0)
                return HttpResponse(byte_stream.read(), content_type="image/jpeg")
        except IOError:
            red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
            response = HttpResponse(content_type="image/jpeg")
            red.save(response, "PNG")
            return response


class ArtistView(APIView):
    def get(self, request):
        artists = get_list_or_404(Artist)
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)


class PaintingView(APIView):
    def get(self, request, artist_id):
        try:
            if artist_id is not None:
                paintings = get_list_or_404(Painting, artist=artist_id)
                serializer = PaintingSerializer(paintings, many=True)

                return Response(serializer.data)
        except:
            return Response("Artist not found", status=status.HTTP_404_NOT_FOUND)
