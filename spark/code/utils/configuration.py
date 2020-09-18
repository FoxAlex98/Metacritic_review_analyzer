import datetime

es_write_conf = {
"es.nodes" : "10.0.100.51",
"es.port" : "9200",
"es.resource" : '%s/%s' % ("metacritic","_doc"),
"es.input.json" : "yes"
}

enco = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime.datetime)
    or isinstance(obj, datetime.date)
    else None
)

mapping = {
    "mappings": {
        "properties": {
            "timestamp": {
                "type": "date"
            }
        }
    }
}