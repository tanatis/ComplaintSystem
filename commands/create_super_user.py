import asyncclick as click

from db import database
from managers.user import UserManager
from models import RoleType


@click.command()
@click.option('-f', '--first_name', type=str, required=True)
@click.option('-l', '--last_name', type=str, required=True)
@click.option('-e', '--email', type=str, required=True)
@click.option('-p', '--phone', type=str, required=True)
@click.option('-i', '--iban', type=str, required=True)
@click.option('-pwd', '--password', type=str, required=True)
async def create_user(first_name, last_name, email, phone, iban, password):
    user_data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': phone,
        'iban': iban,
        'password': password,
        'role': RoleType.admin,
    }
    await database.connect()
    await UserManager.register(user_data)
    await database.disconnect()

'''
In terminal:
export PYTHONPATH=./  # or # set PYTHONPATH=./  
python commands/create_super_user.py -f Ime -l Familia -e admin@admin.com -p +359888123456 -i IBAN1234567890 -pwd 123
'''