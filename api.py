# python3 -m venv .venv
# source .venv/bin/activate
# pip3 install -r requirements.txt
# python3 api.py
from google_play_scraper import app, reviews, Sort
import xlsxwriter
import datetime
import json

appIds = [
    "com.qiiwi.midsomermurders",
    "com.qiiwi.wordington",
    "com.qiiwi.hellskitchen",
    "com.qiiwi.backpacker",
    "com.qiiwi.coronationstreet",
    "com.qiiwi.kitchennightmares",
    "com.qiiwi.puzzleton",
    "com.qiiwi.magicgifts",
    "com.qiiwi.wiap2",
    "com.qiiwi.wordsinapic"
]


def main():
    data = get_data()
    # print(data)
    write_to_file(data)


def get_data():
    data = {}

    for appId in appIds:
        app_data = app(
            appId,
            # lang='en'
            # country='us',  # defaults to 'us'
        )

        app_reviews, token = reviews(
            appId,
            # lang='en',  # defaults to 'en'
            # country='us',  # defaults to 'us'
            sort=Sort.NEWEST,  # defaults to Sort.MOST_RELEVANT
            count=app_data['reviews'],  # defaults to 100
            # filter_score_with=5 # defaults to None(means all score)
            # continuation_token=None
        )

        reviews_history = {}
        tot_score = 0
        review_ratings = 0

        for i, review in enumerate(app_reviews):
            review_ratings += 1
            tot_score += review['score']
            date = review['at'].strftime("%y-%m")  # -%d

            if date not in reviews_history:
                reviews_history[date] = [0, 0]  # [Score, Num of reviews]

            reviews_history[date][0] += review['score']
            reviews_history[date][1] += 1

        # released = app_data['released']
        released = datetime.datetime.strptime(
            app_data['released'], "%b %d, %Y").strftime("%y-%m-%d")
        updated = datetime.datetime.fromtimestamp(
            app_data['updated']).strftime('%y-%m-%d')

        data[released] = {}
        data[released]['Title'] = app_data['title']
        data[released]['Released'] = released
        data[released]['Installs'] = app_data['minInstalls']
        data[released]['Ratings'] = app_data['ratings']
        data[released]['Score'] = round(app_data['score'], 3)
        data[released]['Score (reviews)'] = round(
            tot_score / review_ratings, 3)
        data[released]['Updated'] = updated
        data[released]['Reviews'] = reviews_history

        print(app_data['title'], "✓")

    return data


def write_to_file(data):
    workbook = xlsxwriter.Workbook('data.xlsx')
    sheet = workbook.add_worksheet()
    row_offset = 0
    col_offset = 5

    for col, (title, values) in enumerate(sorted(data.items(), reverse=True)):
        for row, (k, v) in enumerate(values.items()):
            if k == 'Reviews':
                for i, (date, score_n_ratings) in enumerate(v.items()):
                    r = row + row_offset + i
                    c = col + (col * col_offset)
                    avg_score_per_month = round(
                        score_n_ratings[0] / score_n_ratings[1], 3)
                    # avg_ratings_per_month = round(values['Ratings'] / len(v), 3)

                    # write(row, column, item)
                    sheet.write(r, c, date)
                    sheet.write(r, c + 1, score_n_ratings[0])
                    sheet.write(r, c + 2, score_n_ratings[1])
                    sheet.write(r, c + 3, avg_score_per_month)
                    sheet.write(r, c + 4, values['Score'])
                    # sheet.write(r, c + 5, avg_ratings_per_month)
                    # print(date, score_n_ratings)
            else:
                r = row + row_offset
                c = col + (col * col_offset)

                sheet.write(r, c, k)
                sheet.write(r, c + 1, v)
                # print('%s:' % k, v)

    workbook.close()


def print_data(data):
    for title, values in data.items():
        for k, v in values.items():
            if k == 'reviews':
                print('%s:' % k)
                print(json.dumps(v, indent=4, sort_keys=True))
            else:
                print('%s:' % k, v)

        print('='*50)


if __name__ == '__main__':
    main()
