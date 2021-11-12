import interface

from flask import Flask, request, render_template
#
app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def main():
    schema = interface.loadschema()
    if request.method == 'POST':
        getQuery = request.form['specifyQuery']
        # get schema and string and pass to function
        getSelectedSchema = request.form['schemas']


        # processed_text = interface.text(getQuery)

        #get  it from randy's list
        numberOfItem = 4;
        # return numberOfItem

        # interface.loadQEP(getSelectedSchema,processed_text)
        # interface.toggle_display();
        return render_template("interface.html", text=getSelectedSchema, schema=schema, numberOfItem=numberOfItem)
    else:
        return render_template('interface.html', schema=schema)


# main()


# load list from data
# def loadschema():
#     schema = ['schema2', 'schema4', 'schema6']
#     return schema

if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = '8000', debug = True)


# @app.route('/', methods=['GET','POST'])
# def interface_post():
#     text = request.form['text']
#     processed_text = text.upper()
#     return render_template("interface.html", text=processed_text)


