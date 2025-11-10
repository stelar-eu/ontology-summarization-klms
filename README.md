# README Gilgamesh Summarization - Ontology Summarization

This is an easy to full workflow for creating key-value based summaries on input RDF ontologies using Gilgamesh Summarizer.
For more information on the tool visit: [gilgamesh-summarizer](https://github.com/KwtsPls/gilgamesh-summarizer)

## Input
**For all key attributes in JSON, exactly one file path must be provided.**

<table>
  <tr>
    <th>Attributes</th>
    <th>Info</th>
    <th>Value Type</th>
    <th>Required</th>
  </tr>
  <tr>
    <td><code>data_file</code></td>
    <td><code>Any valid RDF format</code> format</td>
    <td><code>list</code></td>
    <td>&#10004;</td>
  </tr>
  <tr>
    <td><code>ontology_file</code></td>
    <td><code>Any valid RDF format</code> format</td>
    <td><code>list</code></td>
    <td>&#10004;</td>
  </tr>
</table>

```
{
	"inputs": {
		"data_file": [
			"XXXXXXXX-bucket/temp1.csv"
		],
		"ontology_file": [
			"XXXXXXXX-bucket/intermediate.json"
		]
		
	}
}
```
1. data_file: The input knowledge graph data
2. ontology_fle: The input knowledge graph's RDF schema

## Parameters
Concering input, additional info must be provided.

<table>
  <tr>
    <th>Attributes</th>
    <th>Info</th>
    <th>Value Type</th>
    <th>Required</th>
  </tr>
  <tr>
	  <td><code>prune_topk_nodes</code></td>
	  <td>Remove nodes with most edges from clusters. Increasing it reduces execution time but reduces accuracy</td>
	  <td><a href="#dataset">dataset_object</a></td>
	  <td></td> 
  </tr>
  <tr>
	  <td><code>max_cluster_size</code></td>
	  <td>Set maximum cluster size. Increasing it reduces execution time but reduces accuracy</td>
	  <td><a href="#dataset">dataset_object</a></td>
	  <td></td> 
  </tr>
		
		
</table>

 An example of parameters for ontology summarization:
```
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
```


## Output
Output will be provide the file where the mappings generated from the ontology summarization process are stored, alongside some basic metrics like the number of key value pairs collected and the number of affected properties in the ontology. E.g

```
{
	'message': 'Tool Executed Succesfully',
	'outputs': {
		"mappings" : "/path/to/write/the/file.json"
	}, 
	'metrics': { 
		'numKVPairs': 3,
		'affectedPredicates' : 10 
	}, 
	'status': "success",
}
```
