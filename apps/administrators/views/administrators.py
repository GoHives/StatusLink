
""" admin's Views """

# Django
from concurrent.futures import process
from operator import is_
from django.views.generic import View,CreateView,TemplateView,DeleteView,DetailView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy




from ..models import LinkInfo,ProcessSteps

class AdminHomeView(TemplateView):
	def get(self, request, **kwargs):     
		return render(request, 'admin_home.html')


class LinkGeneratorView(CreateView):
	def get(self, request, **kwargs):     
		return render(request, 'link_generator.html')
		
	def post(self, request, **kwargs):     
	
		link_name = request.POST.get('link_name')
		
		link = LinkInfo()
		link.link_name = link_name
		link.save()

		return HttpResponseRedirect(self.get_success_url(link.pk))

	def get_success_url(self,link):
		# return reverse('teachers:planifications_list', )
		return reverse("administrators:link_generator_final_step", args=[link])
		# return reverse('administrators:link_generator_final_step')


class LinkGeneratorFinalStepView(View):
	def get(self, request, **kwargs):     
		pk=self.kwargs.get('pk', None)
		context= {}
		link_info=LinkInfo.objects.get(pk=pk)
		context['link_info'] = link_info
		return render(request, 'link_generator_final_step.html',context)
	
	def post(self, request, **kwargs):     
		pk=self.kwargs.get('pk', None)

		comments = request.POST.get('comments',None)
		

		last_link = LinkInfo.objects.get(pk=pk)
		last_link.comments = comments
		last_link.attachment = request.FILES['file']
		last_link.save()
		
		steps = request.POST.getlist('steps',None)
		
		for step in steps:
			if step == "":
				print('vacio')
			else:
				process_steps = ProcessSteps()
				process_steps.step_name = step
				process_steps.link_info = last_link
				process_steps.save()		

		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		return reverse('administrators:opened_links')


class PreviewView(View):
	model = ProcessSteps

	def get(self,request,**kwargs):
		context={}
		pk=self.kwargs.get('pk', None)

		processes = ProcessSteps.objects.filter(link_info=pk).order_by('pk')
		link_info=LinkInfo.objects.get(pk=pk)
		context['steps'] = processes
		context['link_info'] = link_info
		return render(request, 'preview.html',context)

	def post(self, request, **kwargs):     
		# comment = request.POST.get('comment',None)
		
		process_steps= ProcessSteps.objects.get(pk=request.POST.get('step', None))
		if process_steps.is_done == False:
			process_steps.is_done=True
		else:
			process_steps.is_done=False
		process_steps.save()

		# last_link = LinkInfo.objects.last()
		# last_link.comment = comment
		# last_link.save()
		
		# steps = request.POST.getlist('steps',None)
		
		# for step in steps:
		# 	if step == "":
		# 		print('vacio')
		# 	else:
		# 		process_steps = ProcessSteps()
		# 		process_steps.step_name = step
		# 		process_steps.link_info = last_link
		# 		process_steps.save()		
		return HttpResponseRedirect(self.request.path_info)

		# return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		return reverse('administrators:opened_links')

		


class OpenedLinksView(CreateView):
	def get(self, request, **kwargs):
		context={}
		opened_links = LinkInfo.objects.all().order_by('pk')
		context['opened_links'] = opened_links
		return render(request, 'opened_links.html',context)


class LinksDeleteView(DeleteView):
	model = LinkInfo
	success_url = reverse_lazy("administrators:opened_links")

