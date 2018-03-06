import pymysql
from flask import Flask, flash, redirect, render_template, request, session, abort
app = Flask(__name__)

"""
Run this from your shell
and then visit http://localhost:5000/ from your browser
"""

home_html_header = """
<html>
<body background='http://flightattendanttraininghq.com/wp-content/uploads/2017/09/Quiz-Time.png'>
<center>
<h1>Welcome to Quiz World</h1>
<hr>
"""

home_html_footer = """
</center>
</html>
"""

question_answer_html_header = """
<html>
<body>
    <center>
"""

question_answer_html_footer = """    
    </center>
</body>
</html>
"""

def get_quiz_type():
    type_set = []
    conn = pymysql.connect(host='localhost',
                       user='root', password='as920558',
                       db='test', charset='utf8')
    curs = conn.cursor()
    sql = "select distinct(quiz_type_code), quiz_type_desc from quiz"
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        type_set.append({ 'type_code':row[0], 'type_desc':row[1] })
    conn.close()

    return type_set 

def get_quiz_set(quiz_type):
    quiz_set = []
    #type_code = int(quiz_type)
    conn = pymysql.connect(host='localhost',
                       user='root', password='as920558',
                       db='test', charset='utf8')
    curs = conn.cursor()
    sql = "select quiz, answer from quiz where quiz_type_code = " + quiz_type
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        quiz_set.append({ 'quiz':row[0], 'answer':row[1] })
    conn.close()
    return quiz_set

#Initial Page, QUIZ HOME
def get_main_link(type_set):
    html = "<br>"
    html += "<table>\n"
    html += "<form action='/quiz_question' method='POST'>\n"

    for type in type_set:
       code = str(type['type_code'])
       desc = type['type_desc']
       html += "<tr><td align = 'center'>"
       html += "<input type='radio' name='type_code' value='" + code + "'>" + desc + "</input><br>\n" 
       html += "<input type='hidden' name='type_desc' value='" + desc + "'> </input><br>\n" 
       html += "<input type='hidden' name='page_no' value='0' />\n"
       html += "</td></tr>"

    html += "<tr><td align='center'><input type='submit' value = 'Start'></td></tr>\n"
    html += "</form>\n"

    return html

#QUIZ DETAIL
def get_quiz_header(quiz_type_desc):
    html = question_answer_html_header
    html += "<h1> " + quiz_type_desc + " Question</h1>\n"
    return html 

def table_quiz(quiz_set, page_no):

    html = "<table border = '1'>\n"
    html += "<tr>\n <th align = 'center'><h3> Quiz </th>\n"  
    html += "<th align = 'center'><h3> Answer </th></tr>\n"  

    html += "<tr align = 'center' valign = 'middle'>\n"
    html += "<td><h3>Capital of <b>" + quiz_set[page_no]['quiz'] + "</b></td>\n"
    html += "<form action='/quiz_answer' method='POST'>"
    html += "<td><input type = 'text' name = 'answer' > </td>\n"
    html += "</tr>\n"

    html += "</table>\n"
    html += "<br><br>\n"

    html += "<input type='submit' value='Submit'>\n"

    return html
   
def table_answer(quiz_set, page_no):

    submit_value = str(request.form['answer'])
    answer = quiz_set[page_no]['answer'] 

    if submit_value.upper() == answer.upper():
       html = "<h3> Your answer is correct!!!</h3><br>\n"
    else :
       html = "<h3> Unfortunatelly, your answer is wrong!!!</h3><br>\n"

    html += "<table border = '1'>\n"
    html += "<tr>\n <th align = 'center'><h3> Quiz </th>\n"  
    html += "<th align = 'center'><h3> Answer </th></tr>\n"  

    qa_pair = "<tr align = 'center' valign = 'middle'>\n"
    qa_pair += "<td><h3>Capital of <b>" + quiz_set[page_no]['quiz'] + "</b></td>\n"
    qa_pair += "<td><h3><font color='red'><i>" + quiz_set[page_no]['answer'] + "</font></i></h3><p></td>\n"
    qa_pair += "</tr>\n"
    html += qa_pair

    html += "</table>\n"
    html += "<br><br>\n"
    return html

def table_page_action(total_page, cur_page, page_type, type_code, type_desc):

    if page_type == "question":
       html = "<input type='hidden' name='page_no' value='" + str(cur_page) +"'/>\n"
       html += "<input type='hidden' name='type_code' value='" + type_code +"'/>\n"
       html += "<input type='hidden' name='type_desc' value='" + type_desc +"'/>\n"
       html += "</form>\n"
    else :
       is_pre = False
       is_next = False

       if cur_page <> 0  and total_page > 1 :
           is_pre = True
       if cur_page < total_page-1:
           is_next = True

       html = "<table> <tr>\n"
     
       if is_pre == True: 
          html += "<form action='/quiz_question' method='POST'>\n"
          html += "<td><input type='submit' value='PREV'></td>\n"
          html += "<input type='hidden' name='page_no' value='" + str(cur_page-1) + "'/> \n"
          html += "<input type='hidden' name='type_code' value='" + type_code +"'/>\n"
          html += "<input type='hidden' name='type_desc' value='" + type_desc +"'/>\n"
          html += "</form>\n"
       if is_next == True: 
          html += "<form action='/quiz_question' method='POST'>\n"
          html += "<td><input type='submit' value='NEXT'></td>\n"
          html += "<input type='hidden' name='page_no' value='" + str(cur_page+1) + "'/> \n"
          html += "<input type='hidden' name='type_code' value='" + type_code +"'/>\n"
          html += "<input type='hidden' name='type_desc' value='" + type_desc +"'/>\n"
          html += "</form>\n"

       html += "</tr></table>\n"
    
    return html

def get_contents(quiz_set, type_code, type_desc, page_type):
    cur_page = int(request.form['page_no'])
    print("cur_page = ", cur_page)

    html = get_quiz_header(type_desc)

    if page_type == "question":
       html += table_quiz(quiz_set, cur_page)
    elif page_type == "answer": 
       html += table_answer(quiz_set, cur_page)

    html += table_page_action(len(quiz_set), cur_page, page_type, type_code, type_desc)

    html += question_answer_html_footer

    return html

@app.route("/")
def index():
    type_set = get_quiz_type()
    html = home_html_header
    html += get_main_link(type_set)
    html += home_html_footer
    return html

@app.route("/quiz_question", methods=['POST'])
def quiz_question():
    type_code = str(request.form['type_code'])
    type_desc = str(request.form['type_desc'])

    quiz_set = get_quiz_set(type_code)

    html = get_contents(quiz_set, type_code, type_desc, "question")

    return html

@app.route("/quiz_answer", methods=['POST'])
def quiz_answer():

    type_code = str(request.form['type_code'])
    type_desc = str(request.form['type_desc'])
    answer = str(request.form['answer'])

    quiz_set = get_quiz_set(type_code)

    html = get_contents(quiz_set, type_code, type_desc, "answer")

    return html

app.secret_key = 'secret real secret'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
