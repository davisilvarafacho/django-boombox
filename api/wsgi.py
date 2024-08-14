import os
import dotenv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

dotenv.load_dotenv('.env')
dotenv.load_dotenv('.env.prod')

application = get_wsgi_application()
