from elasticsearch import Elasticsearch
from datetime import datetime
from elasticsearch import RequestsHttpConnection

# Configurando as credenciais de autenticação
http_auth = ('multipet', 'multipet@2022#$')

# Conectando ao Elasticsearch
es = Elasticsearch(
    ['http://167.114.191.57:9200'],
    http_auth=http_auth,
    connection_class=RequestsHttpConnection
)

# Buscando todos os documentos em 'meu-indice'
result = es.search(index="logstash-2023.04", query={"match_all": {}})

# Processando os resultados
print(result)




resp = es.search(index="logstash-2023.04", query={"match_all": {}})