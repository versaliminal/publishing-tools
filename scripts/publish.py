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
    print("Loading projects file: {0}".format(config_file))
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
        errors = []
        for key in ['project', 'inputs', 'outputs']:
            if key not in config:
                errors.append(
                    "Config file must contain '{0}' section".format(key))
        if errors:
            raise ValueError("\n".join(errors))
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

    config = read_conifg(args.root)
    project = config['project']
    project_dir = PROJECT_DIR_FMT.format(root=args.root, project=project)
    print("Rendering: root={0}, project={1}".format(args.root, project))

    if args.refresh:
        print("Refreshing sources...")
        utils.remote.refresh_sources(
            project_dir, pydash.get(config, 'inputs.remotes', {}))

    print("Rendering templates...")
    utils.render_templates(project_dir, pydash.get(
        config, 'inputs.templates', []))

    results = []
    outputs = config['outputs']
    pdflatex_config = pydash.get(config, 'outputs.pdflatex')
    if pdflatex_config:
        print("Running LaTex to generate PDF...")
        results.append(utils.latex.run_latex(
            project_dir, project, pdflatex_config))

    imposer_config = pydash.get(config, 'outputs.imposer')
    if imposer_config:
        print("Imposing PDFs...")
        results.extend(utils.imposer(project_dir, project, imposer_config))

    if results:
        print("\nOutputs:")
        for result in results:
            print("  - {0}".format(result))
        print("")


if __name__ == '__main__':
    main()
