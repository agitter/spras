# Datasets
This directory contains example datasets.
It can also be used to store new input data files.
There are currently very small toy datasets and one real dataset.

## File formats
### Node file
Node files include a header row and rows providing attributes for each node.
One column is for the node identifier and must have the header value `NODEID`.
All other columns specify additional node attributes such as prizes.
Any nodes that are listed in a node file but are not present in one or more edges in the edge file will be removed.
For example:
```
NODEID	prize	sources	targets
A	1.0		True
B	3.3	True	
C	2.5		True
D	1.9	True	True
```

A secondary format provides only a list of node identifiers and uses the filename as the node attribute, as in the example `sources.txt`.
This format may be deprecated.

### Edge file
Edge files do not include a header row.
If the edge file three columns, all edges are assumed to be undirected.
In that case, each row lists the two nodes that are connected with an undirected edge and a weight for that edge.
The weights are typically in the range [0,1] with 1 being the highest confidence for the edge.

For example:
```
A	B	0.98
B	C	0.77
```

There is preliminary support for mixed graphs with both directed and undirected edges.
In that case, the fourth column uses `U` for an undirected edge and `D` for a directed edge from the first column to the second.

For example:
```
A	B	0.98	D
B	C	0.77	U
```

## Toy datasets
The following files are very small toy datasets used to illustrate the supported file formats
- `alternative-network.txt`
- `alternative-targets.txt`
- `dir-network.txt`
- `dir-node-prizes.txt`
- `network.txt`
- `node-prizes.txt`
- `sources.txt`
- `targets.txt`

## Epidermal growth factor receptor (EGFR)
This dataset represents protein phosphorylation changes in response to epidermal growth factor (EGF) treatment.
The network includes protein-protein interactions from [iRefIndex](http://irefindex.org/) and kinase-substrate interactions from [PhosphoSitePlus](http://www.phosphosite.org/).
The files are originally from the [Temporal Pathway Synthesizer (TPS)](https://github.com/koksal/tps) repository.
They have been lightly modified for SPRAS by lowering one edge weight that was greater than 1, removing a PSEUDONODE prize, adding a prize of 10.0 to EGF_HUMAN, and converting all edges to undirected edges.
The only source is EGF_HUMAN.
All proteins with phosphorylation-based prizes are also labeled as targets.

If you use any of the input files `tps-egfr-prizes.txt` or `phosphosite-irefindex13.0-uniprot.txt`, reference the publication

[Synthesizing Signaling Pathways from Temporal Phosphoproteomic Data](https://doi.org/10.1016/j.celrep.2018.08.085).
Ali Sinan K�ksal, Kirsten Beck, Dylan R. Cronin, Aaron McKenna, Nathan D. Camp, Saurabh Srivastava, Matthew E. MacGilvray, Rastislav Bod�k, Alejandro Wolf-Yadlin, Ernest Fraenkel, Jasmin Fisher, Anthony Gitter.
*Cell Reports* 24(13):3607-3618 2018.

If you use the network file `phosphosite-irefindex13.0-uniprot.txt`, also reference iRefIndex and PhosphoSitePlus.

[iRefIndex: a consolidated protein interaction database with provenance](https://doi.org/10.1186/1471-2105-9-405).
Sabry Razick, George Magklaras, Ian M Donaldson.
*BMC Bioinformatics* 9(405) 2008.

[PhosphoSitePlus, 2014: mutations, PTMs and recalibrations](https://doi.org/10.1093/nar/gku1267).
Peter V Hornbeck, Bin Zhang, Beth Murray, Jon M Kornhauser, Vaughan Latham, Elzbieta Skrzypek.
*Nucleic Acids Research* 43(D1):D512-520 2015.

The TPS [publication](https://doi.org/10.1016/j.celrep.2018.08.085) describes how the network data and protein prizes were prepared.
