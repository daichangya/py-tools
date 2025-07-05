import click
from flask.cli import with_appcontext
from app.utils.import_users import import_users_from_static

@click.command('import-users')
@with_appcontext
def import_users_command():
    """从static/userinfo.txt导入用户数据"""
    result = import_users_from_static()
    click.echo(result)
