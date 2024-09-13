from django.contrib import admin
from django.urls import include, path
from graphene_django.views import GraphQLView
from music.schema import schema  
from django.views.decorators.csrf import csrf_exempt
from music.views import home 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path('', home, name='home'),
]
