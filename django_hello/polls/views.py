from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from polls.models import Choice, Poll


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_poll_list'
	
	def get_queryset(self):
		return Poll.objects.filter(
			pub_date__lte=timezone.now()
		).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
	model = Poll
	template_name = 'polls/detail.html'
	
	def get_queryset(self):
		return Poll.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
	model = Poll
	template_name = 'polls/results.html'


#def index(request):
#	latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
#	return render(request, 'polls/index.html', {'latest_poll_list':latest_poll_list})

#def detail(request, poll_id):
#	poll = get_object_or_404(Poll, pk=poll_id)
#	return render(request, 'polls/detail.html', {'poll':poll})
	
#def results(request, poll_id):
#	poll = get_object_or_404(Poll, pk=poll_id)
#	return render(request, 'polls/results.html', {'poll':poll})
	
def vote(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'poll':p,
			'error_message':"You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
	return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
