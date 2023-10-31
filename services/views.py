from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import FormView

from .forms import ContactForm, EmailForm
from .models import Email, Page, Post


class Home(ListView):
    model = Page
    template_name = "services/index.html"
    context_object_name = "pages"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Hlavní"
        return context


class ShowPage(Home):
    template_name = "services/page.html"


class GetPost(DetailView):
    model = Post
    template_name = "services/single.html"
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Hlavní"
        return context


class Search(ListView):
    template_name = "services/search.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get("s"))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["s"] = f"s={self.request.GET.get('s')}&"
        return context


class EmailView(CreateView):
    model = Email
    form_class = EmailForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request, "Úspěšně odbíráte.")
            form.save()
            return redirect(reverse("home") + "#email")

        messages.error(request, "E-mail uveden nesprávně")
        return redirect(reverse("home") + "#email")


class ContactFormView(FormView):
    template_name = "services/contact.html"
    form_class = ContactForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = Page.objects.get(slug="rezervace").title
        context["title"] = title
        return context

    def form_valid(self, form):
        self.send_email(**form.cleaned_data)
        return render(
            self.request, "services/contact.html", self.get_context_data(success=True)
        )

    @staticmethod
    def send_email(name, number, email, message):
        text = get_template("services/message.txt")
        html = get_template("services/message.html")
        context = {"name": name, "number": number, "email": email, "message": message}
        subject = "Klientská zprava"
        from_email = settings.EMAIL_HOST_USER
        text_content = text.render(context)
        html_content = html.render(context)

        msg = EmailMultiAlternatives(
            subject, text_content, from_email, ["podgorniy.inc@gmail.com"]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
