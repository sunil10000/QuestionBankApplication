import os
import sys
from .models import QuestionBank, Question, QuestionModule


def downloadbank(bankid):
    QB = QuestionBank.objects.get(pk=bankid)
    f = open("media/Bank.tex", "w+")
    header = str(QB.title).replace(" ", r" \ ").replace("_", "-")
    j = 1
    f.close()
    with open("media/Bank.tex", "w+") as f:

        def questionadd(questid):
            print("inside question")
            ques = Question.objects.get(pk=questid)
            statement = str(ques.statement).replace(" ", r" \ ").replace("_", "-")
            marks = ques.marks
            answer = str(ques.answer).replace(" ", r" \ ").replace("_", "-")
            f.write("\\item \seqsplit{" + statement + "}\\hfill\n")
            f.write("[" + str(marks) + " Marks]" + "\n")
            f.write(r"\\Solution: ")
            f.write(answer+r"\\")
            f.write(r"\vspace*{10pt}")

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

        qidlist = Question.objects.filter(parent=bankid, isRoot=1)
        qmidlist = QuestionModule.objects.filter(parent=bankid, isRoot=1)
        f.write("\\begin{tabular}{|c|c|}\n")
        f.write("\\hline ")

        # create table
        for q in qidlist:
            quizmarks = Question.objects.get(pk=q.id).marks
            f.write("Q"+str(j)+" & "+str(quizmarks)+" \\"+"\\ ")
            j = j+1
            f.write("\\hline ")
        for qm in qmidlist:
            quizmarks = QuestionModule.objects.get(pk=qm.id).marks
            f.write("Q" + str(j) + " & " + str(quizmarks) + " \\" + "\\ ")
            f.write("\\hline ")
            j = j+1
        f.write("\\end{tabular}")
        f.write("\\end{center}\n")

        f.write("\\begin{enumerate}")
        # update enumerate
        for q in qidlist:
            questionadd(q.id)

        for qm in qmidlist:
            questionmodule(qm.id)
        f.write("\\end{enumerate}\n")
        f.write("\\end{document}\n")

    os.system("pdflatex -output-directory media media/Bank.tex")
