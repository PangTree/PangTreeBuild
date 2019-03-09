import unittest
from ddt import ddt
import numpy as np
from tests.context import PangraphPO_Translator
from tests.context import Pangraph
from tests.context import Node
from tests.context import nucleotides as n
from tests.context import NodePO, SequencePO

@ddt
class PangraphPOTranslator_get_po_content_Test(unittest.TestCase):

    def setUp(self):
        nodes = [Node(id=0, base=n.code('T'), aligned_to=None,),
                 Node(id=1, base=n.code('A'), aligned_to=2),
                 Node(id=2, base=n.code('G'), aligned_to=1),
                 Node(id=3, base=n.code('A'), aligned_to=4),
                 Node(id=4, base=n.code('C'), aligned_to=3),
                 Node(id=5, base=n.code('A'), aligned_to=6),
                 Node(id=6, base=n.code('C'), aligned_to=7),
                 Node(id=7, base=n.code('G'), aligned_to=8),
                 Node(id=8, base=n.code('T'), aligned_to=5),
                 Node(id=9, base=n.code('A'), aligned_to=None),
                 Node(id=10, base=n.code('C'), aligned_to=11),
                 Node(id=11, base=n.code('T'), aligned_to=10),
                 Node(id=12, base=n.code('G'), aligned_to=None),
                 Node(id=13, base=n.code('A'), aligned_to=14),
                 Node(id=14, base=n.code('C'), aligned_to=13)
                 ]

        paths = {
            'testseq0': [[0, 1, 3, 5, 9, 10, 13]],
            'testseq1': [[1, 3, 6, 9, 11]],
            'testseq2': [[2, 4, 7, 9, 11, 12]],
            'testseq3': [[2, 4, 8, 9, 11, 12, 14]]
        }
        self.pangraph = Pangraph()
        self.pangraph.nodes = nodes
        self.pangraph.paths = paths

    def test_subpangraph_construction_from_pangraph_keep_seq_0_1(self):
        expected_ponodes = [NodePO(base=n.code('T'), aligned_to=None, in_nodes=[], sequences_ids=[0]),
                            NodePO(base=n.code('A'), aligned_to=None, in_nodes=[0], sequences_ids=[0, 1]),
                            NodePO(base=n.code('A'), in_nodes=[1], aligned_to=None, sequences_ids=[0, 1]),
                            NodePO(base=n.code('A'), in_nodes=[2], aligned_to=4, sequences_ids=[0]),
                            NodePO(base=n.code('C'), in_nodes=[2], aligned_to=3, sequences_ids=[1]),
                            NodePO(base=n.code('A'), in_nodes=[3, 4], aligned_to=None, sequences_ids=[0]),
                            NodePO(base=n.code('C'), in_nodes=[5], aligned_to=7, sequences_ids=[0]),
                            NodePO(base=n.code('T'), in_nodes=[5], aligned_to=6, sequences_ids=[1]),
                            NodePO(base=n.code('A'), in_nodes=[6], aligned_to=None, sequences_ids=[0])]
        expected_posequences = [SequencePO(name='testseq0',
                                           nodes_count=7,
                                           weight=0,
                                           consensus_id=-1,
                                           start_node_id=0),
                                SequencePO(name='testseq1',
                                           nodes_count=5,
                                           weight=100,
                                           consensus_id=-1,
                                           start_node_id=1),
                                ]

        expected_nodes_ids_mapping = {0: 0, 1: 1, 2: 3, 3: 5, 4: 6, 5: 9, 6: 10, 7: 11, 8: 13}

        translator = PangraphPO_Translator(self.pangraph, ['testseq0', 'testseq1'])
        actual_po_content = translator.get_input_po_content()
        expected_po_content = "VERSION=pangenome\n"\
                               "NAME=pangenome\n"\
                               "TITLE=pangenome\n"\
                               "LENGTH=9\n"\
                               "SOURCECOUNT=2\n"\
                               "SOURCENAME=testseq0\n"\
                               "SOURCEINFO=7 0 0 -1 testseq0\n"\
                               "SOURCENAME=testseq1\n"\
                               "SOURCEINFO=5 1 100 -1 testseq1\n"\
                               "t:S0\n"\
                               "a:L0S0S1\n"\
                               "a:L1S0S1\n"\
                               "a:L2S0A4\n"\
                               "c:L2S1A3\n"\
                               "a:L3L4S0S1\n"\
                               "c:L5S0A7\n"\
                               "t:L5S1A6\n"\
                               "a:L6S0"
        self.assertEqual(expected_po_content, actual_po_content)

    def test_subpangraph_construction_from_pangraph_keep_seq3(self):
        expected_nodes = [NodePO(base=n.code('C'), in_nodes=[], aligned_to=None, sequences_ids=[0]),
                          NodePO(base=n.code('A'), in_nodes=[0], aligned_to=None, sequences_ids=[0]),
                          NodePO(base=n.code('T'), in_nodes=[1], aligned_to=None, sequences_ids=[0]),
                          NodePO(base=n.code('A'), in_nodes=[2], aligned_to=None, sequences_ids=[0]),
                          NodePO(base=n.code('T'), in_nodes=[3], aligned_to=None, sequences_ids=[0]),
                          NodePO(base=n.code('G'), in_nodes=[4], aligned_to=None, sequences_ids=[0]),
                          NodePO(base=n.code('C'), in_nodes=[5], aligned_to=None, sequences_ids=[0])
                          ]
        expected_posequences = [
            SequencePO(name='testseq3', nodes_count=7, weight=100, consensus_id=-1, start_node_id=0)
        ]
        expected_nodes_ids_mapping = {0: 2, 1: 4, 2: 8, 3: 9, 4: 11, 5: 12, 6: 14}

        translator = PangraphPO_Translator(self.pangraph, ['testseq3'])
        actual_po_content = translator.get_input_po_content()
        expected_po_content = "VERSION=pangenome\n" \
                              "NAME=pangenome\n" \
                              "TITLE=pangenome\n" \
                              "LENGTH=7\n" \
                              "SOURCECOUNT=1\n" \
                              "SOURCENAME=testseq3\n" \
                              "SOURCEINFO=7 0 100 -1 testseq3\n" \
                              "g:S0\n" \
                              "c:L0S0\n" \
                              "t:L1S0\n" \
                              "a:L2S0\n" \
                              "t:L3S0\n" \
                              "g:L4S0\n" \
                              "c:L5S0"
        self.assertEqual(expected_po_content, actual_po_content)


    def test_subpangraph_construction_full_graph(self):
        nodes = [Node(id=0, base=n.code('A'), aligned_to=None),
                 Node(id=1, base=n.code('A'), aligned_to=None),
                 Node(id=2, base=n.code('C'), aligned_to=None),
                 Node(id=3, base=n.code('A'), aligned_to=None),
                 Node(id=4, base=n.code('T'), aligned_to=None)
                 ]

        paths = {
            'testseq1': [[0, 1, 2, 3, 4]]
        }
        expected_pangraph = Pangraph()
        expected_pangraph.nodes = nodes
        expected_pangraph.paths = paths

        expected_nodes_ids_mapping = {0: 1, 1: 2, 2: 4, 3: 5, 4: 7}

        expected_nodes = [NodePO(base=n.code('A'), in_nodes=[], aligned_to=None, sequences_ids=[0]),
                          NodePO(base=n.code('A'), in_nodes=[0], aligned_to=None, sequences_ids=[0]),
                          NodePO(base=n.code('C'), in_nodes=[1], aligned_to=None, sequences_ids=[0]),
                          NodePO(base=n.code('A'), in_nodes=[2], aligned_to=None, sequences_ids=[0]),
                          NodePO(base=n.code('T'), in_nodes=[3], aligned_to=None, sequences_ids=[0])
                          ]
        expected_posequences = [
            SequencePO(name='testseq1', nodes_count=5, weight=100, consensus_id=-1, start_node_id=0)
        ]

        translator = PangraphPO_Translator(self.pangraph, ['testseq1'])
        actual_po_content = translator.get_input_po_content()
        expected_po_content = "VERSION=pangenome\n" \
                              "NAME=pangenome\n" \
                              "TITLE=pangenome\n" \
                              "LENGTH=5\n" \
                              "SOURCECOUNT=1\n" \
                              "SOURCENAME=testseq1\n" \
                              "SOURCEINFO=5 0 100 -1 testseq1\n" \
                              "a:S0\n" \
                              "a:L0S0\n" \
                              "c:L1S0\n" \
                              "a:L2S0\n" \
                              "t:L3S0"
        self.assertEqual(expected_po_content, actual_po_content)


    def test_subpangraph_should_omit_edges_1(self):
        pangraph_nodes = [Node(id=0,base=n.code('A'), aligned_to=None),
                          Node(id=1,base=n.code('C'), aligned_to=None),
                          Node(id=2,base=n.code('C'), aligned_to=None)]
        pangraph_paths_to_nodes_ids = {
            'seq1': [[0, 2]],
            'seq2': [[0, 1, 2]]
        }
        pangraph = Pangraph()
        pangraph.nodes = pangraph_nodes
        pangraph.paths = pangraph_paths_to_nodes_ids

        # remove seq1
        expected_ponodes = [
            NodePO(base=n.code('A'), in_nodes=[], aligned_to=None, sequences_ids=[2]),
            NodePO(base=n.code('C'), in_nodes=[0], aligned_to=None, sequences_ids=[2]),
            NodePO(base=n.code('C'), in_nodes=[1], aligned_to=None, sequences_ids=[2])
        ]
        expected_ppo_sequences = {
            SequencePO(name='seq2', nodes_count=3, weight=100,consensus_id=-1,start_node_id=0)
        }
        expected_nodes_ids_mapping = {0: 0, 1: 1, 2: 2}

        translator = PangraphPO_Translator(pangraph, ['seq2'])
        actual_po_content = translator.get_input_po_content()
        expected_po_content = "VERSION=pangenome\n" \
                              "NAME=pangenome\n" \
                              "TITLE=pangenome\n" \
                              "LENGTH=3\n" \
                              "SOURCECOUNT=1\n" \
                              "SOURCENAME=seq2\n" \
                              "SOURCEINFO=3 0 100 -1 seq2\n" \
                              "a:S0\n" \
                              "c:L0S0\n" \
                              "c:L1S0"
        self.assertEqual(expected_po_content, actual_po_content)


    def test_subpangraph_should_omit_edges_2(self):
        pangraph_nodes = [Node(id=0, base=n.code('A'), aligned_to=None),
                          Node(id=1, base=n.code('C'), aligned_to=None),
                          Node(id=2, base=n.code('C'), aligned_to=None)]
        pangraph_paths_to_nodes_ids = {
            'seq1': [[0, 2]],
            'seq2': [[0, 1, 2]]
        }
        pangraph = Pangraph()
        pangraph.nodes = pangraph_nodes
        pangraph.paths = pangraph_paths_to_nodes_ids

        # remove seq2
        expected_nodes = [
            NodePO(base=n.code('A'), in_nodes=[], aligned_to=None, sequences_ids=[0]),
            NodePO(base=n.code('C'), in_nodes=[0], aligned_to=None, sequences_ids=[0]),
        ]
        expected_po_sequences = {
            SequencePO(name='seq1', nodes_count=2, weight=100, consensus_id=-1, start_node_id= 0)
        }
        expected_nodes_ids_mapping = {0: 0, 1: 2}

        translator = PangraphPO_Translator(pangraph, ['seq1'])
        actual_po_content = translator.get_input_po_content()
        expected_po_content = "VERSION=pangenome\n" \
                              "NAME=pangenome\n" \
                              "TITLE=pangenome\n" \
                              "LENGTH=2\n" \
                              "SOURCECOUNT=1\n" \
                              "SOURCENAME=seq1\n" \
                              "SOURCEINFO=2 0 100 -1 seq1\n" \
                              "a:S0\n" \
                              "c:L0S0"

        self.assertEqual(expected_po_content, actual_po_content)

    def test_subpangraph_should_omit_in_nodes_and_aligned_nodes(self):
        #original pangraph
        pangraph_nodes = [Node(id=0,base=n.code('A'), aligned_to=None),
                          Node(id=1,base=n.code('C'), aligned_to=2),
                          Node(id=2,base=n.code('T'), aligned_to=1),
                          Node(id=3,base=n.code('G'), aligned_to=None)]
        pangraph_paths_to_nodes_ids = {
            'seq1': [[0, 1, 3]],
            'seq2': [[0, 2, 3]]
        }
        pangraph = Pangraph()
        pangraph.nodes = pangraph_nodes
        pangraph.paths = pangraph_paths_to_nodes_ids

        # remove seq1
        expected_ponodes = [
            NodePO(base=n.code('A'), in_nodes=[], aligned_to=None, sequences_ids=[1]),
            NodePO(base=n.code('T'), in_nodes=[0], aligned_to=None, sequences_ids=[1]),
            NodePO(base=n.code('G'), in_nodes=[1], aligned_to=None, sequences_ids=[1])
        ]
        expected_sequence_po = {
            SequencePO(name='seq2', nodes_count=3, weight=100,consensus_id=-1,start_node_id=0)
        }
        expected_nodes_ids_mapping = {0: 0, 1: 2, 2: 3}

        translator = PangraphPO_Translator(pangraph, ['seq2'])
        actual_po_content = translator.get_input_po_content()
        expected_po_content = "VERSION=pangenome\n" \
                              "NAME=pangenome\n" \
                              "TITLE=pangenome\n" \
                              "LENGTH=3\n" \
                              "SOURCECOUNT=1\n" \
                              "SOURCENAME=seq2\n" \
                              "SOURCEINFO=3 0 100 -1 seq2\n" \
                              "a:S0\n" \
                              "t:L0S0\n" \
                              "g:L1S0"

        self.assertEqual(expected_po_content, actual_po_content)


    def compare_subpangraphs(self, expected_subpangraph, actual_subpangraph):
        self.assertEqual(expected_subpangraph.pangraph._nodes, actual_subpangraph.pangraph._nodes)
        self.assertTrue(np.array_equal(expected_subpangraph.pangraph._pathmanager.paths, actual_subpangraph.pangraph._pathmanager.paths))
        self.assertEqual(expected_subpangraph.nodes_ids_mapping, actual_subpangraph.nodes_ids_mapping)