from django.templatetags.static import static
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('Дама', 'Дама'), ('Кавалер', 'Кавалер')])
    skills = models.ManyToManyField('Dance', blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='')

    def __str__(self):
        return self.user.username

    @property
    def avatar_url(self):
        """Безопасно возвращает URL аватара или дефолтную заглушку."""
        try:
            if self.avatar and hasattr(self.avatar, 'url'):
                return self.avatar.url
        except ValueError:
            # Файл был удалён или путь некорректный
            pass
        return static('engage/avatar-placeholder.svg')


class Dance(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    has_partner = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Engagement(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('confirmed', 'Подтверждено'),
        ('declined', 'Отклонено'),
    ]
    dancer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='engagements')
    partner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_engagements')
    dance = models.ForeignKey(Dance, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('dancer', 'dance')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.dancer.user.username} ↔ {self.partner.user.username} ({self.dance.name}) [{self.get_status_display()}]"

    @property
    def status_badge_class(self):
        status_to_bootstrap = {
            'pending': 'warning text-dark',
            'confirmed': 'success',
            'declined': 'secondary',
        }
        return status_to_bootstrap.get(self.status, 'secondary')
