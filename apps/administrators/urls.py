"""Circles URLs."""

# Django
from django.urls import path
from .views.administrators import *
# Views

from .views import *

urlpatterns = [
	path('home',AdminHomeView.as_view(),name="admin_home"),
	path('link-generator',LinkGeneratorView.as_view(),name="link_generator"),
	path('link-generator-final-step/<pk>',LinkGeneratorFinalStepView.as_view(),name="link_generator_final_step"),
	path('preview/<pk>',PreviewView.as_view(),name="preview"),
	path('opened-links',OpenedLinksView.as_view(),name="opened_links"),
	path('link/<pk>',LinksDeleteView.as_view(),name="delete_link"),
	
]