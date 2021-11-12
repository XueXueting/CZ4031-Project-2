# from flask import Flask, request, render_template

# app = Flask(__name__)

# @app.route('/', methods=['GET','POST'])
def text(query):
    # example of changing text area only - need to change to QEP for this part
    processed_text = query.upper()
    return processed_text

# load list from data
def loadschema():
    schema = ['cust(...)', 'dept(...)', 'trans(...)']
    return schema

# def createElement():
#     HTMLcode = '<div><a href="www.google.com">Google Search</a></div>'
#     self.response.out.write(HTMLcode)

# show/hide annotation
# def toggle_display():
    # el = document.querySelector('.content_section');

    # if (el.style.visibility == 'hidden')
    # {
    #     el.style.visibility = 'visible'
    # } else {
    #     el.style.visibility = 'hidden'
    # }



# if __name__ == '__main__':
#     app.run()

# @app.route('/', methods=['GET','POST'])
# def interface_post():
#     text = request.form['text']
#     processed_text = text.upper()
#     return render_template("interface.html", text=processed_text)




# from flask import Flask, request, render_template
#
# app = Flask(__name__)

# @app.route('/')
# def userinterface():
#     text = request.form['specifyQuery']
#     processed_text = text.upper()
#     schema = ['schema2', 'schema4', 'schema6']
#     return render_template('interface.html', text=processed_text, schema=schema)
#
# if __name__ == "__main__":
#     app.run()