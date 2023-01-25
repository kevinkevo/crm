from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
# helps in checking if the user is organisor after logging in
class OrganisorAndLoginRequiredMixin(AccessMixin):
	"""Verify that the current user is authenticated and is an organisor."""
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated or not request.user.is_organisor:
			return redirect("/land-page")
		return super().dispatch(request, *args, **kwargs)