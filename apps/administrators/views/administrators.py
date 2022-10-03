
""" admin's Views """

# Django
from concurrent.futures import process
from operator import is_
from urllib import request
from django.views.generic import View,CreateView,TemplateView,DeleteView,DetailView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import JsonResponse





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
		last_link.attachment = request.FILES.get('file',None)
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



		# guardar lo creado en una session
		self.request.session['last_link'] = last_link.pk
		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		return reverse('administrators:opened_links')


class LinkDetailView(View):
	model = ProcessSteps

	def get(self,request,**kwargs):
		context={}
		pk=self.kwargs.get('pk', None)

		processes = ProcessSteps.objects.filter(link_info=pk).order_by('pk')
		link_info=LinkInfo.objects.get(pk=pk)
		context['steps'] = processes
		context['link_info'] = link_info
		return render(request, 'detail.html',context)

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
		if self.verify_session() == None:
			print('no hacer nada')
		else:
			context['link'] = self.verify_session()
			del self.request.session['last_link']
		opened_links = LinkInfo.objects.all().order_by('pk')
		context['opened_links'] = opened_links
		return render(request, 'opened_links.html',context)

	def verify_session(self):	
		if 'last_link' in self.request.session:
			return self.request.session['last_link']
		else:
			return None

class LinksDeleteView(DeleteView):
	model = LinkInfo
	success_url = reverse_lazy("administrators:opened_links")


class CancelView(View):
	def get(self, request, **kwargs):
		print('cancelar')
		context={}
		pk=self.kwargs.get('pk', None)
		print('verificar',pk)
		LinkInfo.objects.get(pk=pk).delete()
		print('borra')

		return HttpResponseRedirect(self.get_success_url())

		# return reverse("administrators:link_generator")

	def get_success_url(self):
			# return reverse('teachers:planifications_list', )
		return reverse("administrators:link_generator")		# return render(request, 'opened_links.html',context)


class GetLinkView(View):
	context_object_name = 'calendar_homeworks_list'

	def get(self, request, **kwargs):
		pk=self.kwargs.get('pk', None)
		
		
		link_info = LinkInfo.objects.filter(pk=pk).values('pk')
		
		return JsonResponse(list(link_info), status = 200,safe=False)



class FinalLinkView(View):

	def get(self,request,**kwargs):
		context={}
		pk=self.kwargs.get('pk', None)

		processes = ProcessSteps.objects.filter(link_info=pk).order_by('pk')
		link_info=LinkInfo.objects.get(pk=pk)
		context['steps'] = processes
		context['link_info'] = link_info
		return render(request, 'final_link.html',context)





