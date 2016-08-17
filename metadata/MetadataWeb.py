#http://courses.pgbovine.net/csc201/week13-code.txt

from flask import Flask, render_template,jsonify
from mdr_util import *

app = Flask(__name__)


@app.route('/')
def index():

    #return 'Welcome to Metadata !!! '
    #return render_template('mdrhome.html')
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    status = getScreenStatus()
    return render_template('dashboard.html',status=status)

@app.route('/screens')
def screens():

    #screen_objects = getScreenObjects()
    #return render_template('mdr_screens_bs.html',screen_objects=screen_objects)
    return render_template('mdr_screens_bs.html')
    #return 'Hello World, '+name+ '!'


@app.route('/screenobjects_json')
def screenobjects_json():

    screen_objects_json = getJSONScreenObjects()
    return screen_objects_json
    #return "Hello World, Ragha"
    #return render_template('mdr_screens_bs.html',screen_objects=screen_objects)
    #return 'Hello World, '+name+ '!'


@app.route('/screen_fields/<screen_functionality>/<screen_name>')
def screen_fields(screen_functionality,screen_name):
    #screen_field_objects = {"Attribute_Name":"Test Attribute 1"}
    #screen_field_objects = getScreenFieldObjects(screen_name)

    #return render_template('mdr_screen_fields_bs.html',screen_name=screen_name,screen_field_objects=screen_field_objects)
    #return render_template('mdr_screen_fields_bs.html', screen_name=screen_name)
    return render_template('mdr_screen_fields_bs_top.html',screen_functionality=screen_functionality, screen_name=screen_name)
    #return 'Hello World, '+name+ '!'

@app.route('/mdr_screen_fields_bs_bottom/<screen_functionality>/<screen_name>')
def mdr_screen_fields_bs_bottom(screen_functionality,screen_name):
    return render_template('mdr_screen_fields_bs_bottom.html', screen_functionality=screen_functionality,screen_name=screen_name)

@app.route('/mdr_lineage/<screen_functionality>/<screen_name>/<screen_field_name>')
def mdr_lineage(screen_functionality,screen_name,screen_field_name):
    #screen_functionality ="Test"
    #lineage_object = getLineage(screen_name,screen_field_name)
    #return render_template('mdr_lineage_bs.html',screen_name=screen_name,screen_field_name=screen_field_name,lineage_object=lineage_object)

    return render_template('mdr_lineage_bs_top.html',screen_functionality=screen_functionality,screen_name=screen_name,screen_field_name=screen_field_name)

    #return 'Hello World, '+name+ '!'


@app.route('/mdr_lineage_bs_bottom/<screen_name>/<screen_field_name>')
def mdr_lineage_bs_bottom(screen_name,screen_field_name):

    lineage_object = getLineage(screen_name,screen_field_name)
    return render_template('mdr_lineage_bs_bottom.html',screen_name=screen_name,screen_field_name=screen_field_name,lineage_object=lineage_object)

    #return render_template('mdr_lineage_bs_top.html',screen_name=screen_name,screen_field_name=screen_field_name)


def getJSONScreenObjects():
    # screen master sharepoint list name

    list_name = "Screen Master"

    screen_objects_json = json_sharepointListRowsByListName(list_name)

    return screen_objects_json

def getScreenObjects():
    #screen master sharepoint list name
    list_name = "Screen Master"

    # screen master entity name (i.e. screen name)
    list_column_name = "Entity_x0020_Name"

    #screen_objects = UniqueListItemsByListName_AttributeName(list_name, list_column_name)
    screen_objects =  sharepointListRowsByListName(list_name)
    screen_objects_sorted = sorted(screen_objects,key=list_screen_master_sort,reverse=False)
    #screen_objects = [{"Entity_Name":"Transition"},{"Entity_Name":"Make a payment"},{"Entity_Name":"Make a deposit"}]
    return screen_objects_sorted


def getScreenFieldObjects(screen_name):
    #screen master sharepoint list name
    list_name = "Screen Fields"

    screen_field_objects = getAttributesbyEntity(list_name,screen_name)

    #screen_objects = [{"Entity_Name":"Transition"},{"Entity_Name":"Make a payment"},{"Entity_Name":"Make a deposit"}]
    return screen_field_objects


def getLineage(screen_name,screen_field_name):
    #screen master sharepoint list name
    list_name = "Screen Fields"

    lineage_object = getMDRLineage(screen_name,screen_field_name)

    #displayLineage (screen_name,screen_field_name)

    #screen_objects = [{"Entity_Name":"Transition"},{"Entity_Name":"Make a payment"},{"Entity_Name":"Make a deposit"}]
    return lineage_object

@app.context_processor
def utility_processor():

    def cleanHTMLTags_Flask(input_string):

        output_string = cleanHTMLTags(input_string)

        return output_string

    def getScreenFieldObjects_bs(screen_name):
        return getScreenFieldObjects(screen_name)

    return dict(cleanHTMLTags_Flask=cleanHTMLTags_Flask,getScreenFieldObjects_bs=getScreenFieldObjects_bs)


if __name__ == '__main__':
    #app.run()
    #app.run(debug=True)
    app.run(host='0.0.0.0')
