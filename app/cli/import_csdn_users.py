import click
from flask.cli import with_appcontext
from app.utils.import_csdn_users import import_csdn_users

@click.command('import-csdn-users')
@with_appcontext
def import_csdn_users_command():
    """从static/csdn.csv导入CSDN用户数据"""
    result = import_csdn_users()
    click.echo(result)
