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
        description='A tool for refreshing CSV sources from google sheets')
    parser.add_argument(
        '-r', '--root', help='Root content directory', default=os.getcwd())
    parser.add_argument('-u', '--refresh',
                        help='Refresh upstream sources', action='store_true')
    parser.add_argument(
        '-l', '--look', help='Open oututs with quicklook', action='store_true')
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

        outputs = config['outputs']
        pdflatex = pydash.get(outputs, 'pdflatex')
        if pdflatex:
            print("Running LaTex to generate PDF...")
            utils.latex.run_latex(project_dir, project, pdflatex, args.look)

        print("Imposing PDFs...")
        if pydash.get(config, 'outputs.impositor.halfpage'):
            print("  * Creating half-page imposed version...")
            utils.impose(project_dir, project, booklet=False)
        if pydash.get(config, 'outputs.impositor.booklet'):
            print("  * Creating booklet imposed version...")
            utils.impose(project_dir, project, booklet=True)


if __name__ == '__main__':
    main()
