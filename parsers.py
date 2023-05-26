import json
import time

import requests
import datetime
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

start_time = time.time()


def get_date():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    with open(f"ulprospector_{cur_time}.csv", "w") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
            "Название",
            "Производитель",
            "INCI",
            "Описание"
            )
        )
    headers = {"User-Agent": UserAgent().random}

    url = "https://www.ulprospector.com/en/na/PersonalCare/Product/search?start=1000"
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    pages_count = int(soup.find("ul", class_="pagination").find_all("li", class_="goto-page")[-1].text)
    names_data = []

    for page in range(1, pages_count + 100):
        url = f"https://www.ulprospector.com/en/na/PersonalCare/Product/search?start={page}"
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        names_table = soup.find("tbody").find_all("tr", class_="result_detail_row_bordered")
        for bi in names_table:
            name_data = bi.find_all("td")
            try:
                name_title = name_data[0].find("a").text.strip()
            except:
                name_title = "хз мне не платили"
            try:
                name_prod = name_data[1].text.strip()
            except:
                name_prod = "хз мне не платили"
            try:
                name_inci = name_data[2].text.strip()
            except:
                name_inci = "хз мне не платили"
            try:
                name_op = name_data[3].text.strip()
            except:
                name_op = "хз мне не платили"
            #print(name_title)
            #print(name_prod)
            #print(name_inci)
            #print(name_op)
            #print("#"*10)

            names_data.append(
                {
                    "name_title" : name_title,
                    "name_prod" : name_prod,
                    "name_inci" : name_inci,
                    "name_op" : name_op
                }
            )

            with open(f"ulprospector_{cur_time}.csv", "a") as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        name_title,
                        name_prod,
                        name_inci,
                        name_op
                    )
                )
        print(f"Обработана {page}/{pages_count}")
        time.sleep(1)
    with open(f"labirint_{cur_time}.json", "w") as file:
        json.dump(name_data,file, indent=4, ensure_ascii=False)


def main():
    get_date()
    finish_time = time.time() - start_time
    print(f"Затрачено времени :  {finish_time}")


if __name__ == '__main__':
    main()
