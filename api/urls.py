from django.urls import re_path
from .views import *

urlpatterns = [
	re_path(r'^test/',test, name='test'),
    re_path(r'^getnonogram/',get_nonogram, name='getnonogram'),
    re_path(r'^scoreword/',score_word, name='scoreword'),
    re_path(r'^getsolution/',get_solution, name='getsolution'),#
    re_path(r'^getsolutionscored/',get_solution_with_score, name='getsolutionscored'),
]