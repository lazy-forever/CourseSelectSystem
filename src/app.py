from flask import *
from flask_bootstrap import Bootstrap
from user import *
from admin import *
import secrets

app = Flask(__name__, static_folder='static', template_folder='templates')
Bootstrap(app)
app.secret_key = secrets.token_urlsafe(16)

@app.route('/logout')
def logout():
    session.pop('num', None)
    session.pop('is_admin', None)
    return redirect(url_for('login'))

# user
@app.route('/')
def index():
    if session.get('num') is not None:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        num = request.form['num']
        password = request.form['password']
        if user_loginSql(num, password):
            session['num'] = num
            session['is_admin'] = False
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message='用户名或密码错误')

@app.route('/courses')
def courses():
    if session.get('num') is not None:
        courses = courses_showSql()
        return render_template('courses.html', courses=courses)
    return redirect(url_for('login'))

@app.route('/course/<code>')
def course(code):
    if session.get('num') is not None:
        course = course_showSql(code)
        if course is None:
            return render_template('404.html')
        return render_template('course.html', course=course)
    return redirect(url_for('login'))

@app.route('/select/<code>', methods=['POST'])
def select(code):
    if session.get('num') is not None and session.get('is_admin') is False:
        if select_courseSql(session['num'], code):
            return jsonify({"message":"success"})
        else:
            return jsonify({"message":"error"})
    return jsonify({"message":"error"})

@app.route('/info')
def info():
    if session.get('num') is not None and session.get('is_admin') is False:
        selects = info_showSql(session['num'])
        return render_template('info.html', selects=selects)
    return redirect(url_for('login'))

@app.route('/delete/<code>', methods=['POST'])
def delete(code):
    if session.get('num') is not None and session.get('is_admin') is False:
        if delete_selectSql(session['num'], code):
            return jsonify({"message":"success"})
        else:
            return jsonify({"message":"error"})
    return jsonify({"message":"error"})

@app.route('/projects')
def projects():
    if session.get('num') is not None and session.get('is_admin') is False:
        projects = projects_showSql(session['num'])
        return render_template('projects.html', projects=projects)
    return redirect(url_for('login'))

@app.route('/exitProject/<id>', methods=['POST'])
def exit_project(id):
    if session.get('num') is not None and session.get('is_admin') is False:
        if exit_projectSql(session.get('num'), id):
            return jsonify({"message":"success"})
        else:
            return jsonify({"message":"error"})
    return jsonify({"message":"error"})

@app.route('/editProject/<id>', methods=['POST', 'GET'])
def edit_project(id):
    if request.method == 'GET':
        if session.get('num') is not None and session.get('is_admin') is False:
            return render_template('editProject.html', id=id)
        return redirect(url_for('login'))
    if request.method == 'POST':
        if session.get('num') is not None and session.get('is_admin') is False:
            name = request.json['name']
            imgurl = request.json['imgurl']
            url = request.json['url']
            if edit_projectSql(session.get('num'), id, name, imgurl, url):
                return jsonify({"message":"success"})
            return jsonify({"message":"error"})
        return jsonify({"message":"error"})




# admin
@app.route('/admin')
def admin_redirect():
    return redirect(url_for('admin'))

@app.route('/admin/')
def admin():
    if session.get('num') is not None and session.get('is_admin') is True:
        return render_template('admin/index.html')
    return redirect(url_for('admin_login'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin/login.html')
    else:
        num = request.form['num']
        password = request.form['password']
        if admin_loginSql(num, password):
            session['num'] = num
            session['is_admin'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', message='用户名或密码错误')

@app.route('/admin/courses')
def admin_courses():
    if session.get('num') is not None and session.get('is_admin') is True:
        courses = courses_showSql()
        return render_template('admin/courses.html', courses=courses)
    return redirect(url_for('admin_login'))

@app.route('/admin/mycourses')
def admin_mycourses():
    if session.get('num') is not None and session.get('is_admin') is True:
        courses = mycourses_showSql(session['num'])
        return render_template('admin/mycourses.html', courses=courses)
    return redirect(url_for('admin_login'))

@app.route('/admin/delete/<code>', methods=['POST'])
def admin_delete(code):
    if session.get('num') is not None and session.get('is_admin') is True:
        if delete_courseSql(code):
            return jsonify({"message":"success"})
        else:
            return jsonify({"message":"error"})
    return jsonify({"message":"error"})

@app.route('/admin/editor/<code>', methods=['GET', 'POST'])
def admin_editor(code):
    if session.get('num') is not None and session.get('is_admin') is True:
        course = course_showSql(code)
        if course is None:
            return render_template('404.html')
        if request.method == 'GET':
            return render_template('admin/editor.html', course=course)
        else:
            name = request.json['name']
            credit = request.json['credit']
            if course_editorSql(code, name, credit):
                return jsonify({"message":"success"})
            else:
                return jsonify({"message":"error"})
    return redirect(url_for('admin_login'))


@app.route('/admin/add', methods=['GET', 'POST'])
def admin_add():
    if session.get('num') is not None and session.get('is_admin') is True:
        if request.method == 'GET':
            return render_template('admin/add.html')
        else:
            code = request.json['code']
            name = request.json['name']
            credit = request.json['credit']
            num = session.get('num')
            if course_addSql(code, name, credit, num):
                return jsonify({"message":"success"})
            else:
                return jsonify({"message":"error"})
    return redirect(url_for('admin_login'))


@app.route('/admin/info')
def admin_info():
    if session.get('num') is not None and session.get('is_admin') is True:
        courses = mycourses_showSql(session.get('num'))
        return render_template('admin/info.html', courses=courses)
    return redirect(url_for('admin_login'))

@app.route('/admin/course/<code>')
def admin_course(code):
    if session.get('num') is not None and session.get('is_admin') is True:
        course = course_showSql(code)
        choose = choose_showSql(code)
        if course is None:
            return render_template('404.html')
        return render_template('admin/mystudents.html', course=course, choose=choose)
    return redirect(url_for('admin_login'))

@app.route('/admin/deleteChoose/<code>/<num>', methods=['POST'])
def admin_delete_choose(num, code):
    if session.get('num') is not None and session.get('is_admin') is True:
        if delete_selectSql(num, code):
            return jsonify({"message":"success"})
        else:
            return jsonify({"message":"error"})
    return jsonify({"message":"error"})

@app.route('/admin/editScore/<code>/<num>', methods=['POST'])
def admin_editScore(num, code):
    if session.get('num') is not None and session.get('is_admin') is True:
        score = request.json['score']
        if edit_scoreSql(num, code, score):
            return jsonify({"message":"success"})
        else:
            return jsonify({"message":"error"})
    return jsonify({"message":"error"})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        if session.get('is_admin') is False:
            return render_template('register.html', message='您不是管理员')
        num = request.form['num']
        name = request.form['name']
        password = request.form['password']
        if registerSql(num, name, password):
            return render_template('register.html', message='注册成功')
        else:
            return render_template('register.html', message='注册失败')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)