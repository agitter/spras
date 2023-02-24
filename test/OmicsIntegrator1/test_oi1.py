import pytest
import shutil
import subprocess
from pathlib import Path
from src.omicsintegrator1 import OmicsIntegrator1, write_conf
from src.util import compare_files

TEST_DIR = 'test/OmicsIntegrator1/'
OUT_FILE = TEST_DIR+'output/test_optimalForest.sif'


class TestOmicsIntegrator1:
    """
    Run Omics Integrator 1 in the Docker image
    """
    def test_oi1_required(self):
        out_path = Path(OUT_FILE)
        out_path.unlink(missing_ok=True)
        # Only include required arguments
        OmicsIntegrator1.run(edges=TEST_DIR+'input/oi1-edges.txt',
                             prizes=TEST_DIR+'input/oi1-prizes.txt',
                             output_file=OUT_FILE,
                             w=5,
                             b=1,
                             d=10)
        assert out_path.exists()

    def test_oi1_some_optional(self):
        out_path = Path(OUT_FILE)
        out_path.unlink(missing_ok=True)
        # Include optional argument
        OmicsIntegrator1.run(edges=TEST_DIR+'input/oi1-edges.txt',
                             prizes=TEST_DIR+'input/oi1-prizes.txt',
                             output_file=OUT_FILE,
                             w=5,
                             b=1,
                             d=10,
                             noise=0.333,
                             g=0.001,
                             r=0)
        assert out_path.exists()

    def test_oi1_all_optional(self):
        out_path = Path(OUT_FILE)
        out_path.unlink(missing_ok=True)
        # Include all optional arguments
        OmicsIntegrator1.run(edges=TEST_DIR+'input/oi1-edges.txt',
                             prizes=TEST_DIR+'input/oi1-prizes.txt',
                             dummy_mode='terminals',
                             mu_squared=True,
                             exclude_terms=True,
                             output_file=OUT_FILE,
                             noisy_edges=0,
                             shuffled_prizes=0,
                             random_terminals=0,
                             seed=1,
                             w=5,
                             b=1,
                             d=10,
                             mu=0,
                             noise=0.333,
                             g=0.001,
                             r=0)
        assert out_path.exists()

    def test_oi1_missing(self):
        # Test the expected error is raised when required arguments are missing
        with pytest.raises(ValueError):
            # No edges
            OmicsIntegrator1.run(prizes=TEST_DIR + 'input/oi1-prizes.txt',
                                 output_file=TEST_DIR+'output/test_optimalForest.sif',
                                 w=5,
                                 b=1,
                                 d=10)
        with pytest.raises(ValueError):
            # No w
            write_conf(Path('.'),
                       b=1,
                       d=10)

    # Only run Singularity test if the binary is available on the system
    # spython is only available on Unix, but do not explicitly skip non-Unix platforms
    @pytest.mark.skipif(not shutil.which('singularity'), reason='Singularity not found on system')
    def test_oi1_singularity(self):
        out_path = Path(OUT_FILE)
        out_path.unlink(missing_ok=True)
        # Only include required arguments and run with Singularity
        OmicsIntegrator1.run(edges=TEST_DIR + 'input/oi1-edges.txt',
                             prizes=TEST_DIR + 'input/oi1-prizes.txt',
                             output_file=OUT_FILE,
                             w=5,
                             b=1,
                             d=10,
                             singularity=True)
        assert out_path.exists()

    def test_oi1_snakemake_directed(self):
        """
        Run Omics Integrator 1 through Snakemake and confirm the output on a directed test case matches the expected
        output. Check the raw pathway because the SPRAS processed pathway does not track directed edges.
        @return:
        """
        out_pathway = 'dir-data-omicsintegrator1-params-UJLAW7A/raw-pathway.txt'
        generated_pathway = 'output/' + out_pathway
        Path(generated_pathway).unlink(missing_ok=True)
        Path(generated_pathway.replace('raw-', '')).unlink(missing_ok=True)

        # Run Snakemake in a subprocess with the directed config file
        subprocess.run(['snakemake', '--cores', '1', '--configfile', 'config/dir-config.yaml'])
        expected_pathway = TEST_DIR + 'expected/' + out_pathway

        assert compare_files(generated_pathway, expected_pathway), f'{generated_pathway} and {expected_pathway} do not match'
