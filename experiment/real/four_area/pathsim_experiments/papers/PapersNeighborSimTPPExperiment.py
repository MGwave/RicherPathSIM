import cPickle
import os
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.helper.MetaPathHelper import findMostSimilarNodes, getMetaPathAdjacencyData, testPapers
from experiment.real.four_area.helper.PathSimHelper import getNeighborSimScore

__author__ = 'jontedesco'

class PapersNeighborSimTPPExperiment(Experiment):
    """
      Runs some experiments with NeighborSim on paper similarity for the 'four area' dataset
    """

    def runFor(self, paper, adjMatrix, extraData):
        print("Running for %s..." % paper)

        # Find the top 10 most similar nodes to some given node
        mostSimilar, similarityScores = findMostSimilarNodes(adjMatrix, paper, extraData, method = getNeighborSimScore)
        self.output('Most Similar to "%s":' % paper)
        mostSimilarTable = texttable.Texttable()
        rows = [['Paper', 'Score']]
        rows += [[name, score] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())


def run():
    experiment = PapersNeighborSimTPPExperiment(
        None, 'Most Similar TPP NeighborSim Authors', outputFilePath='results/papers/tppNeighborSim')

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('../../data', 'graphWithCitations')))
    appAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['term', 'paper', 'paper'])
    extraData['fromNodes'] = extraData['toNodes']
    extraData['fromNodesIndex'] = extraData['toNodesIndex']

    for testPaper in testPapers:
        experiment.runFor(testPaper, appAdjMatrix, extraData)

if __name__ == '__main__': run()