from django.shortcuts import render
from django.http import HttpResponse
from .forms import CriteriaForm
from .createmap import getmap


# Create your views here.

def home(request):
    """
    This function should define what the home page
    should look like
    You should be able to pass an entire html page
    to HttpResponse and it probably will work?
    """

    if request.method == 'POST':
        form = CriteriaForm(request.POST)
        if form.is_valid():
            crit_1 = form.cleaned_data('criteria_1')
            crit_2 = form.cleaned_data('criteria_2')
            crit_3 = form.cleaned_data('criteria_3')

            getmap(crit_1, crit_2, crit_3)

            return render('result.html')
    else:
        form = CriteriaForm()

    return render(request, 'home.html', {'form' : form})
