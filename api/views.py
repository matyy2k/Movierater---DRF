from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer, FilmSerializer, ReviewSerializer, ActorSerializer #FilmMiniSerializer
from .models import Film, Review, Actor
from rest_framework.response import Response
from django.http.response import HttpResponseNotAllowed
from rest_framework.decorators import action
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissions

# pagination
class FilmsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class FilmViewSet(viewsets.ModelViewSet):
    serializer_class = FilmSerializer
    filterset_fields = ['title', 'description', 'year']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = '__all__'
    ordering = ['year', ]
    pagination_class = FilmsSetPagination
    authentication_classes = [TokenAuthentication, ]
    # permission_classes = [IsAuthenticatedOrReadOnly, ]
    permission_classes = [DjangoModelPermissions, ]

    def get_queryset(self):
        # year = self.request.query_params.get('year', None)
        # id = self.request.query_params.get('id', None)
        #
        # if id:
        #     qs = Film.objects.filter(id=id)
        # else:
        #     if year:
        #         qs = Film.objects.filter(year=year)
        #     else:
        #         qs = Film.objects.all()
        qs = Film.objects.all()
        return qs

    # def list(self, request, *args, **kwargs):
    #     title = self.request.query_params.get('title', None)
    #     # films = Film.objects.filter(title__exact=title)
    #     # films = Film.objects.filter(title__contains=title)
    #     films = Film.objects.filter(release_date__gte='2000-01-01')
    #
    #     serializer = FilmSerializer(films, many=True)
    #     return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = FilmSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # if request.user.is_superuser:
        film = Film.objects.create(
            title=request.data['title'],
            description=request.data['description'],
            premiere=request.data['premiere'],
            year=request.data['year'],
        )
        serializer = FilmSerializer(film, many=False)
        return Response(serializer.data)
        # else:
        #     return HttpResponseNotAllowed('Not allowed')

    def update(self, request, *args, **kwargs):
        film = self.get_object()
        film.title = request.data['title']
        film.description = request.data['description']
        film.premiere = request.data['premiere']
        film.year = request.data['year']
        film.save()
        serializer = FilmSerializer(film, many=False)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        film = self.get_object()
        film.delete()
        return Response('Film deleted')

    @action(detail=True)
    def premiere(self, request, **kwargs):
        film = self.get_object()
        film.premiere = True
        film.save()

        serializer = FilmSerializer(film, many=False)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def all_premiere(self, request, **kwargs):
        films = Film.objects.all()
        films.update(premiere=request.data['premiere'])

        serializer = FilmSerializer(films, many=True)
        return Response(serializer.data)


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    @action(detail=True, methods=['POST'])
    def join(self, request, **kwargs):
        actor = self.get_object()
        film = Film.objects.get(id=request.data['film'])
        actor.films.add(film)

        serializer = ActorSerializer(actor, many=False)
        return Response(serializer.data)
