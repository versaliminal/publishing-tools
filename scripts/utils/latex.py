
import os
import subprocess

PDF_DIR_FMT = '{project_dir}/pdf'
PDF_PATH_FMT = '{project_dir}/pdf/{project}.pdf'


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
        print("  ! Completed with status {0}, check logs".format(
            result.returncode))
    else:
        print('  * completed successfully')

    return PDF_PATH_FMT.format(project_dir=project_dir, project=project)
