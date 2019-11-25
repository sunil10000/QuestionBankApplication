import os
import sys
from .models import QuizPaper, Question, QuestionModule


def generate_quiz(quizpaperid, title, top, bottom, left, right):
    f = open("media/Quiz.tex", "w+")
    header = str(title).replace(" ", r" \ ").replace("_", "-")
    j = 1
    f.close()
    with open("media/Quiz.tex", "w+") as f:

        def questionadd(questid):
            print("inside question")
            ques = Question.objects.get(pk=questid)
            statement = str(ques.statement)
            marks = ques.marks
            f.write("\\item " + statement + "\\hfill\n")
            f.write("[" + str(marks) + " Marks]" + "\n")
            f.write(r"\\Solution:\\ ")
            f.write(r"\vspace*{" + str((marks * 15)) + "pt}")

        def questionmodule(moduleid):
            print("inside question module")
            quesmodule = QuestionModule.objects.get(pk=moduleid)
            statement = str(quesmodule.statement)
            marks = quesmodule.marks
            f.write("\\item " + statement + "\\hfill\n")
            f.write("[" + str(marks) + " Marks]" + "\n")
            questionidlist = Question.objects.filter(parent=quesmodule.id, isRoot=0)
            questionmoduleidlist = QuestionModule.objects.filter(parent=quesmodule.id, isRoot=0)
            lff = len(questionidlist) + len(questionmoduleidlist)
            if lff != 0:
                f.write("\\begin{enumerate}")
                for ques in questionidlist:
                    questionadd(ques.id)
                for quesmod in questionmoduleidlist:
                    questionmodule(quesmod.id)
                f.write("\\end{enumerate}\n")

        # adding template
        f.write("\\documentclass[10pt]{article}\n")
        f.write("\\usepackage[a4paper,bottom = "+str(bottom)+" in,left = "+str(left)+" in,right = "+str(right)+" in,top = "+str(top)+" in]{geometry}\n")
        f.write("\\usepackage[british]{babel}\n")
        #f.write(r'\emergencystretch 3em')
        f.write("\\usepackage {seqsplit}\n")
        f.write("\\usepackage {amsmath}\n")
        f.write("\\usepackage {fancyhdr}\n")
        f.write("\\pagestyle {fancy}\n")
        f.write("\\lhead {Name \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_}\n")
        f.write("\\rhead {Roll No. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_}\n")
        f.write("\\renewcommand {\headrulewidth}{0.4 pt}\n")
        f.write("\\usepackage {pgf}\n")
        f.write("\\usepackage {pgfpages}\n")
        f.write("\\usepackage {graphicx}\n")
        f.write("\\pgfpagesdeclarelayout {boxed} { \edef\pgfpageoptionborder {3 pt}} { \n")
        f.write("\\pgfpagesphysicalpageoptions \n")
        f.write(" { \n")
        f.write("    logical pages = 1, % \n")
        f.write( "} \n")
        f.write ("\\pgfpageslogicalpageoptions{1}{ \n")
        f.write("    border code =\pgfsetlinewidth {2 pt}\pgfstroke, % \n")
        f.write("    border shrink =\pgfpageoptionborder, \n")
        f.write("    resized width = .90\pgfphysicalwidth, \n")
        f.write("    resized height = .90\pgfphysicalheight, center =\pgfpoint \n")
        f.write("{.5\pgfphysicalwidth}{.5\pgfphysicalheight} }} \n")
        f.write("\\pgfpagesuselayout {boxed} \n")
        f.write(r"\begin {document}\sloppy"+"\n")
        f.write("\\vspace*{2cm}\n")

        f.write("\\begin{center}\n")
        f.write(r"\Huge{"+ header + "}"+r"\\"+"\n")
        f.write("\\vspace*{1 cm}\n")
        f.write(r"\Huge {Duration : 3hrs}"+r"\\"+"\n")
        f.write("\\vspace*{1 cm}\n")
        f.write(r"\date[\today"+ "\n")
        f.write("\\"+"\\")
        f.write("\\vspace*{2 cm}\n")
        quiz = QuizPaper.objects.get(pk=quizpaperid)
        qidlist = list(quiz.qid_list.split(","))[1:]
        qmidlist = list(quiz.qmid_list.split(","))[1:]
        f.write("\\begin{tabular}{|c|c|c|}\n")
        f.write("\\hline ")
        f.write("Question Number & Max Marks & Obtained Marks "+r"\\"+"\n")
        f.write("\\hline ")
        sum_marks = 0
        # create table
        for q in qidlist:
            quizmarks = Question.objects.get(pk=q).marks
            sum_marks = sum_marks + quizmarks
            f.write("Q"+str(j)+" & "+str(quizmarks)+" & \\"+"\\ ")
            j = j+1
            f.write("\\hline ")
        for qm in qmidlist:
            quizmarks = QuestionModule.objects.get(pk=qm).marks
            sum_marks = sum_marks + quizmarks
            f.write("Q" + str(j) + " & " + str(quizmarks) + " & \\" + "\\ ")
            f.write("\\hline ")
            j = j+1

        f.write("Total Marks & "+ str(sum_marks)+" & "r"\\"+"\n")
        f.write("\\hline ")
        f.write("\\end{tabular}")
        f.write("\\end{center}\n")
        f.write("\\pagebreak")
        lf = len(qidlist)+len(qmidlist)
        if lf != 0:
            f.write("\\begin{enumerate}")
            # update enumerate
            for q in qidlist:
                questionadd(q)

            for qm in qmidlist:
                questionmodule(qm)
            f.write("\\end{enumerate}\n")
        f.write("\\end{document}\n")

    os.system("pdflatex -output-directory media media/Quiz.tex")




