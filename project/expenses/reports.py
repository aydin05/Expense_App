from collections import OrderedDict

from django.db.models import Sum, Value
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models.functions import Coalesce
from .models import Expense


def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset.annotate(category_name=Coalesce('category__name', Value('-'))).order_by().values(
            'category_name').annotate(s=Sum('amount')).values_list('category_name', 's')))


def summary_per_year_month():
    expenses = Expense.objects.annotate(
        year=ExtractYear('date'),
        month=ExtractMonth('date'),
    ).values('year', 'month').annotate(total_amount=Sum('amount')).order_by('year', 'month')

    summary = OrderedDict()
    for expense in expenses:
        year_month = f"{expense['month']}/{expense['year']}"
        summary[year_month] = expense['total_amount']
    return summary
