from django_filters import FilterSet
from django_filters.filters import CharFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    """
    Filter for the Title model. Searches by fields "name", "year", "genre",
    "category".
    """
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')
    name = CharFilter(field_name='name', method='name_filter')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'year', 'name')

    def name_filter(self, queryset, name, name_start):
        return queryset.filter(name__startswith=name_start)
