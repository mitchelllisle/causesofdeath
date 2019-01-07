from django import forms
from .utils import autocomplete_categories
from .utils import get_category_detail
from .utils import readData
from .charts import timeseries_chart
from .charts import roc_chart

data = readData()


class ChapterLookup(forms.Form):
    category = forms.TypedChoiceField(
        choices=autocomplete_categories()
    )
    category.widget.attrs.update({'id': 'category', 'onchange': 'this.form.submit()'})

    def search(self):
        selected_category = self.cleaned_data['category']

        output = {
            "category": selected_category,
            "category_detail": get_category_detail(selected_category),
            "timeseries_chart": timeseries_chart(data, selected_category),
            "roc_chart": roc_chart(data, selected_category)
        }
        return output
