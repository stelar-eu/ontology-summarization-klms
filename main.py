import json
import sys
import traceback
from utils.mclient import MinioClient
#gilgamesh libs
from gilgamesh_summarizer.KnowledgeGraph import KnowledgeGraph
from gilgamesh_summarizer.Summarizer import Summarizer

# Here you may define the imports your tool needs...
# import pandas as pd
# import numpy as np
# ...

def run(json):

    """
        This is the core method that initiates tool .py files execution. 
        It can be as large and complex as the tools needs. In this file you may import, call,
        and define any lib, method, variable or function you need for you tool execution.
        Any specific files you need can be in the same directory with this main.py or in subdirs
        with appropriate import statements with respect to dir structure.

        Any logic you implement here is going to be copied inside your tool image when 
        you build it using docker build or the provided Makefile.
        
            The MinIO initialization that is given down below is an example you may use it or not.
            MinIO access credentials are in the form of <ACCESS ID, ACCESS KEY, SESSION TOKEN>
            and are generated upon the OAuth 2.0 token of the user executing the tool. 

            For development purpose you may define your own credentials for your local MinIO 
            instance by commenting the MinIO init part.

    """

    try:
        """
        Init a MinIO Client using the custom STELAR MinIO util file.

        We access the MinIO credentials from the JSON field named 'minio' which 
        was acquired along the tool parameters.

        This credentials can be used for tool specific access too wherever needed
        inside this main.py file.

        """
        ################################## MINIO INIT #################################
        minio_id = json['minio']['id']
        minio_key = json['minio']['key']
        minio_skey = json['minio']['skey']
        minio_endpoint = json['minio']['endpoint_url']
        
        mc = MinioClient(minio_endpoint, minio_id, minio_key, secure=True, session_token=minio_skey)

        # It is strongly suggested to use the get_object and put_object methods of the MinioClient
        # as they handle input paths provided by STELAR API appropriately. (S3 like paths)
        ###############################################################################


        """
        Acquire tool specific parameters from json['parameters] which was given by the 
        KLMS Data API during the creation of the Tool Execution Task.

        An example of parameters for ontology summarization
        {
            "inputs": {
                "data_file": [
                    "XXXXXXXX-bucket/temp1.csv"
                ],
                "ontology_file": [
                    "XXXXXXXX-bucket/intermediate.json"
                ]
                
            },
            "outputs": {
                "mappings_file": "/path/to/write/the/file.json",
            },
            "parameters": {
                "prune_topk_nodes": 100,
                "max_cluster_size": 500,
            }
        }
        """
        graph_file = json["inputs"]['data_file'][0]
        ontology_file = json["inputs"]['ontology_file'][0]
        mappings_file = json["outputs"]["mappings_file"]

        # Download files from MinIO
        mc.get_object(s3_path=graph_file, local_path='data_file.csv')
        graph_file = 'data_file.csv'
        mc.get_object(s3_path=ontology_file, local_path='ontology.json')
        ontology_file = 'ontology.json'

        prune_topk_nodes = json.get('parameters', {}).get('prune_topk_nodes')
        max_cluster_size = json.get('parameters', {}).get('max_cluster_size')
        #default values
        if prune_topk_nodes is None:
            prune_topk_nodes = 6
        if max_cluster_size is None:
            max_cluster_size = 500

        ##### Tool Logic #####
        kg = KnowledgeGraph(graph_file, ontology_file)

        clusters, triples_dict = kg.create_clusters(prune_top_nodes=prune_topk_nodes,max_cluster_size=max_cluster_size)

        classifier = Summarizer(kg)
        classifier.tokenizer.model_max_length = classifier.model.config.max_position_embeddings

        results = classifier.classify_clusters(clusters, triples_dict)

        predicates, mappings = classifier.remove_classes_and_collect_range_predicates(results)

        # Write to a JSON file
        with open('mappings.json', "w") as f:
            json.dump(mappings, f, indent=4)

        #   Upload the results file to MinIO
        mc.put_object(s3_path=mappings_file, file_path='mappings.json')

        out_json= {
                'message': 'Tool Executed Succesfully',
                'outputs': {
                    "mappings" : mappings_file
                }, 
                'metrics': { 
                    'numKVPairs': len(results),
                    'affectedPredicates' : len(predicates) 
                }, 
                'status': "success",
              }

        return out_json
    except Exception as e:
        print(traceback.format_exc())
        return {
            'message': 'An error occurred during data processing.',
            'error': traceback.format_exc(),
            'status': 500
        }
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError("Please provide 2 files.")
    with open(sys.argv[1]) as o:
        j = json.load(o)
    response = run(j)
    with open(sys.argv[2], 'w') as o:
        o.write(json.dumps(response, indent=4))
