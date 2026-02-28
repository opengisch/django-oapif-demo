from django.apps import AppConfig


class OapifDemoConfig(AppConfig):
    name = "oapif_demo"
    verbose_name = "Oapif Demo"

    def ready(self):
        from .qgis import generate_qgs_project

        generate_qgs_project()
