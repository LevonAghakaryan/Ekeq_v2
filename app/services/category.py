from app.repositories.category import CategoryRepository

class CategoryService:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    def get_all_categories(self):
        return self.repo.get_all()

    def get_full_menu(self):
        """Սա օգտակար է կատալոգի էջի համար, որտեղ պետք են և՛ կատեգորիաները, և՛ դիզայնները"""
        return self.repo.get_with_templates()