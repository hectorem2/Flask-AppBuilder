from flask import Flask

from .views import ContactModelView, GroupModelView
from .extensions import appbuilder


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")
    with app.app_context():
        appbuilder.init_app(app)
        appbuilder.add_view(
            GroupModelView,
            "List Groups",
            icon="fa-folder-open-o",
            category="Contacts",
            category_icon="fa-envelope",
        )
        appbuilder.add_separator("Contacts")
        appbuilder.add_view(
            ContactModelView, "List Contacts", icon="fa-envelope", category="Contacts"
        )
        return app