# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views

from .company import company_views
from .admin import admin_views
from .alumni import alumni_views


views = [user_views, index_views, auth_views, company_views, admin_views, alumni_views ] 
# blueprints must be added to this list