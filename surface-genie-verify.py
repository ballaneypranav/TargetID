from pprint import pprint
import yaml
import requests

def get_uniprot_data(entry):
    base_url = "https://www.uniprot.org/uniprot/"
    response = requests.get(base_url + entry + ".txt")
    return response.text

def get_UniProt_ID(swissprot_ids):
    if not isinstance(swissprot_ids, list):
        swissprot_ids = [swissprot_ids]
    files = {
        'from': (None, 'UniProtKB_AC-ID'),
        'to': (None, 'UniProtKB-Swiss-Prot'),
        'ids': (None, ','.join(swissprot_ids)),
    }
    response = requests.post(
        'https://rest.uniprot.org/idmapping/run', files=files)
    print(response.text)
    jobid = response.json()['jobId']

    status = 'RUNNING'
    while status != 'FINISHED':
        response = requests.get(f'https://rest.uniprot.org/idmapping/status/{jobid}')
        if len(response.text) > 100:
            results = response.json()['results']
            break
        # else:
            # print(response.text)
        # try:
            # status = response.json()['jobStatus']
        # except KeyError:
            # break
    
    # result = requests.get(f'https://rest.uniprot.org/idmapping/uniref/results/{jobid}/')
    # yaml.safe_dump(result, open('uniprot_id_mapping.yaml', 'w'))
    for result in results:
        primary_accession = result['to']['primaryAccession']
        if '-' not in primary_accession:
            return primary_accession

# Example usage:
UniProt_ID = get_UniProt_ID("B3AT_HUMAN")
print(UniProt_ID)