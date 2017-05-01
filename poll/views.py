# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.views.defaults import page_not_found, permission_denied, server_error
from django.http import HttpResponseRedirect, HttpResponse
from wsgiref.util import FileWrapper
from django.conf import settings
from .models import *
from .templates import *
from .google_spreadsheet_extractor import SpreadSheetUpdater
from .forms import FormWithCaptcha
from static.poll.scripts.export_all import export
import random
import os
import time
import csv
import sys

# Create your views here.
spreadsheet_updater = SpreadSheetUpdater(filename=os.path.join(settings.STATICFILES_DIRS[0], 'poll/client_secret.json'))

def csv_download(request):
    export()
    wrapper = open(os.path.join(settings.STATICFILES_DIRS[0], 'poll/poll.csv'), 'r' , encoding='cp1251')
    response = HttpResponse(content_type='text/csv; charset=windows-1251')
    response['Content-Disposition'] = "attachment; filename=results_of_poll.csv"


    reader = csv.reader(wrapper)
    writer = csv.writer(response)

    for row in reader:
        writer.writerow(row)

    return response

def skip_not_needed_pages(respondent):
    page = Page.objects.get(number=respondent.page)
    conditions = Condition.objects.filter(page=page)

    # check if all of conditions are met. if not - skip page
    for condition in conditions:
        # if respondent chose some language then his answers in this language
        if (respondent.language == "RU"):
            option_text = condition.option.ru_text
        elif (respondent.language == "UA"):
            option_text = condition.option.ua_text

        answers = Answer.objects.filter(respondent=respondent,
                                        question=condition.option.question,
                                        text=option_text)
        if len(answers) == 0:
            respondent.page += 1
            respondent.save()
            return True
    # if all conditions are met it is not needed to skip page
    return False


def get_context(respondent):
    # get information from database
    db_page = Page.objects.get(number=respondent.page)
    db_videos = Video.objects.filter(page=db_page)
    db_questions = Question.objects.filter(page=db_page).order_by('number')

    # prepare information for template
    template_page = TemplatePage(db_page, respondent.language)

    if (len(db_videos) > 0):
        template_video = TemplateVideo(random.choice(db_videos))
    else:
        template_video = None


    template_questions = []
    # here we prepare questions and options for it
    for db_question in db_questions:
        db_options = Option.objects.filter(question=db_question)
        template_options = [TemplateOption(db_option, respondent.language) for db_option in db_options]
        print(template_options)
        template_questions.append(TemplateQuestion(db_question, template_options, respondent.language))

    context = {
        "page": template_page,
    }

    if (db_page.type in ["Question", "Lottery"]):
        context["questions"] = template_questions
    if (db_page.type in ["Starting"]):
        context["captcha_form"] = FormWithCaptcha()
    if (db_page.type in ["Video"]):
        context["video"] = template_video
        video_answer = Answer(question=db_questions.get(id=78),
                              respondent=respondent,
                              text=template_video.key_name)
        video_answer.save()
        spreadsheet_updater.add_answer(template_video.key_name,
                                       db_questions.get(id=78).id,
                                       respondent.spreadsheet_row)

    if (db_page.type in ["Lottery"]):
        context["lottery_number"] = respondent.lottery_number
        context["lottery_case"] = random.choice(["both", "generation", "manual"])
        type_of_page_question = Question.objects.get(id=90)
        type_of_page = Answer(respondent=respondent,
                              question= type_of_page_question,
                              text=context["lottery_case"]
                              )
        type_of_page.save()
        spreadsheet_updater.add_answer(context["lottery_case"],
                                       type_of_page_question.id,
                                       respondent.spreadsheet_row)

    return context, db_page.type


def get_page(request):

    if (request.session.session_key is None):
        request.session.save()

    try:
        # try to get this respondent information
        respondent = Respondent.objects.get(identity=request.session.session_key)
    except:
        # generate unique lottery number first
        lottery_number = ""
        for i in range(10):
            lottery_number += random.choice('0123456789')

        while Respondent.objects.filter(lottery_number=lottery_number).count() != 0:
            lottery_number = ""
            for i in range(10):
                lottery_number += random.choice('0123456789')

        # create session in db
        respondent = Respondent(identity=request.session.session_key, page=1, lottery_number=lottery_number)
        respondent.save()
        spreadsheet_updater.add_respondent(respondent.spreadsheet_row)


    # skip pages until the one respondent should see
    while skip_not_needed_pages(respondent):
        pass

    context, page_type = get_context(respondent)

    if (page_type == "Starting"):
        return render(request, "Starting.html", context=context)
    elif (page_type == "Login"):
        get_time = str(time.asctime(time.localtime(time.time())))
        question_time = Question.objects.get(id=87)
        get_time_answer = Answer(respondent=respondent,
                          question=question_time,
                          text= get_time)
        get_time_answer.save()
        spreadsheet_updater.add_answer(str(get_time), question_time.id, respondent.spreadsheet_row)
        return render(request, "Login.html", context=context)
    elif (page_type == "Question"):
        return render(request, "Question.html", context=context)
    elif (page_type == "Video"):
        return render(request, "Video.html", context=context)
    elif (page_type == "Lottery"):
        return render(request, "Lottery.html", context=context)
    elif (page_type == "FinalPage"):
        return render(request, "FinalPage.html", context=context)
    else:
        return page_not_found(request)


def post_answer(request):
    respondent = get_object_or_404(Respondent, identity=request.session.session_key)
    #try:
    page = Page.objects.get(number=respondent.page)
    questions = Question.objects.filter(page=page)
    if (page.type == "Lottery"):
        coins = "Null"
        if ("Generate" in request.COOKIES and request.COOKIES["Generate"]=="true"):
            coins = 0
            for i in range(10):
                if (str(i+1) in request.POST and request.POST[str(i+1)] == "on"):
                    coins += 1

        user_coins = request.POST["heads_size"]


        question_lottery_coins = questions.get(id=86)
        question_user_coins = questions.get(id=89)
        question_lottery_number = questions.get(id=75)
        lottery_coins = Answer(respondent = respondent,
                               question=question_lottery_coins,
                               text=coins)
        lottery_coins.save()

        user_db_coins = Answer(respondent = respondent,
                               question = question_user_coins,
                               text = user_coins)
        user_db_coins.save()

        lottery_number_db = Answer(respondent = respondent,
                                   question = question_lottery_number,
                                   text = str(respondent.lottery_number))
        lottery_number_db.save()

        spreadsheet_updater.add_answer(user_coins,question_user_coins.id, respondent.spreadsheet_row)
        spreadsheet_updater.add_answer(str(coins), question_lottery_coins.id, respondent.spreadsheet_row)
        spreadsheet_updater.add_answer(str(respondent.lottery_number), question_lottery_number.id, respondent.spreadsheet_row)

    elif (page.type == "Login"):
        post_time = str(time.asctime(time.localtime(time.time())))
        question_time = Question.objects.get(id=88)
        post_time_answer = Answer(respondent=respondent,
                          question=question_time,
                          text= post_time)
        post_time_answer.save()
        spreadsheet_updater.add_answer(str(post_time), question_time.id, respondent.spreadsheet_row)
        if "Like" in request.COOKIES:
            text_like = request.COOKIES["Like"]
        else:
            text_like = "FALSE"
        question_like = questions.get(ua_heading="Лайкнув")
        answer_like = Answer(respondent=respondent,
                             question=question_like,
                             text=text_like)
        answer_like.save()
        spreadsheet_updater.add_answer(str(text_like), question_like.id, respondent.spreadsheet_row)
        #shared = request.POST["Shared"] == "true"
    else:
        if (page.type == "Starting"):
            form = FormWithCaptcha(request.POST)
            if not form.is_valid():
                return HttpResponseRedirect('/poll/')
    # one page could contain several questions
        for question in questions:
         # some questions could have several answers
            user_answer = request.POST.getlist(str(question.id))
            print(question.id)
            spreadsheet_updater.add_answer(str(user_answer), question.id, respondent.spreadsheet_row)
            for option in user_answer:
                # allow user to choose preferred language
                if (question.type=="LanguageChoosing"):
                    respondent.language = {"Русский": "RU", "Українська": "UA"}[option]

                # save answer in database
                db_answer = Answer(respondent=respondent, question=question, text=option)
                db_answer.save()

    respondent.page += 1
    respondent.save()
    return HttpResponseRedirect('/poll/')
    #except:
    #    return server_error(request)


