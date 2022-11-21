from pathlib import Path

from envyaml import EnvYAML

BASE_DIR = Path(__name__).resolve().parent
env = EnvYAML(f'{BASE_DIR}/fastapi_template/app/configs/env.yaml')


class ProjectSettings:
    title = env['project.title']
    host = env['project.host']
    port = env['project.port']
    root_path = env['project.root-path']
    version = env['project.version']
    debug = env['project.debug']


class DBSettings:
    host = env['database.host']
    port = env['database.port']
    username = env['database.username']
    password = env['database.password']
    name = env['database.name']
    schema = env['database.schema']
    config = f"postgresql+asyncpg://{username}:{password}@{host}/{name}"


class JWTSettings:
    secret_key = env['auth.secret-key']
    algo = env['auth.algorithm']
