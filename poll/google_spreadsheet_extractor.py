import gspread
from .models import Question
from oauth2client.service_account import ServiceAccountCredentials

class SpreadSheetUpdater:

    def __init__(self, filename):
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(filename, scope)
        gc = gspread.authorize(credentials)
        self.spreadsheet = gc.open("Антикорупційне опитування")
        self.worksheet = self.spreadsheet.get_worksheet(0)

        #questions = Question.objects.all().order_by('number')

        #for i in range(len(questions)):
        #    if (self.worksheet.col_count == i+1):
        #        self.worksheet.add_cols(1)
        #    self._add_question(i+1, questions[i].ua_heading)

    def add_respondent(self, respondent_id):
        if (respondent_id+1 == self.worksheet.row_count):
            self.worksheet.add_rows(1)
        self.worksheet.update_cell(row=respondent_id+1, col=1, val=str(respondent_id))

    def add_answer(self, answer_text, question_id, respondent_id):
        self.worksheet.update_cell(row=respondent_id+1, col=question_id+1, val=answer_text)

    def _add_question(self, question_id, question_text):
        self.worksheet.update_cell(row=1, col=question_id+1, val=question_text)

#wks.share('tarasov@ucu.edu.ua', perm_type='user', role='writer')


#cell_list = worksheet.range('A1:C7')
#for cell in cell_list:
#    cell.value = "0))"

#worksheet.update_cells(cell_list)




