from Bio import AlignIO
from io import StringIO
from pangraph import nucleotides
from pangraph.Node import Node
from pangraph.PangraphBuilder.PangraphBuilderBase import PangraphBuilderBase
from metadata.MultialignmentMetadata import MultialignmentMetadata
from pangraph.custom_types import NodeID, SequenceID, Nucleobase, ColumnID, BlockID


class PangraphBuilderFromMAF(PangraphBuilderBase):
    def __init__(self, genomes_info: MultialignmentMetadata):
        super().__init__(genomes_info)
        self.pangraph = None

    def build(self, input: StringIO, pangraph):
        input = [*AlignIO.parse(input, "maf")]
        self.init_pangraph(pangraph)

        current_node_id = NodeID(-1)
        column_id = ColumnID(-1)
        for block_id, block in enumerate(input):
            block_width = len(block[0].seq)

            for col in range(block_width):
                column_id += 1
                sequence_name_to_nucleotide = {seq.id: seq[col] for seq in block}
                nodes_codes = sorted([*(
                    set([nucleotide for nucleotide in sequence_name_to_nucleotide.values()])).difference({'-'})])
                column_nodes_ids = [current_node_id + i + 1 for i, _ in enumerate(nodes_codes)]

                for i, nucl in enumerate(nodes_codes):
                    current_node_id += 1
                    self.add_node(id=current_node_id,
                                  base=nucl,
                                  aligned_to=self.get_next_aligned_node_id(i, column_nodes_ids),
                                  column_id=column_id,
                                  block_id=block_id)

                    for sequence, nucleotide in sequence_name_to_nucleotide.items():
                        if nucleotide == nucl:
                            self.add_node_do_sequence(seqID=sequence, node_id=current_node_id)

    def init_pangraph(self, pangraph):
        pangraph.nodes = []
        pangraph.paths = {seq_id: [] for seq_id in self.sequences_names}
        self.pangraph = pangraph

    def add_node_do_sequence(self, seqID: SequenceID, node_id: NodeID):
        if self.pangraph.paths[seqID]:
            self.pangraph.paths[seqID][-1].append(node_id)
        else:
            self.pangraph.paths[seqID].append([node_id])

    def add_node(self,
                 id: NodeID,
                 base: Nucleobase,
                 aligned_to: NodeID,
                 column_id: ColumnID,
                 block_id: BlockID) -> None:
        self.pangraph.nodes.append(Node(node_id=id,
                                        base=nucleotides.code(base),
                                        aligned_to=aligned_to,
                                        column_id=column_id,
                                        block_id=block_id))

    def get_next_aligned_node_id(self, current_column_i, column_nodes_ids):
        if len(column_nodes_ids) > 1:
            return column_nodes_ids[(current_column_i + 1) % len(column_nodes_ids)]
        return None

    @staticmethod
    def get_nodes_count(mafalignment) -> int:
        nodes_count = 0
        for block in mafalignment:
            number_of_columns = len(block[0].seq)

            for col_id in range(number_of_columns):
                letters_in_columns = set([block[i].seq[col_id] for i in range(len(block))]).difference(set('-'))
                nodes_count += len(letters_in_columns)

        return nodes_count


