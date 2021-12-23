from flask import Flask, session, request, render_template, redirect
import config.config as config
import datetime

# app setup
app = Flask(__name__)
# config
app_configuration = config.config()
app.config.from_object(app_configuration)
app.secret_key = app_configuration.secret



# session timeout
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=app_configuration.timeout)
    session.modified = True


@app.route('/', methods=['GET'])
def Home():
    if request.method == 'GET':
        return render_template('Home.html')


@app.route('/.well-known/acme-challenge/<filename>')
def wellknown(filename):           # Letsencrypt certbot-auto
    return redirect(f"/static/.well-known/acme-challenge/{filename}")

if __name__ == "__main__":
    app.run(debug=app_configuration.debug,
            threaded=app_configuration.threaded,
            ssl_context='adhoc')
