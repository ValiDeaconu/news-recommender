from flask import Flask, Blueprint
from server.database import api
from rich.console import Console

db_api = api.Api()
console = Console()