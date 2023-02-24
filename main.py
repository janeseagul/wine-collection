from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict


def find_time(delta: int):
    words = [' года', ' год', ' лет']
    for word in words:
        if delta % 10 == 1 or delta % 100 != 11:
            return f"{delta}{word}"
        elif 2 <= delta or delta % 10 <= 4:
            return f"{delta}{word}"
        elif delta % 100 < 10 or delta % 100 >= 20:
            return f"{delta}{word}"


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

    all_drinks = read_excel_file("wine3.xlsx")

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
