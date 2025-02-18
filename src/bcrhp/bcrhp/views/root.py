from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import ensure_csrf_cookie

from arches.app.views.base import BaseManagerView


class BcrhpRootView(BaseManagerView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(main_script="views/root")
        context["page_title"] = _("BCRHP Self Service")
        return render(request, "bcrhp/root.htm", context)
