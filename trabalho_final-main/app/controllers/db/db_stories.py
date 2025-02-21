from app.models.stories import Stories
import json

class DataStory():
    """"Banco de Dados para as historias"""
    def __init__(self):
        self.data_stories = self.load_data_stories()

    def load_data_stories(self):
        try:
            with open("app/static/js/data_stories,json") as arquivo_json:
                story_data = json.load(arquivo_json)
            return [Stories(**data) for data in story_data]        
        except FileNotFoundError:
            return[Stories('Não Encontrado', 'Não Encontrado', 'Não encontrado')]
    
    def get_data_stories(self, parameter):
        """Obtém o livro/história com base no parâmetro (como um índice)"""
        try:
            #usando um loop para percorrer a lista e encontrar o item
            for index, stories in enumerate(self.data_stories):
                if index == int(parameter):
                    return stories
        except ValueError:
            return None #se o parâmtro não for um valo válido
        return None #se o índice não for achado
