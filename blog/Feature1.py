import os
import sys
import shutil
import argparse
from .models import QuizPaper, Question, QuestionModule

def fn(quizpaperid, title):
    f = open("Quiz.tex", "w+")
    header = title
    j=1
    with open("Quiz.tex", "w+"):
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
        qidlist = quiz.qid_list
        qmidlist = quiz.qmid_list
        # number_of_questions = len(qidlist)\
        # number_of_modules = len(qmidlist)
        f.write("\\begin{tabular}{|c|c|}\n")
        f.write("\\hline ")
        for q in qidlist:
            quizmarks = Question.objects.get(pk=q).marks
            f.write("Q"+str(j)+" & "+quizmarks+" \\"+"\\ ")
            j=j+1
            f.write("\\hline ")
        for qm in qmidlist:
            quizmarks = QuestionModule.objects.get(pk=qm).marks
            f.write("Q" + str(j) + " & " + quizmarks + " \\" + "\\ ")
            f.write("\\hline ")
            j = j+1
        f.write("\\end{tabular}")
        f.write("\\end{center}\n")

        f.write("\\begin{enumerate}")
        for q in qidlist:
            ques = Question.objects.get(pk=q)
            statement = ques.statement
            marks = ques.marks
            f.write("\\item \seqsplit{"+statement+"}\\hfill\n")
            f.write("["+str(marks)+" Marks]"+"\n")
            f.write("\\"+"\\"+" Solution:")
            f.write("\\vspace*{"+str((marks*40))+"pt}")
        

        for qm in qmidlist:
            quesmodule = QuestionModule.objects.get(pk=qm)
            statement = quesmodule.statement
            marks = quesmodule.marks
            f.write("\\item \seqsplit{"+statement+"}\\hfill\n")
            f.write("["+str(marks)+" Marks]"+"\n")
            f.write("\\"+"\\"+" Solution:")
            f.write("\\vspace*{"+str((marks*40))+"pt}")
        f.write("\\end{enumerate}\n")
        f.write("\\end{document}\n")
fn(2)
