# ttrpg-tools
Tools for managing and publishing content for Table-Top Roleplaying Games (TTRPGs)

Rendered examples:
 [Example PDF](docs/examples/example.pdf)  

# Setup
## Python environment
To create a valid python environment run the follwoing:
1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r scripts/requirements.txt`

# Creating a new project
1. Create your templates under projects/{project_name}/templates/
2. Create your source tables under projects/{project_name}/tables/ (you may skip this if you want to refresh from gsheets)
3. Update the projects.yaml file to include your project resources

# Rendering your project
Run the render script (add `--refresh` to refresh sources)
`scripts/render.py content {project-name}`
Rendered templates will be found under content/rendered