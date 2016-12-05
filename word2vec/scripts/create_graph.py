import os
import sys, subprocess, os
from subprocess import call
from tempfile import NamedTemporaryFile

from tulip import *

DATA_DIR = "../data"
BIN_DIR = "../bin"
SRC_DIR = "../src"

TEXT_DATA = DATA_DIR+"/mon5.cln"
VECTOR_DATA = DATA_DIR+"/mon5.vec"

init_words = ["opencare"]

BIN_DIR+="/distance"
ARG = DATA_DIR+"/"+VECTOR_DATA

KNN = 10
min_KNN = 1
max_KNN = 3

def parse_w2vec_output(output):
	lines = output.split('\n')[5:5+KNN]
	vector = {}

	for l in lines:
		word, weight = l.split()
		vector[word] = float(weight)

	return vector

def call_w2vec(query):
	command = [BIN_DIR, ARG]
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

	grep_stdout = process.communicate(input=query+'\nEXIT\n')[0]
	return parse_w2vec_output(grep_stdout)

def create_graph():
	global KNN

	graph = tlp.newGraph()
	vLabel = graph.getStringProperty("viewLabel")

	for KNN in range(min_KNN,max_KNN+1):
		print "processing k=", KNN

		g = graph.addSubGraph()
		g.setName("Word2Vec KNN="+str(KNN))

		weight = g.getDoubleProperty("cosine_similarity")
		w2n = {}
		queried = set()

		def getNode(w):
			if w not in w2n:
				n = graph.addNode()
				vLabel[n] = w
				w2n[w] = n
			
			n = w2n[w]
			g.addNode(n)
			return n

		currentVector = init_words
		#updated = True

		while len(currentVector) > 0:

			new_vector = set()
			#print " before: ",currentVector

			for w1 in currentVector:
				#print "processing ", w1, g.numberOfNodes(), '/', g.numberOfEdges()
				#updated = False

				if w1 not in queried:
					#updated = True
					queried.update([w1])
					#print len(queried)
					n1 = getNode(w1)
					vec = call_w2vec(w1)
					#print vec

					for w2 in vec:
						n2 = getNode(w2)

						e = graph.existEdge(n1, n2, True)

						if not e.isValid():
							e = graph.addEdge(n1, n2)
						g.addEdge(e)

						weight[e] = vec[w2]

					new_vector.update(vec)

			currentVector = new_vector
			#print " after: ",currentVector

		viewLayout = g.getLayoutProperty("viewLayout")
		g.applyLayoutAlgorithm("FM^3 (OGDF)", viewLayout)

		gg = g.addSubGraph()
		gg.setName("Word2Vec mutual KNN="+str(KNN))
		maxWeight = gg.getDoubleProperty("max_weight")

		for n1 in g.getNodes():
			for n2 in g.getInOutNodes(n1):
				e1 = graph.existEdge(n1, n2, True)
				e2 = graph.existEdge(n2, n1, True)
				if e1.isValid() and e2.isValid():
					gg.addNode(n1)
					gg.addNode(n2)
					gg.addEdge(e1)
					maxWeight[e1] = max(weight[e1], weight[e2])



	print tlp.saveGraph(graph, DATA_DIR+'/graph.tlp')


if __name__ == '__main__':
	create_graph()