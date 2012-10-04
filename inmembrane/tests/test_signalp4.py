import os
import unittest
import sys

import inmembrane
import inmembrane.tests
from inmembrane import helpers
from inmembrane.plugins import signalp4

class TestSignalp(unittest.TestCase):
  def setUp(self):
    self.dir = os.path.join(
       os.path.abspath(
       os.path.dirname(inmembrane.tests.__file__)), 'signalp4')

  def test_signalp(self):
    save_dir = os.getcwd()
    os.chdir(self.dir)

    helpers.silence_log(True)
    helpers.clean_directory('.', ['input.fasta'])
    
    self.params = inmembrane.get_params()
    if not self.params['signalp4_bin']:
      self.params['signalp4_bin'] = 'signalp'
    self.params['fasta'] = "input.fasta"
    self.params['signalp4_organism'] = 'gram+'
    self.seqids, self.proteins = \
        helpers.create_proteins_dict(self.params['fasta'])
    signalp4.annotate(self.params, self.proteins)

    self.expected_output = {
        u'SPy_0252': True, 
        u'SPy_2077': False, 
        u'SPy_0317': True,
        u'sp|B7LNW7': True,
    }
    for seqid in self.expected_output:
      self.assertEqual(
          self.expected_output[seqid], self.proteins[seqid]['is_signalp'])
    self.assertEqual(self.proteins[u'sp|B7LNW7']['signalp_cleave_position'], 22)
    os.chdir(save_dir)


if __name__ == '__main__':
  unittest.main()