from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Search, Q, Range
import json

def remover_campos_sem_prefixo(dicionario, prefixo1, prefixo2):
    campos_com_prefixo = {}
    for chave, valor in dicionario.items():
        if chave == "Alerta__ONN": continue
        if chave.startswith(prefixo1) or chave.startswith(prefixo2):
            if valor == 1:
                campos_com_prefixo[chave] = valor
        
    return campos_com_prefixo

hora_atual = datetime.now() + timedelta(minutes=180)
hora_anterior = hora_atual - timedelta(hours=1)
hora_atual_str = hora_atual.strftime("%Y-%m-%dT%H:%M:%S")
hora_anterior_str = hora_anterior.strftime("%Y-%m-%dT%H:%M:%S")

http_auth = ('multipet', 'multipet@2022#$')
es = Elasticsearch(['http://167.114.191.57:9200'], http_auth=http_auth)
search = Search(using=es, index="logstash-2023.05")

query = "icinga.service.keyword : c48381c1-d4b2-44bd-beb5-9d38cda7b829 AND (output.Fault__ONN :1 OR output.Alerta__ONN : 1)"

search = search.query(
    Q("bool", must=[
        Q("query_string", query=query),
        Q("range", **{"@timestamp":{"gte": "2023-05-31T23:19:00",
                                    "lte": "2023-05-31T23:20:00"}})
    ])
)
search = search.extra(size=1)

result = search.execute()

final_json = dict()

print(len(result.hits))
# Processar o resultado
for hit in result.hits:
    documento_dict = hit.to_dict()
    print(documento_dict)
    output_dict = remover_campos_sem_prefixo(documento_dict["output"], "Alerta", "Fault")
    if len(output_dict) < 2: continue

    data_datetime = datetime.strptime(documento_dict["@timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
    out_timestamp = (data_datetime - timedelta(minutes=180)).strftime("%Y-%m-%dT%H:%M:%S")

    final_json[out_timestamp] = output_dict
    # print(documento_dict["@timestamp"])
    # print(documento_dict["output"])
    

    

print(json.dumps(final_json))
