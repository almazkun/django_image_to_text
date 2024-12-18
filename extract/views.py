import base64
from django.views.generic.edit import FormView
from .forms import ImageTextExtractionForm


class ExtractView(FormView):
    template_name = "index.html"
    form_class = ImageTextExtractionForm
    success_url = "/"

    def form_valid(self, form):
        text = form.save()
        encoded_text = base64.b64encode(text.encode("utf-8")).decode("utf-8")
        response = super().form_valid(form)
        response.set_cookie(
            "extracted_text",
            encoded_text,
            max_age=3600,
            httponly=True,
            samesite="Lax",
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        encoded_text = self.request.COOKIES.get("extracted_text")
        if encoded_text:
            try:
                extracted_text = base64.b64decode(encoded_text.encode("utf-8")).decode(
                    "utf-8"
                )
            except (base64.binascii.Error, UnicodeDecodeError):
                extracted_text = None
        else:
            extracted_text = None

        context["extracted_data"] = extracted_text

        return context
