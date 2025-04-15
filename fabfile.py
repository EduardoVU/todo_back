# fabfile.py

from fabric import task

@task
def run_dev(c):
    c.run('uvicorn main:app --reload --port 3000')

@task
def install(c):
    c.run('pip install -r requirements.txt')
    c.run('pip freeze > requirements.txt')
