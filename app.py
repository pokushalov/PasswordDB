import secrets

from flask import Flask, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from loguru import logger
from model import PWDForm
from mydb import mydb

csrf = CSRFProtect()

app = Flask(__name__)
csrf.init_app(app)

app.debug = True
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
app.config['WTF_CSRF_ENABLED'] = False

# toolbar = DebugToolbarExtension(app)
Bootstrap(app)

dbs = None

@app.route('/del/<pwdid>', methods=['POST', 'GET'])
def delpwd(pwdid):
    dbs.deletpwd(pwdid)
    return redirect(url_for('main_page'))


@app.route('/editpwd/<pwdid>', methods=['POST', 'GET'])
def editpwd(pwdid):
    form = PWDForm(request.form)
    current_info = dbs.findbyid(pwdid)
    # set values
    form.generated_id = current_info["generated_id"]
    form.entity_name.data = current_info["entity_name"]
    form.entity_username.data = current_info["entity_username"]
    form.password.data = current_info["password"]
    form.ticket.data = current_info["ticket"]

    if request.method == 'POST' and form.validate_on_submit():
        try:
            logger.info("Updating info ")
            entity_name = form.entity_name.data
            entity_username = form.entity_username.data
            password = form.password.data
            ticket = form.ticket.data
            logger.debug(f"{entity_name}:{entity_username}:{password}:{ticket}")

            dbs.AddInfo(entity_name, entity_username, password, ticket, form.generated_id)
            logger.success("Added")
            return redirect(url_for('main_page'))
        except Exception as e:
            logger.error(f"Error: {e}")
    else:
        return render_template('updatepwd.html', action="Edit", form=form)
    return 'OK'

@app.route('/editpwd', methods=['POST', 'GET'])
def addpwd():

    form = PWDForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        try:
            logger.info("Adding info ")
            logger.info("***")
            entity_name = form.entity_name.data
            entity_username = form.entity_username.data
            password = form.password.data
            ticket = form.ticket.data
            logger.debug(f"{entity_name}:{entity_username}:{password}:{ticket}")

            dbs.AddInfo(entity_name, entity_username, password, ticket, None)
            logger.success("Added")
            return redirect(url_for('main_page'))
        except Exception as e:
            logger.error(f"Error: {e}")
    else:
        return render_template('updatepwd.html', form=form)


@app.route('/')
def main_page():
    rows = dbs.getallpwds()
    return render_template("main.html", rows=rows)


if __name__ == '__main__':
    logger.info("Starting")
    dbs = mydb("pwds.sqllite", logger)
    app.run(debug=True, port=5002)
