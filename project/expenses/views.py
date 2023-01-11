from django.views.generic.list import ListView
from django.db.models import Count, Sum, Q
from django.db.models.functions import ExtractMonth, ExtractYear
from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, summary_per_year_month


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            if name:
                queryset = queryset.filter(name__icontains=name)

        return super().get_context_data(
            form=form,
            object_list=queryset,
            total_spent=queryset.aggregate(total_spent=Sum('amount')),
            summary_per_category=summary_per_category(queryset),
            summary_per_year_month=summary_per_year_month(),
            **kwargs)

    def get_queryset(self, **kwargs):
        queryset = super(ExpenseListView, self).get_queryset()
        from_date = self.request.GET.get('from_date')
        to_date = self.request.GET.get('to_date')
        category = self.request.GET.getlist('category')
        sort_date = self.request.GET.get('sort_date')
        sort_category = self.request.GET.get('sort_category')
        year_month = self.request.GET.get('year_month')
        if from_date and to_date:
            return queryset.filter(date__range=(from_date, to_date))
        elif category:
            return queryset.filter(Q(category__in=category))
        elif sort_date:
            return queryset.order_by(sort_date)
        elif sort_category:
            return queryset.order_by(sort_category)
        elif year_month:
            return queryset.values('year_month').annotate(total_amount=Sum('amount')).annotate(
                month=ExtractMonth('date')
            ).annotate(year=ExtractYear('date')).order_by(
                'year', 'month')
        return queryset


class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get_queryset(self):
        return Category.objects.annotate(num_expenses=Count('expense'))
