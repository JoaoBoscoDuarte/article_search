import requests

class CrossrefSearcher:
    # Inicializa o buscador com a URL da API
    def __init__(self):
        self.api_url = 'https://api.crossref.org/works'
    
    # Busca artigos por termo específico
    def search_by_term(self, term, rows=10):
        params = {
            'query': term,
            'rows': rows,
            'filter': 'type:journal-article'
        }
        
        try:
            response = requests.get(self.api_url, params=params)

            if response.status_code == 200:
                return response.json()
            
            else:
                print(f"Erro {response.status_code}: {response.text}")
                return {}
            
        except Exception as e:
            print(f"Erro na requisição: {e}")
            return {}
    
    # Extrai informações dos artigos do JSON retornado
    def extract_articles(self, json_data):
        articles = []
        
        if 'message' in json_data and 'items' in json_data['message']:
            for item in json_data['message']['items']:
                article = {
                    'titulo': item.get('title', [''])[0],
                    'doi': item.get('DOI'),
                    'ano': self._get_year(item),
                    'url': item.get('URL'),
                    'autores': self._get_authors(item)
                }
                articles.append(article)
        
        return articles
    
    # Extrai ano de publicação do artigo
    def _get_year(self, item):
        if 'published-print' in item:
            return item['published-print'].get('date-parts', [[None]])[0][0]
        
        elif 'published-online' in item:
            return item['published-online'].get('date-parts', [[None]])[0][0]
        
        return None
    
    # Extrai lista de autores do artigo
    def _get_authors(self, item):
        authors = []

        if 'author' in item:
            for author in item['author']:

                name = f"{author.get('given', '')} {author.get('family', '')}".strip()
                if name:
                    authors.append(name)

        return authors

# Termo específico para busca
terms = "biopsychosocial assessment technology"

# Execução da busca
searcher = CrossrefSearcher()
print(f"Buscando por: {terms}")

result = searcher.search_by_term(terms)
articles = searcher.extract_articles(result)

print(f"\nEncontrados: {len(articles)} artigos")

# Mostra primeiros 3 resultados
for i, article in enumerate(articles[:3], 1):
    print(f"\n{i}. {article['titulo']}")
    print(f"   Ano: {article['ano']}")
    print(f"   DOI: {article['doi']}")
    print(f"   Autores: {', '.join(article['autores'][:2])}")