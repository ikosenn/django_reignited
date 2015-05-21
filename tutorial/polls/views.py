
from django.shortcuts import render

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views import generic

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import Question
from .models import Choice
# Create your views here.
def index(request):
    #return HttpResponse("Hello world you are at the index")
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #output = ', '.join([p.question_text for p in latest_question_list])
    #return HttpResponse(output)
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # context = RequestContext(request, {
    #     'latest_question_list': latest_question_list,
    # })
    # return HttpResponse(template.render(context))
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    # return HttpResponse("You're looking at question %s." % question_id)
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    #response = "You're looking at the results of question %s."
    #return HttpResponse(response % question_id)

    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls/results.html', {'question':question})

def vote(request, question_id):
   # return HttpResponse("You're voting on question %s." % question_id)

    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST.get('choice'))
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):

        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
