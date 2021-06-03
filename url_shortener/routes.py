from flask import render_template, request, redirect, url_for, flash
import sqlalchemy
from url_shortener.url_filter import validate_url
from url_shortener import app, init_connection_engine
from uuid import uuid4


@app.route('/')
def index():
    """
    Renders index page.
    """
    return render_template('index.html')


# Shortened URL
@app.route('/short_URL', methods=['POST'])
def shorten():
    """
    Attempts to shorten the URL.
    """

    # On POST request, when the form is submitted.
    if request.method == 'POST':

        url_data = request.form['url']

        # If no URL has been provided
        if not url_data:
            flash('No URL provided. Please try again')
            return redirect(url_for('index'))

        # ================================================================================= Valid URL has been provided

        db = init_connection_engine()

        if type(validate_url(url_data)) is bool and validate_url(url_data):

            url_id = str(uuid4().fields[0])

            def create_tables():
                """
                Creates tables (if they don't already exist)
                """
                with db.connect() as conn:
                    conn.execute(
                        "CREATE TABLE IF NOT EXISTS url_list "
                        "(url_id VARCHAR(20) NOT NULL UNIQUE, url_data VARCHAR(2083) NOT NULL);"
                    )
            create_tables()

            # Preparing a statement beforehand can help protect against injections.
            stmt = sqlalchemy.text(
                "INSERT INTO url_list (url_data, url_id)" " VALUES (:url_data, :url_id)"
            )

            # Check if the URL record exists in the DB already.
            try:
                with db.connect() as conn:
                    lookup_url = "SELECT url_id FROM url_list WHERE url_data='" + url_data + "';"
                    url_exists = conn.execute(lookup_url).fetchall()

                    if len(url_exists) > 0:
                        return render_template(
                            'short_URL.html',
                            url=url_data,
                            result=f"{app.config['TARGET_URL']}{url_exists[0][0]}"
                        )
            # If no record was found in the DB.
            except:
                pass

            # Adding URL to the DB.
            try:
                # Using a with statement ensures that the connection is always released
                # back into the pool at the end of statement (even if an error occurs).
                with db.connect() as conn:
                    conn.execute(stmt, url_data=url_data, url_id=url_id)
            # If something goes wrong.
            except:
                flash('Something went wrong')
                return redirect(url_for('index'))

            return render_template(
                'short_URL.html',
                url=url_data,
                result=f"{app.config['TARGET_URL']}{url_id}"
            )

        # =================================================================================== Couldn't validate the URL
        else:
            error_msg = validate_url(url_data)
            flash(error_msg)
            return redirect(url_for('index'))


@app.route('/<string:id>/')
def forward_to(id):
    """
    Routing the shortened URL to its target.
    """

    db = init_connection_engine()

    if id == 'short_URL':
        return redirect(url_for('index'))
    else:
        # Looking up the URL by its ID in the DB.
        try:
            # Using a with statement ensures that the connection is always released
            # back into the pool at the end of statement (even if an error occurs).
            with db.connect() as conn:
                lookup_url = "SELECT url_data FROM url_list WHERE url_id='" + id + "';"
                target_url = conn.execute(lookup_url).fetchone()
                # If target URL is not found.
                if not target_url:
                    flash('Not found')
                    return redirect(url_for('index'))
        # If something goes wrong.
        except:
            flash('Something went wrong')
            return redirect(url_for('index'))

    return redirect(target_url[0])
