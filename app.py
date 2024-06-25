from flask import Flask, render_template, abort
from lastfm_bot import User


app = Flask(__name__)


@app.route("/")
def user_index():
    users = User.get_all_users()
    return render_template('users.html', users=users)


@app.route("/user/<int:user_id>")
def user_view(user_id):
    user = User.get_user_from_db(user_id)
    if user is None:
        abort(404)
    all_songs = User.get_all_song(user_id)
    return render_template('user.html', user=user, songs=all_songs)


if __name__ == "__main__":
    app.run()