import sqlite3
import csv

conn = sqlite3.connect('db.sqlite3')

respondents = conn.cursor()
respondents.execute('SELECT spreadsheet_row FROM poll_respondent')

questions = conn.cursor()
questions.execute('SELECT ua_heading FROM poll_question ORDER BY column_number')

with open('poll.csv', 'w') as csvfile:
    field_names = ["#"]
    for question in questions:
        if (question[0] not in field_names):
            field_names.append(question[0])
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    for respondent in respondents:
        row = {"#": respondent[0]}
        answers = conn.cursor()
        answers.execute('SELECT text, ua_heading FROM poll_answer JOIN poll_question ON poll_answer.question_id = poll_question.id WHERE respondent_id = %s ORDER BY poll_question.column_number' % respondent[0] )
        for text, ua_heading in answers:
            if ua_heading in row:
                row[ua_heading] += '"' + text + '"'
            else:
                row[ua_heading] = '"' + text + '"'
        writer.writerow(row)






