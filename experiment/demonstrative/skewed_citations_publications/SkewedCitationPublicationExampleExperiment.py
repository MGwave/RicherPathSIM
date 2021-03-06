import texttable
from experiment.Experiment import Experiment
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Conference import Conference
from src.model.node.dblp.Paper import Paper
from src.similarity.heterogeneous.NeighborSimStrategy import NeighborSimStrategy
from src.similarity.heterogeneous.RecursivePathSimStrategy import RecursivePathSimStrategy
from src.similarity.heterogeneous.path_shape_count.FlattenedMatrixStrategy import FlattenedMatrixStrategy
from src.similarity.heterogeneous.path_shape_count.VectorProductStrategy import VectorProductStrategy
from src.util.EdgeBasedMetaPathUtility import EdgeBasedMetaPathUtility
from src.util.SampleGraphUtility import SampleGraphUtility

__author__ = 'jontedesco'


class SkewedCitationPublicationExampleExperiment(Experiment):
    """
      Experiment to test results of PathSim on examples given in PathSim paper
    """

    def outputSimilarityScores(self, authorMap, authors, strategy, strategyName):
        self.output('\n\n%s Scores (compared to Alice):' % strategyName)
        rows = [
            [author.name for author in authors],
            ['%1.2f' % strategy.findSimilarityScore(authorMap['Alice'], author) for author in authors]
        ]
        pathSimTable = texttable.Texttable()
        pathSimTable.add_rows(rows)
        self.output(pathSimTable.draw())

    def run(self):

        self.graph, authorMap, conference, citationsPublications = \
            SampleGraphUtility.constructSkewedCitationPublicationExample(introduceRandomness=False)

        # Get the nodes we care about
        authors = [
            authorMap['Alice'],
            authorMap['Bob'],
            authorMap['Carol'],
            authorMap['Dave'],
            authorMap['Ed'],
            authorMap['Frank']
        ]
        metaPathUtility = EdgeBasedMetaPathUtility()

        # Output adjacency matrices
        self.output('\nCPA Adjacency Matrix:')
        cpaadjMatrix, nodesIndex = metaPathUtility.getAdjacencyMatrixFromGraph(
            self.graph, [Conference, Paper, Author], project=True
        )
        adjMatrixTable = texttable.Texttable()
        rows = [['Conference'] + [author.name for author in authors]]
        rows += [[conference.name] + [cpaadjMatrix[nodesIndex[conference]][nodesIndex[author]] for author in authors]]
        adjMatrixTable.add_rows(rows)
        self.output(adjMatrixTable.draw())

        self.output('\nCPPA Adjacency Matrix:')
        cpaadjMatrix, nodesIndex = metaPathUtility.getAdjacencyMatrixFromGraph(
            self.graph, [Conference, Paper, Paper, Author], project=True
        )
        adjMatrixTable = texttable.Texttable()
        rows = [['Conference'] + [author.name for author in authors]]
        rows += [[conference.name] + [cpaadjMatrix[nodesIndex[conference]][nodesIndex[author]] for author in authors]]
        adjMatrixTable.add_rows(rows)
        self.output(adjMatrixTable.draw())

        # Total citation & publication counts
        self.output('\nCitation & Publication Counts')
        adjMatrixTable = texttable.Texttable()
        rows = [['Measure'] + [author.name for author in authors]]
        rows += [['Citations'] + [citationsPublications[author][0] for author in authors]]
        rows += [['Publications'] + [citationsPublications[author][1] for author in authors]]
        adjMatrixTable.add_rows(rows)
        self.output(adjMatrixTable.draw())

        # Output NeighborSim & PathSim similarity scores
        neighborSimStrategy = NeighborSimStrategy(self.graph, [Conference, Paper, Author], symmetric=True)
        self.outputSimilarityScores(authorMap, authors, neighborSimStrategy, 'APCPA PathSim')
        neighborSimStrategy = NeighborSimStrategy(self.graph, [Conference, Paper, Paper, Author])
        self.outputSimilarityScores(authorMap, authors, neighborSimStrategy, 'APPCPPA PathSim')

        # Omit extra duplicate entry in path, and weight at different levels of 'relative'
        for strategy, generalStrategyTitle in [(FlattenedMatrixStrategy, 'FlatMat'), (VectorProductStrategy, 'VectorProduct')]:
            for w in [1.0, 0.5, 0]:
                neighborPathShapeStrategy = strategy(
                    self.graph, weight=w, omit=[], metaPath=[Conference, Paper, Paper, Author], symmetric=True
                )
                strategyTitle = 'APPCPPA %s ShapeSim (%1.2f weight)' % (generalStrategyTitle, w)
                self.outputSimilarityScores(authorMap, authors, neighborPathShapeStrategy, strategyTitle)
        w = 1.0
        neighborPathShapeStrategy = VectorProductStrategy(
            self.graph, weight=w, omit=[0], metaPath=[Conference, Paper, Paper, Author], symmetric=True
        )
        strategyTitle = 'APPCPPA VectorProduct ShapeSim omitting CPC (%1.2f weight)' % w
        self.outputSimilarityScores(authorMap, authors, neighborPathShapeStrategy, strategyTitle)

        # Output recursive pathsim strategy score(s)
        recursivePathSimStrategy = RecursivePathSimStrategy(self.graph, [Conference, Paper, Paper, Author])
        self.outputSimilarityScores(authorMap, authors, recursivePathSimStrategy, 'APPCPPA Recursive PathSim')



if __name__ == '__main__':
    experiment = SkewedCitationPublicationExampleExperiment(
        None,
        'Skewed citation publication count example'
    )
    experiment.start()