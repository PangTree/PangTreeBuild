from bisect import bisect_left
from pathlib import Path
from typing import List, Dict, Union

from pangraph import Pangraph
from tools import pathtools
from pangraph.custom_types import NodeID, SequenceID
from pangraph.PangraphToFilesConverters.PangraphToPO import PangraphToPO, NodePO, SequencePO
from consensus.exceptions import TreeConsensusGenerationException
from call_external.poa import call as call_poa


def get_top_consensus(pangraph: Pangraph,
                      sequences_ids: List[SequenceID],
                      output_dir: Path,
                      file_prefix: str,
                      blosum_path) -> List[NodeID]:
    poa_input_path = pathtools.get_child_file_path(output_dir, f"{file_prefix}_in_pangenome.po")
    poa_output_path = pathtools.get_child_file_path(output_dir, f"{file_prefix}_out_pangenome.po")

    s = PangraphPO_Translator(pangraph, sequences_ids)
    poa_input_content = s.get_input_po_content()
    with open(poa_input_path, 'w') as poa_input:
        poa_input.write(poa_input_content)
    call_poa(po_file_path=poa_input_path,
             hb_file_path=poa_output_path,
             blosum_path=blosum_path,
             hbmin=0.6)
    with open(poa_output_path) as poa_output:
        poa_output_lines = poa_output.readlines()
    top_consensus = s.read_top_consensus(poa_output_lines)

    return top_consensus


class PangraphPO_Translator:
    def __init__(self, pangraph: Pangraph, sequences_ids: List[SequenceID]):
        self.pangraph: Pangraph = pangraph
        self.sequences_ids: List[SequenceID] = sequences_ids
        self.new_to_old: Dict[NodeID, NodeID] = None
        self.old_to_new: Dict[NodeID, NodeID] = None
        self.seq_old_to_new: Dict[SequenceID, int] = None
        self.seq_new_to_old: Dict[int, SequenceID] = None

    def get_input_po_content(self) -> str:
        paths_to_keep = [path
                         for seq_id in self.sequences_ids
                         for path in self.pangraph.paths[seq_id]]
        nodes_ids_to_keep = list(set([node_id
                                      for path in paths_to_keep
                                      for node_id in path]))
        sorted_nodes_ids_to_keep = sorted(nodes_ids_to_keep)
        self.old_to_new = {node_id: i for i, node_id in enumerate(sorted_nodes_ids_to_keep)}
        self.new_to_old = {new_node_id: old_node_id for old_node_id, new_node_id in self.old_to_new.items()}
        self.seq_old_to_new = {seq_id: i for i, seq_id in enumerate(self.sequences_ids)}
        self.seq_new_to_old = {i: seq_id for seq_id, i in self.seq_old_to_new.items()}

        po_nodes = [NodePO(base=self.pangraph.nodes[self.new_to_old[new_node_id]].base,
                           aligned_to=self._get_aligned_node(self.new_to_old[new_node_id], sorted_nodes_ids_to_keep),
                           in_nodes=set(),
                           sequences_ids=[]
                           )
                    for new_node_id in range(len(nodes_ids_to_keep))]

        sequences_weight: Dict[SequenceID, int] = self.pangraph.get_sequences_weights(self.sequences_ids)
        po_sequences = [SequencePO(name=self.seq_new_to_old[new_seq_id],
                                   nodes_count=self.pangraph.get_sequence_nodes_count(self.seq_new_to_old[new_seq_id]),
                                   weight=sequences_weight[self.seq_new_to_old[new_seq_id]],
                                   consensus_id=-1,
                                   start_node_id=self.old_to_new[
                                       self.pangraph.paths[self.seq_new_to_old[new_seq_id]][0][0]]
                                   )
                        for new_seq_id in range(len(paths_to_keep))]

        for seq_id in self.sequences_ids:
            new_seq_id = self.seq_old_to_new[seq_id]
            for path in self.pangraph.paths[seq_id]:
                for i, node_id in enumerate(path):
                    new_node_id = self.old_to_new[node_id]
                    po_nodes[new_node_id].sequences_ids.append(new_seq_id)
                    if i > 0:
                        new_in_node_id = self.old_to_new[path[i-1]]
                        po_nodes[new_node_id].in_nodes.add(new_in_node_id)

        for node in po_nodes:
            node.in_nodes = sorted(node.in_nodes)

        p_to_po = PangraphToPO()
        return p_to_po.get_po_file_content(po_nodes, po_sequences)

    def _get_aligned_node(self, old_node_id: NodeID, sorted_nodes_ids_to_keep: List[NodeID]) -> Union[NodeID, None]:
        aligned_to = self.pangraph.nodes[old_node_id].aligned_to
        if aligned_to is None:
            return None
        while aligned_to != old_node_id:
            if self.is_in(sorted_list=sorted_nodes_ids_to_keep, x=aligned_to):
                return self.old_to_new[aligned_to]
            aligned_to = self.pangraph.nodes[aligned_to].aligned_to
        return None

    def is_in(self, sorted_list, x):
        i = bisect_left(sorted_list, x)
        if i != len(sorted_list) and sorted_list[i] == x:
            return True
        return False

    def read_top_consensus(self, poa_output_lines: List[str]) -> List[NodeID]:
        po_lines_iterator = iter(poa_output_lines)

        for i in range(3):
            next(po_lines_iterator)

        nodes_count = int(self._extract_line_value(next(po_lines_iterator)))
        paths_count = int(self._extract_line_value(next(po_lines_iterator)))

        top_consensus_expected_id = len(self.sequences_ids)
        if paths_count == top_consensus_expected_id:
            raise TreeConsensusGenerationException("No additional sequences in output po than in input!")

        detailed_consens0_info = None
        for i in range(2*paths_count):
            path_name = self._extract_line_value(next(po_lines_iterator))
            if path_name == "CONSENS0":
                detailed_consens0_info = next(po_lines_iterator)
                if i != top_consensus_expected_id:
                    raise Exception("Consensus is found in unexpected line number!")
                break
            else:
                _ = next(po_lines_iterator)
                continue

        if detailed_consens0_info is None:
            raise Exception("Cannot find sequence with name \"CONSENS0\" in output po file.")


        detailed_info = self._extract_line_value(detailed_consens0_info).split(' ')
        consens0_nodes_count = int(detailed_info[0])
        consensus_name = f"S{top_consensus_expected_id}"
        first_node_line_id = 5 + paths_count * 2
        old_node_id = 0
        new_node_id = 0
        consensus_path : List[NodeID] = [None] * consens0_nodes_count
        for file_position in range(first_node_line_id, len(poa_output_lines)):
            if consensus_name in poa_output_lines[file_position]:
                consensus_path[old_node_id] = self.new_to_old[new_node_id]
                old_node_id += 1
            new_node_id += 1

        return consensus_path

    def _extract_line_value(self, line: str) -> str:
        return line.split('=')[1].strip()