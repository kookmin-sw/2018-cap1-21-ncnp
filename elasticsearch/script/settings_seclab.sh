#curl -XPUT http://203.246.112.133:9200/seclab?pretty

#curl -XPOST http://203.246.112.133:9200/seclab/_close?pretty

curl -XPUT -H "Content-Type: application/json" "http://203.246.112.133:9200/seclab?pretty" -d '
{
	"settings": {
		"analysis" : {
			"analyzer":{
				"ssdeep_analyzer": {
					"tokenizer" : "ssdeep_ngram_tokenizer"
				}
			},
			"tokenizer":{
				"ssdeep_ngram_tokenizer": {
					"type" : "ngram",
					"min_gram" : "6",
					"max_gram" : "6"	
				}
			}
		}
	},
	"mappings" : {
		"analyzed_report" :{
			"properties":{
				"SSDeep_chunk":{
					"type" : "text",
					"analyzer" : "ssdeep_analyzer"
				},
				"SSDeep_double_chunk":{
					"type" : "text",
					"analyzer" : "ssdeep_analyzer"
				},
				"SSDeep_chunk_size" :{
					"type" : "integer"
				},
				"Uploaded_Date" : {
					"type" : "date"
				}
			}
		}
	}
}'