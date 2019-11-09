import unittest
from pathlib import Path

from ddt import unpack, data, ddt

from tests.context import pathtools,graph, po, multialignment


def nid(x): return graph.NodeID(x)


def bid(x): return graph.Base(x)


@ddt
class PoagraphToPOTests(unittest.TestCase):

    def setUp(self):
        self.po_files_dir = 'tests/output/po_files/'

    def test_1_typical_poagraph(self):
        expected_po_content_path = Path(self.po_files_dir + "test_1.po")

        poagraph_nodes = [graph.Node(node_id=nid(0), base=bid('A'), aligned_to=nid(1)),
                          graph.Node(node_id=nid(1), base=bid('G'), aligned_to=nid(0)),
                          graph.Node(node_id=nid(2), base=bid('C'), aligned_to=nid(3)),
                          graph.Node(node_id=nid(3), base=bid('G'), aligned_to=nid(2)),
                          graph.Node(node_id=nid(4), base=bid('A'), aligned_to=nid(5)),
                          graph.Node(node_id=nid(5), base=bid('T'), aligned_to=nid(4)),
                          graph.Node(node_id=nid(6), base=bid('G'), aligned_to=None),
                          graph.Node(node_id=nid(7), base=bid('G'), aligned_to=None),
                          graph.Node(node_id=nid(8), base=bid('A'), aligned_to=nid(9)),
                          graph.Node(node_id=nid(9), base=bid('C'), aligned_to=nid(10)),
                          graph.Node(node_id=nid(10), base=bid('G'), aligned_to=nid(11)),
                          graph.Node(node_id=nid(11), base=bid('T'), aligned_to=nid(8)),
                          graph.Node(node_id=nid(12), base=bid('A'), aligned_to=nid(13)),
                          graph.Node(node_id=nid(13), base=bid('C'), aligned_to=nid(12)),
                          graph.Node(node_id=nid(14), base=bid('T'), aligned_to=None),
                          graph.Node(node_id=nid(15), base=bid('A'), aligned_to=nid(16)),
                          graph.Node(node_id=nid(16), base=bid('C'), aligned_to=nid(17)),
                          graph.Node(node_id=nid(17), base=bid('G'), aligned_to=nid(15))
                          ]

        poagraph_sequences = {
            msa.SequenceID('seq0'):
                graph.Sequence(msa.SequenceID('seq0'),
                              [graph.SeqPath([*map(nid, [0, 2, 4, 6, 7, 8, 12, 14, 16])])],
                              graph.SequenceMetadata({'group': '1'})),
            msa.SequenceID('seq1'):
                graph.Sequence(msa.SequenceID('seq1'),
                              [graph.SeqPath([*map(nid, [1, 2, 5, 6, 7, 9])])],
                              graph.SequenceMetadata({'group': '1'})),
            msa.SequenceID('seq2'):
                graph.Sequence(msa.SequenceID('seq2'),
                              [graph.SeqPath([*map(nid, [3, 4, 6, 7, 10, 12, 14, 17])])],
                              graph.SequenceMetadata({'group': '1'})),
            msa.SequenceID('seq3'):
                graph.Sequence(msa.SequenceID('seq3'),
                              [graph.SeqPath([*map(nid, [11, 13, 14, 15])])],
                              graph.SequenceMetadata({'group': '1'})),
        }

        poagraph = graph.Poagraph(poagraph_nodes, poagraph_sequences)

        actual_po_content = po.poagraph_to_PangenomePO(poagraph)
        expected_po_content = pathtools.get_file_content(expected_po_content_path)
        self.assertEqual(expected_po_content, actual_po_content)

    def test_2_consensuses_and_empty_sequences(self):
        expected_po_content_path = Path(self.po_files_dir + "test_2.po")

        poagraph_nodes = [graph.Node(node_id=nid(0), base=bid('C'), aligned_to=nid(1)),
                          graph.Node(node_id=nid(1), base=bid('T'), aligned_to=nid(0)),
                          graph.Node(node_id=nid(2), base=bid('A'), aligned_to=nid(3)),
                          graph.Node(node_id=nid(3), base=bid('G'), aligned_to=nid(2)),
                          graph.Node(node_id=nid(4), base=bid('C'), aligned_to=None),
                          graph.Node(node_id=nid(5), base=bid('T'), aligned_to=None),
                          graph.Node(node_id=nid(6), base=bid('A'), aligned_to=nid(7)),
                          graph.Node(node_id=nid(7), base=bid('T'), aligned_to=nid(6)),
                          graph.Node(node_id=nid(8), base=bid('G'), aligned_to=None)
                          ]

        poagraph_sequences = {
            msa.SequenceID('seq0'):
                graph.Sequence(msa.SequenceID('seq0'),
                              [graph.SeqPath([*map(nid, [0, 3, 4, 5, 6, 8])])],
                              graph.SequenceMetadata({'group': '1'})),
            msa.SequenceID('seq1'):
                graph.Sequence(msa.SequenceID('seq1'),
                              [graph.SeqPath([*map(nid, [1, 2, 4, 5, 7, 8])])],
                              graph.SequenceMetadata({'group': '1'})),
            msa.SequenceID('seq2'):
                graph.Sequence(msa.SequenceID('seq2'),
                              [],
                              graph.SequenceMetadata({'group': '1'})),
            msa.SequenceID('seq3'):
                graph.Sequence(msa.SequenceID('seq3'),
                              [],
                              graph.SequenceMetadata({'group': '1'})),
            msa.SequenceID('CONSENS0'):
                graph.Sequence(msa.SequenceID('CONSENS0'),
                              [graph.SeqPath([*map(nid, [0, 3, 4, 5, 7, 8])])],
                              None),
            msa.SequenceID('CONSENS1'):
                graph.Sequence(msa.SequenceID('CONSENS1'),
                              [graph.SeqPath([*map(nid, [1, 2, 4, 5, 6, 8])])],
                              None),
        }

        poagraph = graph.Poagraph(poagraph_nodes, poagraph_sequences)

        actual_po_content = po.poagraph_to_PangenomePO(poagraph)
        expected_po_content = pathtools.get_file_content(expected_po_content_path)
        self.assertEqual(expected_po_content, actual_po_content)

    @data(([], ""),
          ([nid(0), nid(1)], "L0L1"))
    @unpack
    def test_3_get_in_nodes_info(self, in_nodes, expected_in_nodes):
        actual_in_nodes = po._get_in_nodes_info(in_nodes)
        self.assertEqual(expected_in_nodes, actual_in_nodes)

    @data(([], ""),
          ([0, 1], "S0S1"),
          ([1, 3], "S1S3"))
    @unpack
    def test_get_sources_info(self, sources_ids, expected_info):
        actual_sources_ids = po._get_sources_info(sources_ids)
        self.assertEqual(expected_info, actual_sources_ids)

    @data((None, ""),
          (0, "A0"))
    @unpack
    def test_get_aligned_to_info(self, aligned_to, expected_aligned_to):
        actual_aligned_to = po._get_aligned_to_info(aligned_to)
        self.assertEqual(expected_aligned_to, actual_aligned_to)


if __name__ == '__main__':
    unittest.main()
