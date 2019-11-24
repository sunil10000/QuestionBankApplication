import os
import sys
from .models import QuizPaper, Question, QuestionModule


def generate_quiz(quizpaperid, title):
    f = open("Quiz.tex", "w+")
    header = title
    j = 1
    print("hi")
    f.close()
    with open("Quiz.tex", "w+") as f:

        def questionadd(questid):
            print("inside question")
            ques = Question.objects.get(pk=questid)
            statement = str(ques.statement).replace(" ", r" \ ").replace("_", "-")
            marks = ques.marks
            f.write("\\item \seqsplit{" + statement + "}\\hfill\n")
            f.write("[" + str(marks) + " Marks]" + "\n")
            f.write(r"\\Solution:\\ ")
            f.write(r"\vspace*{" + str((marks * 20)) + "pt}")

        def questionmodule(moduleid):
            print("inside question module")
            quesmodule = QuestionModule.objects.get(pk=moduleid)
            statement = str(quesmodule.statement).replace(" ", r" \ ").replace("_", "-")
            marks = quesmodule.marks
            f.write("\\item \seqsplit{" + statement + "}\\hfill\n")
            f.write("[" + str(marks) + " Marks]" + "\n")
            questionidlist = Question.objects.filter(parent=quesmodule.id, isRoot=0)
            questionmoduleidlist = QuestionModule.objects.filter(parent=quesmodule.id, isRoot=0)
            f.write("\\begin{enumerate}")
            for ques in questionidlist:
                questionadd(ques.id)
            for quesmod in questionmoduleidlist:
                questionmodule(quesmod.id)
            f.write("\\end{enumerate}\n")

        # adding template
        f.write("\\documentclass[10pt]{article}\n")
        f.write("\\usepackage[a4paper,bottom = 0.6in,left = 0.75in,right = 0.75in,top = 0.6in]{geometry}\n")
        f.write("\\usepackage{seqsplit}")
        f.write("\\begin {document}\n")
        f.write("\\vspace*{2cm}\n")

        f.write("\\begin{center}\n")
        f.write(header+"\n")
        f.write("\\"+"\\")
        f.write("\\vspace*{1cm}\n")
        quiz = QuizPaper.objects.get(pk=quizpaperid)
        qidlist = list(quiz.qid_list.split(","))[1:]
        qmidlist = list(quiz.qmid_list.split(","))[1:]
        f.write("\\begin{tabular}{|c|c|}\n")
        f.write("\\hline ")

        # create table
        for q in qidlist:
            quizmarks = Question.objects.get(pk=q).marks
            f.write("Q"+str(j)+" & "+str(quizmarks)+" \\"+"\\ ")
            j = j+1
            f.write("\\hline ")
        for qm in qmidlist:
            quizmarks = QuestionModule.objects.get(pk=qm).marks
            f.write("Q" + str(j) + " & " + str(quizmarks) + " \\" + "\\ ")
            f.write("\\hline ")
            j = j+1
        f.write("\\end{tabular}")
        f.write("\\end{center}\n")

        f.write("\\begin{enumerate}")
        # update enumerate
        for q in qidlist:
            questionadd(q)

        for qm in qmidlist:
            questionmodule(qm)
        f.write("\\end{enumerate}\n")
        f.write("\\end{document}\n")
