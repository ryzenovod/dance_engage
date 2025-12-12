from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST

from collections import defaultdict
import random

from .forms import ProfileForm, CustomLoginForm, CustomUserCreationForm
from .models import UserProfile, Dance, Engagement  # Убедитесь, что UserProfile импортирован
from .dance_data import LEVEL_ORDER
from .dance_loader import ensure_dances_seeded


def group_dances_by_level(dances):
    buckets = defaultdict(list)
    for dance in dances:
        buckets[dance.level].append(dance)

    ordered_groups = [(level, buckets[level]) for level in LEVEL_ORDER if buckets[level]]
    leftovers = [(level, group) for level, group in buckets.items() if level not in LEVEL_ORDER]

    return ordered_groups + leftovers

@login_required
@require_POST
def confirm_engagement(request, engagement_id):
    engagement = get_object_or_404(
        Engagement,
        id=engagement_id,
        partner=request.user.userprofile,  # Используем UserProfile
        status='pending'
    )
    engagement.status = 'confirmed'
    engagement.save()
    messages.success(request, "Вы подтвердили ангажирование!")
    return redirect(f'{reverse("engagement_list")}?random={random.randint(1, 1000)}')

def home(request):
    profile = request.user.userprofile if request.user.is_authenticated else None
    dance_filter = request.GET.get('dance')
    status_filter = request.GET.get('status')

    engagements = (
        profile.engagements.select_related('partner__user', 'dance')
        if profile else Engagement.objects.none()
    )

    if dance_filter:
        engagements = engagements.filter(dance__id=dance_filter)
    if status_filter in dict(Engagement.STATUS_CHOICES):
        engagements = engagements.filter(status=status_filter)

    all_dances = ensure_dances_seeded().order_by('name')

    engagement_stats = {
        'total': engagements.count(),
        'confirmed': engagements.filter(status='confirmed').count(),
        'pending': engagements.filter(status='pending').count(),
    }

    skills_count = profile.skills.count() if profile else 0

    register_form = None if request.user.is_authenticated else CustomUserCreationForm()

    return render(request, 'engage/home.html', {
        'profile': profile,
        'engagements': engagements,
        'all_dances': all_dances,
        'status_choices': Engagement.STATUS_CHOICES,
        'engagement_stats': engagement_stats,
        'register_form': register_form,
        'skills_count': skills_count,
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматически логиним
            messages.success(request, "Регистрация прошла успешно! Добро пожаловать на бал.")
            return redirect('home')
        else:
            messages.error(request, "Не удалось сохранить форму. Проверьте подсказки рядом с полями.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'engage/register.html', {'form': form})

class MyLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'login.html'

@login_required
def select_skills(request):
    profile = request.user.userprofile
    dances = ensure_dances_seeded().order_by('name')
    dances_by_level = group_dances_by_level(dances)

    if request.method == "POST":
        selected_ids = []
        for raw_id in request.POST.getlist('dances'):
            try:
                selected_ids.append(int(raw_id))
            except (TypeError, ValueError):
                continue

        profile.skills.set(selected_ids)
        return redirect('home')

    return render(request, 'engage/skills.html', {
        'dances_by_level': dances_by_level,
        'selected_dances': profile.skills.all()
    })

@login_required
def edit_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Сохраняем навыки, даже если роль изменилась
            form.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'engage/edit_profile.html', {'form': form})

@login_required
def select_engagements(request):
    profile = request.user.userprofile
    dances = ensure_dances_seeded().order_by('name')
    dances_by_level = group_dances_by_level(dances)

    if request.method == "POST":
        selected_dance_ids = request.POST.getlist('dances')

        # Удаляем только ангажирования текущего пользователя
        Engagement.objects.filter(dancer=profile).delete()

        # Создаем новые ангажирования
        for dance_id in selected_dance_ids:
            dance = Dance.objects.get(id=dance_id)
            Engagement.objects.create(
                dancer=profile,
                partner=profile,  # Замените на реального партнёра при необходимости
                dance=dance,
                status='pending'
            )

        return redirect('home')

    return render(request, 'engage/skills.html', {
        'dances_by_level': dances_by_level,
        'selected_dances': [e.dance for e in profile.engagements.all()],
        'title': 'Какие танцы вы хотите танцевать на балу?'
    })

@login_required
def dance_list(request):
    dances = ensure_dances_seeded().order_by('name')
    dances_by_level = group_dances_by_level(dances)
    return render(request, 'engage/dance_list.html', {'dances_by_level': dances_by_level})

@login_required
@require_POST
def engage(request, partner_id, dance_id):
    # Используем UserProfile напрямую
    partner_profile = get_object_or_404(UserProfile, id=partner_id)
    dance = get_object_or_404(Dance, id=dance_id)
    current_profile = request.user.userprofile  # Текущий пользователь как UserProfile

    if partner_profile == current_profile:
        messages.warning(request, "Нельзя ангажировать самого себя.")
        return redirect('partner_list', dance_id=dance.id)

    # Проверка существующего ангажирования
    if not Engagement.objects.filter(dancer=current_profile, dance=dance).exists():
        Engagement.objects.create(
            dancer=current_profile,
            partner=partner_profile,
            dance=dance,
            status='pending'
        )
        messages.success(request, "Приглашение отправлено!")
    else:
        messages.info(request, "У вас уже есть приглашение для этого танца.")
    return redirect('engagement_list')

@login_required
def engagement_list(request):
    profile = request.user.userprofile  # Получаем UserProfile текущего пользователя

    my_engagements = Engagement.objects.filter(dancer=profile)
    incoming_requests = Engagement.objects.filter(partner=profile, status='pending')

    # Фильтрация по танцу и статусу (оставьте без изменений)
    dance_filter = request.GET.get('dance')
    status_filter = request.GET.get('status')

    if dance_filter:
        my_engagements = my_engagements.filter(dance__id=dance_filter)
        incoming_requests = incoming_requests.filter(dance__id=dance_filter)

    if status_filter:
        my_engagements = my_engagements.filter(status=status_filter)

    all_dances = ensure_dances_seeded().order_by('name')

    return render(request, 'engage/engagement_list.html', {
        'my_engagements': my_engagements,
        'incoming_requests': incoming_requests,
        'all_dances': all_dances,
        'selected_dance': dance_filter,
        'selected_status': status_filter,
    })

# Пример для decline_engagement
@login_required
@require_POST
def decline_engagement(request, engagement_id):
    engagement = get_object_or_404(
        Engagement,
        id=engagement_id,
        partner=request.user.userprofile,  # Используем UserProfile
        status='pending'
    )
    engagement.delete()
    return redirect('engagement_list')


@login_required
def partner_list(request, dance_id):
    dance = get_object_or_404(Dance, id=dance_id)
    profile = request.user.userprofile

    # Используем userprofile вместо User
    possible_partners = UserProfile.objects.filter(skills=dance).exclude(user=request.user)

    # Фильтрация по роли
    if profile.role == 'Дама':
        possible_partners = possible_partners.filter(role='Кавалер')
    elif profile.role == 'Кавалер':
        possible_partners = possible_partners.filter(role='Дама')

    # Исправленный запрос
    sent_engagements = Engagement.objects.filter(
        dancer=profile,
        dance=dance
    ).values_list('partner__user__id', flat=True)

    possible_partners = possible_partners.exclude(user__id__in=sent_engagements)

    return render(request, 'engage/partner_list.html', {
        'dance': dance,
        'partners': possible_partners
    })
