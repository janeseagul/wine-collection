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
    sorted = excel_data_df.to_dict(orient="records")
    default_drinks = defaultdict(list)
    for drinks in sorted:
        default_drinks[drinks["Категория"]].append(drinks)
    return default_drinks



def main ():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    start_year = datetime.datetime(year=1920, month=1, day=1)
    year_now = datetime.datetime.today()
    delta = year_now.year - start_year.year

    all_products = read_excel_file("wine3.xlsx")
    excel_data_df = pandas.read_excel("wine.xlsx")

    rendered_page = template.render(
        year_now=delta,
        word=find_time(delta),
        all_products=all_products
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
