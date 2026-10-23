from django.contrib import messages
from django.db.models import F
from django.http import Http404
from django.urls import reverse_lazy
from django.views import generic

from .forms import ContactForm
from .models import Blog, Certificate, Portfolio, Testimonial, UserProfile
from .services import (
    CONTACT_SERVICE_CHOICES,
    DEFAULT_PROCESS,
    SERVICE_GROUPS,
    get_priority_services,
    get_service,
)


def _project_ordering(queryset):
    return queryset.order_by(F("date").desc(nulls_last=True), "-id")


class IndexView(generic.TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        portfolio = _project_ordering(Portfolio.objects.filter(is_active=True))
        testimonials = Testimonial.objects.filter(is_active=True)
        certificates = Certificate.objects.filter(is_active=True).order_by(
            F("date").desc(nulls_last=True), "name"
        )
        blogs = Blog.objects.filter(is_active=True).order_by("-timestamp")
        profile = (
            UserProfile.objects.select_related("user")
            .prefetch_related("skills")
            .first()
        )
        skills = profile.skills.all() if profile else []
        key_skills = [skill for skill in skills if skill.is_key_skill]

        featured_portfolio = list(portfolio.filter(is_featured=True)[:3])
        if len(featured_portfolio) < 3:
            featured_ids = {project.pk for project in featured_portfolio}
            featured_portfolio.extend(
                [
                    project
                    for project in portfolio
                    if project.pk not in featured_ids
                ][: 3 - len(featured_portfolio)]
            )

        context.update(
            {
                "portfolio": portfolio,
                "featured_portfolio": featured_portfolio,
                "testimonials": testimonials,
                "certificates": certificates,
                "blogs": blogs[:3],
                "profile": profile,
                "skills": skills,
                "key_skills": key_skills,
                "project_count": portfolio.count(),
                "skill_count": len(skills),
                "certificate_count": certificates.count(),
                "article_count": blogs.count(),
                "priority_services": get_priority_services(),
            }
        )
        return context


class ServicesView(generic.TemplateView):
    template_name = "main/services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "service_groups": SERVICE_GROUPS,
                "priority_services": get_priority_services(),
                "process_steps": DEFAULT_PROCESS,
            }
        )
        return context


class ServiceDetailView(generic.TemplateView):
    template_name = "main/service-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = get_service(self.kwargs["slug"])
        if not service:
            raise Http404("Service not found")

        projects = Portfolio.objects.filter(
            is_active=True, slug__in=service.get("related_projects", [])
        )
        project_map = {project.slug: project for project in projects}
        related_projects = [
            project_map[slug]
            for slug in service.get("related_projects", [])
            if slug in project_map
        ]

        context.update(
            {
                "service": service,
                "process_steps": DEFAULT_PROCESS,
                "related_projects": related_projects,
                "other_services": [
                    item
                    for item in get_priority_services()
                    if item["slug"] != service["slug"]
                ],
            }
        )
        return context


class ContactView(generic.FormView):
    template_name = "main/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("main:home")

    def get_initial(self):
        initial = super().get_initial()
        requested_service = self.request.GET.get("service", "")
        if requested_service in dict(CONTACT_SERVICE_CHOICES):
            initial["service"] = requested_service
        return initial

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "Thank you. Your inquiry has been received and I will be in touch soon.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Please check the highlighted fields and try again.",
        )
        return super().form_invalid(form)


class PortfolioView(generic.ListView):
    model = Portfolio
    template_name = "main/portfolio.html"
    paginate_by = 9

    def get_queryset(self):
        return _project_ordering(Portfolio.objects.filter(is_active=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        technologies = {
            technology
            for project in Portfolio.objects.filter(is_active=True)
            for technology in project.technology_list
        }
        context["technologies"] = sorted(technologies, key=str.lower)
        return context


class PortfolioDetailView(generic.DetailView):
    model = Portfolio
    template_name = "main/portfolio-detail.html"

    def get_queryset(self):
        return Portfolio.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_projects"] = _project_ordering(
            Portfolio.objects.filter(is_active=True).exclude(pk=self.object.pk)
        )[:3]
        return context


class BlogView(generic.ListView):
    model = Blog
    template_name = "main/blog.html"
    paginate_by = 9

    def get_queryset(self):
        return Blog.objects.filter(is_active=True).order_by("-timestamp")


class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = "main/blog-detail.html"

    def get_queryset(self):
        return Blog.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_posts"] = (
            Blog.objects.filter(is_active=True)
            .exclude(pk=self.object.pk)
            .order_by("-timestamp")[:2]
        )
        return context
