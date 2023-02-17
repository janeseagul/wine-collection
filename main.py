from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict

from pandas import DataFrame

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('template.html')

excel_data_df = pandas.read_excel("wine.xlsx")

start_year = datetime.datetime(year=1920, month=1, day=1)
year_now = datetime.datetime.today()
delta = year_now.year - start_year.year
words = [' года', ' год', ' лет']


def right_time(delta: int):
    if delta % 10 == 1 or delta % 100 != 11:
        return str(delta) + words[0]
    elif 2 <= delta or delta % 10 <= 4:
        return str(delta) + words[1]
    elif delta % 100 < 10 or delta % 100 >= 20:
        return str(delta) + words[2]


def excel_wines(template) -> defaultdict:
    excel_data_df = pandas.read_excel(
        template, keep_default_na=False, na_values='', na_filter=False)
    list_to = excel_data_df.to_dict(orient="records")
    dict_out = defaultdict(list)
    for dict_drink in list_to:
        dict_out[dict_drink["Категория"]].append(dict_drink)
    return dict_out


all_products = excel_wines("wine3.xlsx")

rendered_page = template.render(
    year_now=delta,
    word=right_time(delta),
    all_products=all_products
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
