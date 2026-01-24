from app.repositories.template import TemplateRepository

class TemplateService:
    def __init__(self, repo: TemplateRepository):
        self.repo = repo

    def get_full_catalog(self):
        """Ստանում է ամբողջ կատալոգը"""
        return self.repo.get_all()

    def get_template_details(self, template_id: int):
        """Ստանում է մեկ տեմպլեյթի տվյալները (օրինակ՝ product detail էջի համար)"""
        return self.repo.get_by_id(template_id)

    def get_templates_by_type(self, category_id: int):
        """Ստանում է տեմպլեյթներ միայն կոնկրետ կատեգորիայի համար (օր.՝ միայն հարսանիք)"""
        return self.repo.get_by_category(category_id)