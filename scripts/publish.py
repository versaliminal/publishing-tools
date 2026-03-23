#!python
import argparse
import utils
import os
import pydash
import yaml

PROJECT_DIR_FMT = '{root}/{project}'
CONFIG_FILE_FMT = '{content_root}/project.yaml'


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
    parser.add_argument('-u', '--refresh',
                        help='Refresh upstream sources', action='store_true')
    args = parser.parse_args()

    utils.print_header("Loading projects configuration...")
    config = read_conifg(args.root)
    if not config:
        utils.print_item_failure("Invalid project configuration")
        return
    project = config['project']
    project_dir = PROJECT_DIR_FMT.format(root=args.root, project=project)

    if args.refresh:
        utils.print_header("Refreshing sources...")
        utils.remote.refresh_sources(
            project_dir, pydash.get(config, 'inputs.remotes', {}))

    utils.print_header("Rendering templates...")
    utils.render_templates(project_dir, pydash.get(
        config, 'inputs.templates', []))

    results = []
    pdflatex_config = pydash.get(config, 'outputs.pdflatex')
    if pdflatex_config:
        utils.print_header("Running LaTex to generate PDF...")
        results.append(utils.latex.run_latex(
            project_dir, project, pdflatex_config))

    imposer_config = pydash.get(config, 'outputs.imposer')
    if imposer_config:
        utils.print_header("Imposing PDFs...")
        results.extend(utils.imposer(project_dir, project, imposer_config))

    if results:
        utils.print_header("Outputs:")
        for result in results:
            print("- {0}".format(result))
        print("")


if __name__ == '__main__':
    main()
