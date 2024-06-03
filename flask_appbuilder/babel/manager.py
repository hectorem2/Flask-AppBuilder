import os

from flask import current_app, has_request_context, request, session
from flask_appbuilder.babel.views import LocaleView
from flask_appbuilder.basemanager import BaseManager
from flask_babel import Babel


class BabelManager(BaseManager):
    babel = None
    locale_view = None

    def __init__(self, appbuilder):
        super(BabelManager, self).__init__(appbuilder)
        current_app.config.setdefault("BABEL_DEFAULT_LOCALE", "en")
        if not current_app.config.get("LANGUAGES"):
            current_app.config["LANGUAGES"] = {"en": {"flag": "us", "name": "English"}}
        appbuilder_parent_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), os.pardir
        )
        appbuilder_translations_path = os.path.join(
            appbuilder_parent_dir, "translations"
        )
        if "BABEL_TRANSLATION_DIRECTORIES" in current_app.config:
            current_translation_directories = current_app.config.get(
                "BABEL_TRANSLATION_DIRECTORIES"
            )
            translations_path = (
                appbuilder_translations_path + ";" + current_translation_directories
            )
        else:
            translations_path = appbuilder_translations_path + ";translations"
        current_app.config["BABEL_TRANSLATION_DIRECTORIES"] = translations_path
        self.babel = Babel(current_app)
        self.babel.locale_selector_func = self.get_locale

    def register_views(self):
        self.locale_view = LocaleView()
        self.appbuilder.add_view_no_menu(self.locale_view)

    @property
    def babel_default_locale(self):
        return current_app.config["BABEL_DEFAULT_LOCALE"]

    @property
    def languages(self):
        return current_app.config["LANGUAGES"]

    def get_locale(self):
        if has_request_context():
            # locale selector for API searches for request args
            for arg, value in request.args.items():
                if arg == "_l_":
                    if value in self.languages:
                        return value
                    else:
                        return self.babel_default_locale
            locale = session.get("locale")
            if locale:
                return locale
            session["locale"] = self.babel_default_locale
            return session["locale"]
