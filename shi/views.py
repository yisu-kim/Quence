from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Shi, Choice
from .forms import ShiForm
from .quence import Quence


class IndexView(generic.ListView):
    template_name = 'shi/index.html'
    context_object_name = 'latest_shi_list'

    def get_queryset(self):
        """Return the last five published shis."""
        return Shi.objects.filter(published_date__lte=timezone.now()).order_by('-published_date') #[:5]


class DetailView(generic.DetailView):
    model = Shi
    context_object_name = 'shi'
    template_name = 'shi/detail.html'


def quence(shi, text):
    q = Quence()
    output = q.call_tf(text)
    for out in output:
        choice = Choice()
        choice.input = shi
        choice.choice_text = out
        choice.save()


def new(request):
    if request.method == "POST":
        form = ShiForm(request.POST)
        if form.is_valid():
            shi = form.save(commit=False)
            shi.save()
            quence(shi, shi.input_text)
            return redirect('shi:detail', pk=shi.pk)
    else:
        form = ShiForm()
    return render(request, 'shi/new.html', {'form': form})


def select(request, input_id):
    shi = get_object_or_404(Shi, pk=input_id)
    try:
        selected_choice = shi.choice_set.get(pk=request.POST['choice'])
        shi.choice_set.exclude(pk=request.POST['choice']).delete()
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the voting form.
        return render(request, 'shi/detail.html', {
            'shi': shi,
            'error_message': "You didn't select a choice.",
        })
    else:
        output_text = shi.output_text
        output_text += selected_choice.choice_text + '\n'
        shi.output_text = output_text
        shi.save()
        return render(request, 'shi/detail.html', {'shi': shi,})


def make(request, input_id):
    shi = get_object_or_404(Shi, pk=input_id)
    choice = shi.choice_set.get()
    choice_text = choice.choice_text
    shi.choice_set.all().delete()
    quence(shi, choice_text)
    return render(request, 'shi/detail.html', {'shi': shi,})


def draft(request):
    shi = Shi.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'shi/draft.html', {'shi': shi,})


def publish(request, input_id):
    shi = get_object_or_404(Shi, pk=input_id)
    shi.publish()
    shi.choice_set.all().delete()
    return redirect('shi:detail', pk=shi.pk)