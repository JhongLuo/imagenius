from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
import uuid


# Get AWS credentials
class OSearch():
    def __init__(self) -> None:
        host = 'search-ece1779t18a3-pn6k2juowrs5mx4lj2zd7rmgxi.us-east-1.es.amazonaws.com'
        region = 'us-east-1'
        credentials = boto3.Session().get_credentials()
        awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es', session_token=credentials.token)
        self.index = 'prompt'
        self.client = OpenSearch(
            hosts=[{'host': host, 'port': 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )

        if not self.client.indices.exists(index=self.index):
            mapping = {
                "mappings": {
                    "properties": {
                        "text": {
                            "type": "text"
                        }
                    }
                }
            }
            self.client.indices.create(index=self.index, body=mapping)
        
    def add_prompt(self, prompt):
        sentence_id = str(uuid.uuid4())
        self.client.index(
            index=self.index, 
            id=sentence_id,
            body={
                'text': prompt,
        })
        
    def search(self, search_term):
        res = self.client.search(index=self.index, body={
            'query': {
                'multi_match': {
                    "query": search_term,
                    "fuzziness": "AUTO",
                    "fields": ["text"],
                }
            }
        })
        return [obj['_source']['text'] for obj in res['hits']['hits']]
    
    def clear(self):
        self.client.indices.delete(index=self.index, ignore=[400, 404])