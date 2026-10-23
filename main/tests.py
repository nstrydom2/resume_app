import time
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core import signing
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import CONTACT_TOKEN_SALT
from .models import (
    Blog,
    Certificate,
    ContactProfile,
    Portfolio,
    Skill,
    Testimonial,
    UserProfile,
)
from .services import PRIORITY_SERVICE_SLUGS


def contact_token(age_seconds=5):
    created = time.time() - age_seconds
    with patch("django.core.signing.time.time", return_value=created):
        return signing.dumps(
            {"created": created}, salt=CONTACT_TOKEN_SALT
        )


def contact_payload(**overrides):
    payload = {
        "name": "Jamie",
        "email": "Jamie@Example.com",
        "business_name": "Jamie's Bakery",
        "service": "spreadsheet-data",
        "message": "I would like to talk about cleaning a monthly export.",
        "current_process": "Exports are cleaned by hand in Excel.",
        "volume_frequency": "Four files a month.",
        "desired_deadline": "End of next month.",
        "budget_range": "automation-project",
        "preferred_contact": "email",
        "company_website": "",
        "form_token": contact_token(),
    }
    payload.update(overrides)
    return payload


class PortfolioTests(TestCase):
    def test_slug_and_absolute_url(self):
        project = Portfolio.objects.create(name="My Cool Project", is_active=True)

        self.assertEqual(project.slug, "my-cool-project")
        self.assertEqual(project.get_absolute_url(), "/portfolio/my-cool-project/")
        self.assertEqual(
            reverse("main:portfolio", kwargs={"slug": project.slug}),
            "/portfolio/my-cool-project/",
        )

    def test_duplicate_names_get_unique_slugs(self):
        first = Portfolio.objects.create(name="Same Name")
        second = Portfolio.objects.create(name="Same Name")

        self.assertNotEqual(first.slug, second.slug)
        self.assertEqual(second.slug, "same-name-2")

    def test_technology_list_is_parsed(self):
        project = Portfolio.objects.create(
            name="Stacked",
            technologies="Django, PostgreSQL, HTMX",
        )

        self.assertEqual(
            project.technology_list, ["Django", "PostgreSQL", "HTMX"]
        )

    def test_list_only_shows_active_projects(self):
        visible = Portfolio.objects.create(name="Visible", is_active=True)
        Portfolio.objects.create(name="Hidden", is_active=False)

        response = self.client.get(reverse("main:portfolios"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, visible.name)
        self.assertNotContains(response, "Hidden")

    def test_list_renders_without_an_image(self):
        Portfolio.objects.create(name="No Image", is_active=True)

        response = self.client.get(reverse("main:portfolios"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "project-placeholder")

    def test_detail_renders_without_an_image(self):
        project = Portfolio.objects.create(
            name="No Image Detail",
            description="A project without a cover image.",
            is_active=True,
        )

        response = self.client.get(project.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A project without a cover image.")

    def test_inactive_project_detail_returns_404(self):
        project = Portfolio.objects.create(name="Archived", is_active=False)

        response = self.client.get(project.get_absolute_url())

        self.assertEqual(response.status_code, 404)

    def test_projects_alias_redirects_to_portfolio(self):
        response = self.client.get("/projects/")

        self.assertRedirects(response, reverse("main:portfolios"), status_code=301)


class BlogTests(TestCase):
    def test_slug_and_absolute_url(self):
        post = Blog.objects.create(name="A Journal Post", is_active=True)

        self.assertEqual(post.slug, "a-journal-post")
        self.assertEqual(post.get_absolute_url(), "/blog/a-journal-post/")

    def test_list_renders_without_an_image(self):
        post = Blog.objects.create(name="No Image Post", is_active=True)

        response = self.client.get(reverse("main:blogs"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.name)
        self.assertContains(response, "post-placeholder")

    def test_inactive_post_detail_returns_404(self):
        post = Blog.objects.create(name="Draft", is_active=False)

        response = self.client.get(post.get_absolute_url())

        self.assertEqual(response.status_code, 404)


class PageTests(TestCase):
    def test_home_renders_without_projects(self):
        Portfolio.objects.all().delete()

        response = self.client.get(reverse("main:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Projects are being updated")

    def test_home_shows_priority_services_without_skill_percentages(self):
        response = self.client.get(reverse("main:home"))

        self.assertEqual(response.status_code, 200)
        for slug in PRIORITY_SERVICE_SLUGS:
            self.assertContains(response, f"/services/{slug}/")
        self.assertContains(response, "Explore services")
        self.assertNotContains(response, "Working proficiency")

    def test_home_renders_with_content(self):
        user = User.objects.create_user(
            username="nick",
            password="password",
            first_name="Nick",
            last_name="Strydom",
            email="nick@example.com",
        )
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.title = "Full Stack Developer"
        profile.bio = "I build things for the web."
        profile.save()

        python = Skill.objects.create(name="Python", score=92)
        django = Skill.objects.create(name="Django", score=90, is_key_skill=True)
        profile.skills.add(python, django)

        Portfolio.objects.create(
            name="Featured Build",
            description="A featured full stack application.",
            date=timezone.now(),
            technologies="Django, PostgreSQL",
            live_url="https://example.com",
            repository_url="https://github.com/example/repo",
            is_featured=True,
            is_active=True,
        )
        Certificate.objects.create(
            name="Example Academy",
            title="Advanced Django",
            date=timezone.now(),
            is_active=True,
        )
        Testimonial.objects.create(
            name="Alex Doe",
            role="Product Lead",
            quote="Great to work with.",
            is_active=True,
        )
        Blog.objects.create(
            name="First Post",
            description="A short article.",
            author="Nick",
            is_active=True,
        )

        response = self.client.get(reverse("main:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Featured Build")
        self.assertContains(response, "Advanced Django")
        self.assertContains(response, "Alex Doe")
        self.assertContains(response, "First Post")
        self.assertContains(response, "Python")

    def test_contact_page_renders_qualified_inquiry_form(self):
        response = self.client.get(reverse("main:contact"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tell me what is slowing you down.")
        self.assertContains(response, "What do you need help with?")
        self.assertContains(response, "Current process or tools")
        self.assertContains(response, "Budget range")
        self.assertContains(response, "form_token")

    def test_contact_form_preselects_requested_service(self):
        response = self.client.get(
            reverse("main:contact"), {"service": "pdf-extraction"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="pdf-extraction" selected')

    def test_contact_form_saves_qualification_data(self):
        response = self.client.post(
            reverse("main:contact"), contact_payload(), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactProfile.objects.count(), 1)
        inquiry = ContactProfile.objects.get()
        self.assertEqual(inquiry.email, "jamie@example.com")
        self.assertEqual(inquiry.service, "spreadsheet-data")
        self.assertEqual(inquiry.business_name, "Jamie's Bakery")
        self.assertEqual(inquiry.budget_range, "automation-project")
        self.assertContains(
            response, "Your inquiry has been received and I will be in touch soon."
        )

    def test_contact_form_rejects_honeypot_submission(self):
        response = self.client.post(
            reverse("main:contact"),
            contact_payload(company_website="https://spam.example"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactProfile.objects.count(), 0)
        self.assertContains(response, "Please check the highlighted fields")

    def test_contact_form_rejects_submission_that_is_too_fast(self):
        response = self.client.post(
            reverse("main:contact"),
            contact_payload(form_token=contact_token(age_seconds=0)),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactProfile.objects.count(), 0)
        self.assertContains(response, "Please take a moment")

    def test_contact_form_rejects_expired_token(self):
        response = self.client.post(
            reverse("main:contact"),
            contact_payload(form_token=contact_token(age_seconds=60 * 60 * 3)),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactProfile.objects.count(), 0)
        self.assertContains(response, "This form has expired")

    def test_demo_project_is_labelled(self):
        response = self.client.get(
            reverse("main:portfolio", kwargs={"slug": "csv-cleanup-utility"})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Demonstration project")
        self.assertContains(response, "not client work")

    def test_portfolio_detail_shows_actions_and_stack(self):
        project = Portfolio.objects.create(
            name="Linked Project",
            description="A project with links.",
            technologies="Django, HTMX",
            live_url="https://example.com",
            repository_url="https://github.com/example/project",
            is_active=True,
        )

        response = self.client.get(project.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "https://example.com")
        self.assertContains(response, "https://github.com/example/project")
        self.assertContains(response, "HTMX")

    def test_blog_detail_renders(self):
        post = Blog.objects.create(
            name="Detail Post",
            description="A detailed article.",
            body="<p>Article body.</p>",
            author="Nick",
            is_active=True,
        )

        response = self.client.get(post.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Detail Post")
        self.assertContains(response, "Article body.")


class ServiceTests(TestCase):
    def test_service_catalog_renders(self):
        response = self.client.get(reverse("main:services"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Practical software for the work")
        self.assertContains(response, "Full catalog")
        self.assertContains(response, "Scope and limits")
        for slug in PRIORITY_SERVICE_SLUGS:
            self.assertContains(response, f"/services/{slug}/")

    def test_each_priority_service_page_renders(self):
        for slug in PRIORITY_SERVICE_SLUGS:
            with self.subTest(slug=slug):
                response = self.client.get(
                    reverse("main:service", kwargs={"slug": slug})
                )

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "The problem")
                self.assertContains(response, "What you receive")
                self.assertContains(response, "Scope and limits")
                self.assertContains(response, "Request a quote")

    def test_unknown_service_returns_404(self):
        response = self.client.get(
            reverse("main:service", kwargs={"slug": "not-a-service"})
        )

        self.assertEqual(response.status_code, 404)
