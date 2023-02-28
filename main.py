from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict
import argparse


def find_time(delta):
    years_count = str(delta)

    if len(years_count) == 0: return ''
    if len(years_count) > 1 and years_count[-2] == '1': return 'лет'

    words = {'0': 'лет', '1': 'год', '2': 'года', '3': 'года', '4': 'года', '5': 'лет', '6': 'лет', '7': 'лет',
             '8': 'лет', '9': 'лет'}
    return str(delta) + ' ' + words[years_count[-1]]


def read_excel_file(template) -> defaultdict:
    excel_data_df = pandas.read_excel(
        template, keep_default_na=False, na_values='', na_filter=False)
    sorted_drinks = excel_data_df.to_dict(orient="records")
    all_drink_items = defaultdict(list)
    for drinks in sorted_drinks:
        all_drink_items[drinks["Категория"]].append(drinks)
    return all_drink_items


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    start_time = datetime.datetime(year=1920, month=1, day=1)
    now_time = datetime.datetime.today()
    delta = now_time.year - start_time.year

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file_name',
        '-f',
        default='wine3.xlsx'
    )
    args = parser.parse_args()

    all_drinks = read_excel_file(args.file_name)

    rendered_page = template.render(
        year_now=delta,
        word=find_time(delta),
        all_drinks=all_drinks
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
