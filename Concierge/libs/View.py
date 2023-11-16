from django.apps import apps


class View:
    @staticmethod
    def register():
        ...
        
    @staticmethod
    def getContext(context):
        main = {
            "currentUser": apps.get_app_config("ConciergeApp").currentUser
        }
        main.update(context)
        return main