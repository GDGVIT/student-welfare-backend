from django.contrib import admin

# Custom Admin Site forDSW
class SWAdminSite(admin.AdminSite):
    site_header = "SW Admin"
    site_title = "SW Admin Portal"
    index_title = "Welcome to SW Admin Portal"

    def has_permission(self, request):
        return request.user.is_authenticated and (request.user.is_dsw or request.user.is_superuser)
    
sw_admin_site = SWAdminSite(name="dsw_admin")