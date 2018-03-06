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
    print("sql = ", sql)
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        type_set.append({ 'type_code':row[0], 'type_desc':row[1] })
    conn.close()

    return type_set 

def get_quiz(quiz_type):
    quiz_set = []
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

def get_link(type_set):
    html = "<br>"
    for type in type_set:
       if type['type_code'] == "01":
          link = '/state_capital'
       else : 
          link = '/nation_capital'
       html += "<li><a href=" + link + ">" + type['type_desc'] + "</li><br>"

    return html

def get_quiz_header(quiz_type_desc):
    html = "<h1> " + quiz_type_desc + "Question</h1>"
    return html 

def table_quiz_answer(quiz_set, page_no, link):
    cur_page = int(page_no)

    html = "<table border = '1'>"
    html += "<tr><th align = 'center'><h3> Quiz </th>"  
<<<<<<< HEAD:quiz_answer_session.py
    html += "<th align = 'center'><h3> Answer </th></tr>"  

=======
    html += "<th align = 'center'><h3> Answer </th></tr>"
    
>>>>>>> 8a8279241481232afff7d19696392e2db6b10ce5:quiz_answer_web.py
    qa_pair = "<tr align = 'center' valign = 'middle'>"
    qa_pair += "<td><h3>Capital of <b>" + quiz_set[cur_page]['quiz'] + "</b></td>"
    qa_pair += "<td><h3><font color='red'><i>" + quiz_set[cur_page]['answer'] + "</font></i></h3><p></td>"
    qa_pair += "</tr>"
<<<<<<< HEAD:quiz_answer_session.py
    html += qa_pair

=======
    
    html += qa_pair
>>>>>>> 8a8279241481232afff7d19696392e2db6b10ce5:quiz_answer_web.py
    html += "</table>"
    html += "<br><br>"
    return html
   
def table_page_action(total_page, cur_page, link):

    cur_page = int(cur_page)

    is_pre = False
    is_next = False

    if cur_page <> 0  and total_page > 1 :
        is_pre = True
    if cur_page < total_page-1:
        is_next = True

    html = "<table> <tr>"
  
    if is_pre == True: 
        html += "<td><li><a href=" + link + "_prev> PREV </li></td>"
    if is_next == True: 
        html += "<td><li><a href=" + link + "_next> NEXT </li></td>"

    html += "</tr></table>"
    
    return html

def get_contents(quiz_type_code, link, quiz_type_desc):
    cur_page = session['page_no']

    html = question_answer_html_header
    html += get_quiz_header(quiz_type_desc)

    quiz_set = get_quiz(quiz_type_code)
    qa_pair = table_quiz_answer(quiz_set, cur_page, link)
    html += qa_pair
    html_page_info = table_page_action(len(quiz_set), cur_page, link)
    html += html_page_info
    html += question_answer_html_footer

    return html

@app.route("/")
def index():
    type_set = get_quiz_type()
    html = home_html_header
    html += get_link(type_set)
    html += home_html_footer
    return html

@app.route("/state_capital", methods=['GET'])
def state_capital():
    global session
    if 'page_no' not in session:
        session = {'page_no':'0'}
    html = get_contents("01", "/state_capital", "State Capital ")
    return html
 
@app.route("/state_capital_prev", methods=['GET'])
def state_capital_prev():
    global session
    page_no = session['page_no']
    session['page_no'] = int(page_no) - 1
    html = get_contents("01", "/state_capital", "State Capital ")
    return html
 
@app.route("/state_capital_next", methods=['GET'])
def state_capital_next():
    global session
    page_no = session['page_no']
    session['page_no'] = int(page_no) + 1
    html = get_contents("01", "/state_capital", "State Capital ")
    return html
 
@app.route("/nation_capital", methods=['GET'])
def nation_capital():
    global session
    if 'page_no' not in session:
        session = {'page_no':'0'}
    html = get_contents("02", "/nation_capital", "Nation Capital ")
    return html
 
@app.route("/nation_capital_prev", methods=['GET'])
def nation_capital_prev():
    global session
    page_no = session['page_no']
    session['page_no'] = int(page_no) - 1
    html = get_contents("02", "/nation_capital", "Nation Capital ")
    return html
 
@app.route("/nation_capital_next", methods=['GET'])
def nation_capital_next():
    global session
    page_no = session['page_no']
    session['page_no'] = int(page_no) + 1
    html = get_contents("02", "/nation_capital", "Nation Capital ")
    return html
 
app.secret_key = 'secret real secret'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
