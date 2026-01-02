import secrets

from django.utils import timezone
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import WaitlistApplication
from .forms import WaitlistForm


def main_page_view(request):
    subject = None
    message = None
    error = None

    if request.method == "POST":
        form = WaitlistForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            application, created = WaitlistApplication.objects.get_or_create(
                email=email,
                defaults={"confirmation_token":  secrets.token_urlsafe(16)},
            )

            if created:
                confirmation_link = request.build_absolute_uri(
                    f"/accounts/confirm-email/{application.confirmation_token}/")

                send_mail(
                    subject="Book DNA: Confirm your application.",
                    message=(
                        "Hello fellow bookworm,\n\n"
                        "To confirm your email address for the Book DNA beta, please click here:\n\n"
                        f"{confirmation_link}\n\n"
                        "Thanks,\nBen"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )

                message = ("Please click the link in the confirmation email to confirm your application to the beta.\n"
                           "We will be in touch soon!")
            else:
                subject = "You're on the list!"
                message = (
                    "We will be in touch one it is ready for testing\n"
                    "Ben"
                )
    else:
        form = WaitlistForm()

    return render(
        request,
        "waitlist/landing.html",
        context={
            "subject": subject,
            "message": message,
            "error": error,
            "form": form
        }
    )


def confirm_email_view(request, token):
    subject = None
    message = None
    error = None

    try:
        application = get_object_or_404(
            WaitlistApplication,
            confirmation_token=token
        )
        if not application.is_confirmed:
            application.is_confirmed = True
            application.confirmed_at = timezone.now()
            application.save()
            message = "Your email has been confirmed. Thank you!"
        else:
            subject = "You're on the list!"
            message = (
                "We will be in touch once it is ready for testing,"
                "\n\nBen"
            )
    except WaitlistApplication.DoesNotExist:
        error = "Invalid confirmation token."
        return render(request, "waitlist/confirm_email.html", context={"message": message, "error": error})

    return render(
        request,
        "waitlist/confirm_email.html",
        context={
            "subject": subject,
            "message": message,
            "error": error
        }
    )
