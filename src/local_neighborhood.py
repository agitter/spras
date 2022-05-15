import pandas as pd
from pathlib import Path
from src.PRM import PRM
from src.util import prepare_volume, run_container

__all__ = ['LocalNeighborhood']


class LocalNeighborhood(PRM):
    required_inputs = ['network', 'nodes']

    def generate_inputs(data, filename_map):
        """
        Access fields from the dataset and write the required input files
        @param data: dataset
        @param filename_map: a dict mapping file types in the required_inputs to the filename for that type
        @return:
        """
        for input_type in LocalNeighborhood.required_inputs:
            if input_type not in filename_map:
                raise ValueError(f"{input_type} filename is missing")

        node_df = data.node_table
        if not ('prize' in node_df.columns or 'sources' in node_df.columns or 'targets' in node_df.columns):
            raise ValueError('Local Neighborhood requires node prizes or sources or targets')

        #print(node_df)
        #print(node_df[node_df['targets'] == True]['NODEID'].values)
        node_set = set()
        # TODO debug why the prize column is missing
        if 'prize' in node_df.columns:
            node_set.update(node_df.loc[node_df['prize'] > 0, 'NODEID'])
        if 'sources' in node_df.columns:
            node_set.update(node_df[node_df['sources'] == True]['NODEID'].values)
        if 'targets' in node_df.columns:
            node_set.update(node_df[node_df['targets'] == True]['NODEID'].values)

        with open(filename_map['nodes'], 'w') as f:
            for node in sorted(node_set):
                f.write(f'{node}\n')

        edges_df = data.get_interactome()
        edges_df.to_csv(filename_map['network'], sep='|', index=False, columns=['Interactor1', 'Interactor2'])

    @staticmethod
    def run(network=None, nodes=None, output_file=None, singularity=False):
        """
        Run Local Neighborhood with Docker
        @param network:  input network file (required)
        @param nodes:  input node list (required)
        @param output_file: path to the output pathway file (required)
        @param singularity: if True, run using the Singularity container instead of the Docker container
        """
        if not network or not nodes or not output_file:
            raise ValueError('Required Local Neighborhood arguments are missing')

        work_dir = '/spras'

        # Each volume is a tuple (src, dest)
        volumes = list()

        bind_path, network_file = prepare_volume(network, work_dir)
        volumes.append(bind_path)

        bind_path, node_file = prepare_volume(nodes, work_dir)
        volumes.append(bind_path)

        # Ensure that the local output directory exists
        out_dir = Path(output_file).parent
        out_dir.mkdir(parents=True, exist_ok=True)
        bind_path, output_file = prepare_volume(output_file, work_dir)
        volumes.append(bind_path)

        command = ['python',
                   '/LocalNeighborhood/local_neighborhood.py',
                   '--network', network_file,
                   '--nodes', node_file,
                   '--output', output_file]

        print('Running Local Neighborhood with arguments: {}'.format(' '.join(command)), flush=True)

        # TODO consider making this a string in the config file instead of a Boolean
        container_framework = 'singularity' if singularity else 'docker'
        out = run_container(container_framework,
                            'agitter/local-neighborhood',
                            command,
                            volumes,
                            work_dir)
        print(out)

    @staticmethod
    def parse_output(raw_pathway_file, standardized_pathway_file):
        """
        Convert a predicted pathway into the universal format
        @param raw_pathway_file: pathway file produced by an algorithm's run function
        @param standardized_pathway_file: the same pathway written in the universal format
        """
        pathway_df = pd.read_csv(raw_pathway_file, sep='|')
        pathway_df['Rank'] = 1
        pathway_df.to_csv(standardized_pathway_file, header=False, index=False, sep=' ')
