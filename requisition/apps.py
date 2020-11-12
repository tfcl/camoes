from django.apps import AppConfig


class RequisitionConfig(AppConfig):
    name = 'requisition'
    def ready(self):
        import requisition.signals