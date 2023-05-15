from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import PortariaLoginView, PortariaHomeView, PortariaEntradaView, PortariaSaidaView, \
    PortariaLancaEntradaView, PortariaLancaSaidaView

app_name = 'portaria'

urlpatterns = [
    path("futurecode/portaria/login", PortariaLoginView.as_view(), name='portaria_login'),
    path("futurecode/portaria/home", PortariaHomeView.as_view(), name='portaria_home'),
    path("futurecode/portaria/entrada", PortariaEntradaView.as_view(), name='portaria_entrada'),
    path("futurecode/portaria/lancentrada/<int:id_visitante>", PortariaLancaEntradaView.as_view(), name='portaria_lancentrada'),
    path("futurecode/portaria/saida", PortariaSaidaView.as_view(), name='portaria_saida'),
    path("futurecode/portaria/lancsaida/<int:pk>", PortariaLancaSaidaView.as_view(), name='portaria_lancsaida'),
    path('futurecode/portaria/logout/', LogoutView.as_view(next_page='portaria:portaria_login'), name='portaria_logout'),
]
