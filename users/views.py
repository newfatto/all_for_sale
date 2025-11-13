from django.conf import settings
from django.contrib.auth import login
from django.core.mail import send_mail
from django.urls import reverse_lazy

from users.models import CustomUser
from users.forms import CustomUserCreationForm, CustomUserAuthenticationForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(CreateView):
    """Контроллер для регистрации нового пользователя.
    Создаёт пользователя, логинит, отправляет welcome-письмо.
    """
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        """
        Вызывается при валидной форме.
        Сохраняет пользователя, логинит его и отправляет письмо.
        """
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        self.send_welcome_email(user.email)
        return response

    def send_welcome_email(self, user_email):
        """
        Отправляет приветственное письмо новому пользователю.
        """
        subject = 'Skystore дождался тебя'
        message = ('Ура! Ты зарегистрирован на сайте'
                   'Теперь тебе доступно то, что доступно зарегистрированным пользователям')
        recipient_list = [user_email, ]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)


class CustomLoginView(LoginView):
    """ Контроллер авторизации пользователя. """
    form_class = CustomUserAuthenticationForm
    template_name = 'login.html'
    next_page = reverse_lazy('catalog:home')


class CustomLogoutView(LogoutView):
    """ Контроллер выхода пользователя из системы. """
    next_page = reverse_lazy('catalog:home')
