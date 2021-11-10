from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def main():
    # loading a list to select panel
    schema = loadschema()
    if request.method == 'POST':
        # example of changing text area only - need to change to QEP for this part
        text = request.form['specifyQuery']
        processed_text = text.upper()
        return render_template('interface.html', text=processed_text, schema=schema)
    else:
        return render_template('interface.html', schema=schema)


# load list from data
def loadschema():
    schema = ['schema2', 'schema4', 'schema6']
    return schema


if __name__ == "__main__":
    app.run()

# @app.route('/', methods=['GET','POST'])
# def interface_post():
#     text = request.form['text']
#     processed_text = text.upper()
#     return render_template("interface.html", text=processed_text)


