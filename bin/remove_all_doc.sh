curl -X POST "localhost:9200/metacritic/_delete_by_query?pretty" \
     -H 'Content-Type: application/json' \
     -d' {
            "query": {
                        "match_all": {}
                     }
         } '