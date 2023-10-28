from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormView
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.conf import settings
from .models import Page, Post, Email
from .forms import ContactForm, EmailForm


class Home(ListView):
    model = Page
    template_name = 'services/index.html'
    context_object_name = 'pages'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context


class ShowPage(Home):
    template_name = 'services/page.html'


class GetPost(DetailView):
    model = Post
    template_name = 'services/single.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context


class Search(ListView):
    template_name = 'services/search.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context


class EmailView(CreateView):
    model = Email
    form_class = EmailForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request, 'Новостная рассылка оформлена.')
            form.save()
            return redirect(reverse('home') + '#email')

        messages.error(request, 'Email указан неверно.')
        return redirect(reverse('home') + '#email')


class ContactFormView(FormView):
    template_name = 'services/contact.html'
    form_class = ContactForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = Page.objects.get(slug='svyazhites-s-nami').title
        context['title'] = title
        return context

    def form_valid(self, form):
        self.send_email(**form.cleaned_data)
        return render(self.request, 'services/contact.html', self.get_context_data(success = True))

    @staticmethod
    def send_email(name, number, email, message):
        text = get_template('services/message.txt')
        html = get_template('services/message.html')
        context = {'name': name, 'number':number, 'email': email, 'message': message}
        subject = 'Сообщение от клиента'
        from_email = settings.EMAIL_HOST_USER
        text_content = text.render(context)
        html_content = html.render(context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, ['podgorniy.inc@gmail.com'])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
