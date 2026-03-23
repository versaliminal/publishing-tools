
import os
import subprocess
from . import format

PDF_DIR_FMT = '{project_dir}/pdf'
PDF_PATH_FMT = '{project_dir}/pdf/{project}.pdf'
LOG_PATH_FMT = '{project_dir}/pdf/{project}.log'


def run_latex(project_dir, project, config):
    """
    Runs pdflatex with configured inputs and optionally shows output for the project.
    """
    try:
        os.mkdir(PDF_DIR_FMT.format(project_dir=project_dir))
    except FileExistsError:
        pass
    latex_args = ['pdflatex', '-interaction=nonstopmode',
                  '-output-directory=pdf']
    result = subprocess.run(
        latex_args + config['includes'], cwd=project_dir, capture_output=True, text=True)
    if result.returncode != 0:
        format.print_item_notice("Completed with status {0}, check logs: {1}".format(
            result.returncode, LOG_PATH_FMT.format(project_dir=project_dir, project=project)))
    else:
        format.print_item_success('Generated PDF', indent=1)

    return PDF_PATH_FMT.format(project_dir=project_dir, project=project)
