#!python
import argparse
import csv
import jinja2
import os
import re
import shutil
import urllib.request
import yaml

gsheets_url_format = '{url}/gviz/tq?tqx=out:csv&sheet={sheet}'

sheet_path_format = '{root}/tables/{project}/{sheet}.csv'
template_dir_format = '{root}/templates/{project}'
rendered_path_format = '{root}/rendered/{project}/{output}'

include_format = '\\include{{rendered/{output}}}\n'

yaml_tag = '(yaml)'

def read_conifg(filename, project):
    print("Loading projects file: {0}".format(filename))
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
        if project in config:
            return config[project]

def refresh_sources(root, project, config):
    project_dir = "{0}/tables/{1}".format(root, project)
    try:
        os.mkdir(project_dir)
    except FileExistsError:
        pass
    if not config['gsheets_url']:
        print("No remote configured, skipping refresh")
        return
    for entry in config['inputs']:
        url = gsheets_url_format.format(url=config['gsheets_url'], sheet=entry['sheet'])
        output = "{0}/{1}.csv".format(project_dir, entry['sheet'].lower())
        print("  * Downloading {0} sheet to {1}".format(entry['sheet'], output))
        try:
            urllib.request.urlretrieve(url, output)
        except Exception as e:
            print("\t- Error downloading file:", e)

def clear_rendered(root, project):
    project_dir = "{0}/rendered/{1}".format(root, project)
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
    os.mkdir(project_dir)

def jinja_to_latex_arg(content):
    if content and isinstance(content, str):
        return '{' + content + '}'
    else:
        return '{}'

def jinja_to_latex_args(*args):
    return "".join(map(jinja_to_latex_arg, args))

def populate_templates(content_root, project, config):
    for entry in config['inputs']:
        populate_template(content_root, project, entry['sheet'], entry['template'])

def populate_template(content_root, project, sheet_name, template_name):
    includes_file_path = rendered_path_format.format(root=content_root, project=project, output='includes.tex')
    includes_file = open(includes_file_path, 'a')

    sheet_file_path = sheet_path_format.format(root=content_root, project=project, sheet=sheet_name)
    with open(sheet_file_path, 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file)

        template_dir = template_dir_format.format(root=content_root, project=project)
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
        env.globals.update(arg=jinja_to_latex_arg, args=jinja_to_latex_args)
        template = env.get_template(template_name)

        for row in reader:
            output_file_name = "{0}-{1}.tex".format(row['Number'], row['Name'])
            output_file_path = rendered_path_format.format(root=content_root, project=project, output=output_file_name)
            
            includes_file.write(include_format.format(output=output_file_name))
            print("  * Populating {0}".format(output_file_name))
            with open(output_file_path, 'w') as tex_file:
                parsed_cols = {}
                for k, v in row.items():
                    if not v:
                        continue
                    if k.endswith(yaml_tag):
                        name = k.replace(yaml_tag, '').strip()
                        parsed_cols[name] = yaml.safe_load(v)
                        print("Parsed table: {0}".format(parsed_cols[name]))
                tex_file.write(template.render(raw=row, parsed=parsed_cols))
        includes_file.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A tool for refreshing CSV sources from google sheets')
    parser.add_argument('project', help='Project name')
    parser.add_argument('--root', help='Root content directory', default=os.getcwd())
    parser.add_argument('--refresh', help='Refresh upstream sources', action='store_true')
    args = parser.parse_args()
    print("Rendering: root={0}, project={1}".format(args.root, args.project))
    
    content_root="{0}/content".format(args.root)
    config_file = "{0}/projects.yaml".format(content_root)
    config = read_conifg(config_file, args.project)
    print("Config={0}".format(config))

    if args.refresh:
        print("Refreshing sources...")
        refresh_sources(content_root, args.project, config)
    
    clear_rendered(content_root, args.project)
    populate_templates(content_root, args.project, config)

    

    
    

