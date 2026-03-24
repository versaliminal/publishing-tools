import csv
import jinja2
import os
import shutil
import yaml
from . import format

TABLE_PATH_FMT = '{project_dir}/tables/{table}'
TEMPLATE_PATH_FMT = '{project_dir}/templates/{template}'
RENDERED_PATH_FMT = '{project_dir}/rendered/{output}'
INCLUDES_FILE = 'includes.tex'

INCLUDE_FMT = '\\input{{rendered/{output}}} \\clearpage\n'
YAML_TAG = '(yaml)'


def clear_rendered(project_dir):
    """
    Destroys and re-creates the rendered directory.
    """
    rendered_dir = RENDERED_PATH_FMT.format(project_dir=project_dir, output="")
    if os.path.exists(rendered_dir):
        shutil.rmtree(rendered_dir)
    os.mkdir(rendered_dir)


def jinja_to_latex_arg(content):
    """
    Formats a single argument as a latex argument (string, int, or float only).
    """
    if content:
        if isinstance(content, int) or isinstance(content, float):
            content = str(content)
        if isinstance(content, str):
            return '{' + content + '}'
    return '{}'


def jinja_to_latex_args(*args):
    """
    Formats any number of arguments as latex arguments.
    """
    return "".join(map(jinja_to_latex_arg, args))


def render_templates(project_dir, config):
    """
    Runs all table and template mappings.
    """
    templates_dir = TEMPLATE_PATH_FMT.format(
        project_dir=project_dir, template="")

    clear_rendered(project_dir)
    includes_file_path = RENDERED_PATH_FMT.format(
        project_dir=project_dir, output=INCLUDES_FILE)
    with open(includes_file_path, 'w') as includes_file:
        for entry in config.get('mappings', []):
            table_file_path = TABLE_PATH_FMT.format(
                project_dir=project_dir, table=entry['table'])
            render_template(project_dir, table_file_path,
                            templates_dir, entry['template'], includes_file)


def render_template(project_dir, table_file_path, template_dir, template_name, includes_file):
    """
    Runs the specified template for every row in the specified table.
    """
    with open(table_file_path, 'r', newline='') as table_file:
        reader = csv.DictReader(table_file)

        env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
        env.globals.update(arg=jinja_to_latex_arg, args=jinja_to_latex_args)
        template = env.get_template(template_name)

        for row in reader:
            if row['Render'] == 'FALSE':
                format.print_item_notice("Skipping {0} because Render is FALSE".format(
                    row['Name']))
                continue

            output_file_name = "{0}-{1}.tex".format(
                row['Number'], row.get('Name', '').replace(" ", "_"))
            output_file_path = RENDERED_PATH_FMT.format(
                project_dir=project_dir, output=output_file_name)

            includes_file.write(INCLUDE_FMT.format(output=output_file_name))
            format.print_item_success("Rendering {0}".format(output_file_name))
            with open(output_file_path, 'w') as tex_file:
                parsed_cols = {}
                for k, v in row.items():
                    if not v:
                        continue
                    if k.endswith(YAML_TAG):
                        name = k.replace(YAML_TAG, '').strip()
                        parsed_cols[name] = yaml.safe_load(v)
                tex_file.write(template.render(raw=row, parsed=parsed_cols))


def template_cp(src, dest, project):
    """
    Renders a single template file to the specified destination.
    """
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(src.parent))
    template = env.get_template(src.name)
    with open(dest, 'w') as dest_file:
        dest_file.write(template.render(project=project))
