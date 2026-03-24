#!python
import argparse
import shutil
import utils
import os
import pydash
from pathlib import Path
import yaml

PROJECT_DIR_FMT = '{root}/{project}'
CONFIG_FILE_FMT = '{content_root}/project.yaml'

PROJECT_STRUCTURE = [
    '{project}',
    '{project}/templates',
    '{project}/tables',
    '{project}/pdf',
    '{project}/rendered',
    '{project}/images',
]
PROJECT_EXAMPLES = [
    'fancy.cls',
    'printable.cls',
    'common.cls',
    'main.tex',
]


def read_conifg(content_root):
    """
    Reads the project config file.
    """
    config_file = CONFIG_FILE_FMT.format(content_root=content_root)
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
        errors = False
        for key in ['project', 'inputs', 'outputs']:
            if key not in config:
                utils.print_item_failure(
                    "Config file must contain a valid '{0}' entry".format(key))
                errors = True
        if errors:
            return None
        utils.print_item_success(
            "Loaded configuration for project: {0}".format(config['project']))
        return config


def main():
    """
    Implements main workflow.
    """
    parser = argparse.ArgumentParser(
        description='A tool for rendering rich documents from CSV sources')
    parser.add_argument(
        '-r', '--root', help='Root content directory', default=os.getcwd())
    parser.add_argument('-u', '--update',
                        help='Update sources from remote', action='store_true')
    parser.add_argument(
        '-i', '--init', help='Initialize a new project with the provided name')
    args = parser.parse_args()

    if args.init:
        utils.print_header(
            "Initializing new project: {0}...".format(args.init))
        for path_fmt in PROJECT_STRUCTURE:
            path = path_fmt.format(project=args.init)
            os.makedirs(path, exist_ok=True)
        utils.print_item_success("Created project structure")
        src_path = Path(__file__).parent / 'skel'
        dest = Path(args.init)
        for example in PROJECT_EXAMPLES:
            src = src_path / example
            dest = Path(args.init) / example
            shutil.copy(src, dest)
        utils.print_item_success("Initialized project with example tex files")
        utils.template_cp(src_path / 'project.yaml.template',
                          Path(args.root) / 'project.yaml', args.init)
        utils.print_item_success("Created example project.yaml file")
        return

    utils.print_header("Loading projects configuration...")
    config = read_conifg(args.root)
    if not config:
        utils.print_item_failure("Invalid project configuration")
        return
    project = config['project']
    project_dir = PROJECT_DIR_FMT.format(root=args.root, project=project)

    if args.update:
        utils.print_header("Refreshing sources...")
        utils.remote.refresh_sources(
            project_dir, pydash.get(config, 'inputs.remotes', {}))

    utils.print_header("Rendering templates...")
    utils.render_templates(project_dir, pydash.get(
        config, 'inputs.templates', []))

    pdfs = []
    pdflatex_config = pydash.get(config, 'outputs.pdflatex')
    if pdflatex_config:
        utils.print_header("Running LaTex to generate PDF...")
        pdfs.extend(utils.latex.run_latex(
            project_dir, project, pdflatex_config))

    results = []
    results.extend(pdfs)

    imposer_config = pydash.get(config, 'outputs.imposer')
    if imposer_config:
        for pdf in pdfs:
            utils.print_header("Imposing PDF {0}...".format(Path(pdf).name))
            results.extend(utils.imposer(pdf, imposer_config))

    if results:
        utils.print_header("Outputs:")
        for result in results:
            print("- {0}".format(result))
        print("")


if __name__ == '__main__':
    main()
