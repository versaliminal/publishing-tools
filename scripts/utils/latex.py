
from logging import config
import jinja2
import os
from pathlib import Path
import subprocess
from . import format
import pydash

PDF_DIR_FMT = '{project_dir}/pdf'
PDF_PATH_FMT = '{pdf_dir}/{project}.pdf'
LOG_PATH_FMT = '{pdf_dir}/{project}.log'
TMP_MAIN_FILE_FMT = '{project_dir}/{project}-{variant}.tex'

LATEX_ARGS_FMT = 'pdflatex,-interaction=nonstopmode,-output-directory={output_dir},{main_file}'


def run_latex(project_dir, project, config):
    """
    Runs pdflatex with configured inputs and optionally shows output for the project.
    """
    results = []
    pdf_dir = PDF_DIR_FMT.format(project_dir=project_dir)
    try:
        os.mkdir(pdf_dir)
    except FileExistsError:
        pass

    for variant in pydash.get(config, 'variants', []):
        format.print_subheader(
            "Running LaTex for variant: {0}".format(variant['name']))
        variant_main = template_main_file(
            project_dir, project, config['mainfile'], variant['name'], variant['class'])
        results.append(run_latex_cmd(
            project_dir, pdf_dir, Path(variant_main).name))
        os.remove(variant_main)

    return results


def run_latex_cmd(project_dir, pdf_dir, main_file):
    pdf_path = PDF_PATH_FMT.format(
        pdf_dir=pdf_dir, project=Path(main_file).stem)
    log_path = LOG_PATH_FMT.format(
        pdf_dir=pdf_dir, project=Path(main_file).stem)

    latex_args = LATEX_ARGS_FMT.format(
        output_dir=pdf_dir, main_file=main_file).split(',')
    result = subprocess.run(
        latex_args, cwd=project_dir, capture_output=True, text=True)
    if result.returncode != 0:
        format.print_item_notice("Completed with status {0}, check logs: {1}".format(
            result.returncode, log_path), indent=1)
    else:
        format.print_item_success(
            'Generated PDF: {0}'.format(pdf_path), indent=1)
    return pdf_path


def template_main_file(project_dir, project, main_file, variant_name, class_file):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(project_dir))
    template = env.get_template(main_file)
    output_file_path = TMP_MAIN_FILE_FMT.format(
        project_dir=project_dir, project=project, variant=variant_name)
    with open(output_file_path, 'w') as variant_main_file:
        variant_main_file.write(template.render(
            class_file="{" + class_file + "}"))
    return output_file_path
