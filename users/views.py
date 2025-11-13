from django.conf import settings
from django.contrib.auth import login
from django.core.mail import send_mail
from django.urls import reverse_lazy

from users.models import CustomUser
from users.forms import CustomUserCreationForm

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
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        """
        Вызывается при валидной форме.
        Сохраняет пользователя, логинит его и отправляет письмо.
        """
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        """
        Отправляет приветственное письмо новому пользователю.
        """
        subject = 'Skystore дождался тебя'
        message = ('Ура! Ты зарегистрирован на сайте'
                   'Теперь тебе доступно то, что доступно зарегистрированным пользователям')
        recipient_list = [user_email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)


class CustomLoginView(LoginView):
    """ Контроллер авторизации пользователя. """
    template_name = 'registration/login.html'
    success_url = reverse_lazy('catalog:home')


class CustomLogoutView(LogoutView):
    """ Контроллер выхода пользователя из системы. """
    def get_next_page(self):
        return reverse_lazy('logged_out')  # Перенаправление на другую страницу после выхода
