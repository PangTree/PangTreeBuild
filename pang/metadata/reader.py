import json
from .SequenceMetadata import SequenceMetadata
from .MultialignmentMetadata import MultialignmentMetadata


def read(gen_info_file):
    """Parse genomes metadata file to Metadata object."""

    with open(gen_info_file) as p:
        metadata = json.load(p)
        genome_metadata = {seq['id']: SequenceMetadata(name=seq['name'],
                                                       genbankID=seq['genbankID'],
                                                       assemblyID=seq['assemblyID'],
                                                       mafname=seq['mafname'],
                                                       group=seq['group'])for seq in metadata['data']}
        return MultialignmentMetadata(title=metadata['title'],
                                      version=metadata['source'],
                                      genomes_metadata=genome_metadata)