class TemplateOption:

    def __init__(self, option, language):

        if (language == "UA"):
            self.text = option.ua_text
        elif (language == "RU"):
            self.text = option.ru_text


class TemplateQuestion:

    def __init__(self, question, templateOptions, language):

        if (language == "UA"):
            self.heading = question.ua_heading
            self.text = question.ua_text
        elif (language == "RU"):
            self.heading = question.ru_heading
            self.text = question.ru_text

        self.id = question.id
        self.type = question.type
        self.options = templateOptions


class TemplatePage:

    def __init__(self, page, language):

        if (language == "UA"):
            self.title = page.ua_title
            self.heading = page.ua_heading
            self.text = page.ua_text
        elif (language == "RU"):
            self.title = page.ru_title
            self.heading = page.ru_heading
            self.text = page.ru_text

        self.type = page.type
        self.number = page.number

class TemplateVideo:

    def __init__(self, video):

        self.url = video.url