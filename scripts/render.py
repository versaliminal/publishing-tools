#!python
import argparse
import csv
import jinja2
import os
import shutil
import subprocess
import urllib.request
import yaml

GSHEETS_URL_FMT = '{url}/gviz/tq?tqx=out:csv&sheet={sheet}'

PROJECT_DIR_FMT = '{root}/{project}'
TABLE_PATH_FMT = '{project_dir}/tables/{table}'
TEMPLATE_PATH_FMT = '{project_dir}/templates/{template}'
RENDERED_PATH_FMT = '{project_dir}/rendered/{output}'
PDF_DIR_FMT = '{project_dir}/pdf'
INCLUDES_FILE = 'includes.tex'
CONFIG_FILE_FMT = '{content_root}/projects.yaml'

INCLUDE_FMT = '\\input{{rendered/{output}}} \clearpage\n'

YAML_TAG = '(yaml)'

def read_conifg(content_root, project):
    config_file = CONFIG_FILE_FMT.format(content_root=content_root)
    print("Loading projects file: {0}".format(config_file))
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
        if project in config:
            return config[project]

def refresh_sources(project_dir, config):
    try:
        os.mkdir(project_dir)
        os.mkdir(TABLE_PATH_FMT.format(""))
    except FileExistsError:
        pass
    if not config['gsheets_url']:
        print("No remote configured, skipping refresh")
        return
    for entry in config['mappings']:
        url = GSHEETS_URL_FMT.format(url=config['gsheets_url'], sheet=entry['sheet'])
        output = TABLE_PATH_FMT.format(project_dir=project_dir, table=entry['table'])
        print("  * Downloading {0} sheet to {1}".format(entry['sheet'], output))
        try:
            urllib.request.urlretrieve(url, output)
        except Exception as e:
            print("\t- Error downloading file:", e)

def clear_rendered(project_dir):
    rendered_dir = RENDERED_PATH_FMT.format(project_dir=project_dir, output="")
    if os.path.exists(rendered_dir):
        shutil.rmtree(rendered_dir)
    os.mkdir(rendered_dir)

def jinja_to_latex_arg(content):
    if content:
        if isinstance(content, int):
            content = str(content)
        if isinstance(content, str):
            return '{' + content + '}'
    return '{}'

def jinja_to_latex_args(*args):
    return "".join(map(jinja_to_latex_arg, args))

def render_templates(project_dir, config):
    for entry in config['mappings']:
        render_template(project_dir, entry['table'], entry['template'])

def render_template(project_dir, table_name, template_name):
    includes_file_path = RENDERED_PATH_FMT.format(project_dir=project_dir, output=INCLUDES_FILE)
    includes_file = open(includes_file_path, 'a')

    table_file_path = TABLE_PATH_FMT.format(project_dir=project_dir, table=table_name)
    with open(table_file_path, 'r', newline='') as table_file:
        reader = csv.DictReader(table_file)

        template_dir = TEMPLATE_PATH_FMT.format(project_dir=project_dir, template="")
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
        env.globals.update(arg=jinja_to_latex_arg, args=jinja_to_latex_args)
        template = env.get_template(template_name)

        for row in reader:
            output_file_name = "{0}-{1}.tex".format(row['Number'], row['Name'])
            output_file_path = RENDERED_PATH_FMT.format(project_dir=project_dir, output=output_file_name)
            
            includes_file.write(INCLUDE_FMT.format(output=output_file_name))
            print("  * Rendering {0}".format(output_file_name))
            with open(output_file_path, 'w') as tex_file:
                parsed_cols = {}
                for k, v in row.items():
                    if not v:
                        continue
                    if k.endswith(YAML_TAG):
                        name = k.replace(YAML_TAG, '').strip()
                        parsed_cols[name] = yaml.safe_load(v)
                tex_file.write(template.render(raw=row, parsed=parsed_cols))
        includes_file.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A tool for refreshing CSV sources from google sheets')
    parser.add_argument('project', help='Project name')
    parser.add_argument('--root', help='Root content directory', default=os.getcwd())
    parser.add_argument('--refresh', help='Refresh upstream sources', action='store_true')
    args = parser.parse_args()
    print("Rendering: root={0}, project={1}".format(args.root, args.project))
    
    content_root="{0}/projects".format(args.root)
    
    config = read_conifg(content_root, args.project)
    project_dir = PROJECT_DIR_FMT.format(root=content_root, project=args.project)

    if args.refresh:
        print("Refreshing sources...")
        refresh_sources(project_dir, config)
    
    clear_rendered(project_dir)
    print("Rendering templates...")
    render_templates(project_dir, config)

    outputs = config['outputs']
    if outputs['latex']:
        print("Running LaTex...")
        try:
            os.mkdir(PDF_DIR_FMT.format(project_dir=project_dir))
        except FileExistsError:
            pass
        args = ['pdflatex', '-interaction=nonstopmode', '-output-directory=pdf']
        result = subprocess.run(args + outputs['latex']['includes'], cwd=project_dir, capture_output=True, text=True)
        if result.returncode != 0:
            print("  ! Completed with status {0}, check logs".format(result.returncode))
        else:
            print('  * completed successfully')

    

    
    

