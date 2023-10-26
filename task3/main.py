from flask import Flask, request, Response
import json
import xml.etree.ElementTree as ET

app = Flask(__name__)

def json_to_xml(json_data):
    def recursive_dict_to_xml(parent, data):
        for key, value in data.items():
            element = ET.SubElement(parent, key)
            if isinstance(value, dict):
                recursive_dict_to_xml(element, value)
            elif isinstance(value, list):
                for item in value:
                    recursive_dict_to_xml(element, {"item": item})
            else:
                element.text = str(value)

    root = ET.Element("data")
    recursive_dict_to_xml(root, json_data)
    return ET.tostring(root, encoding="unicode")

@app.route('/convert', methods=['POST'])
def convert_json_to_xml():
    try:
        json_data = request.json
        if not json_data:
            return Response(response="Invalid JSON", status=400)

        xml_data = json_to_xml(json_data)
        return Response(response=xml_data, content_type="application/xml", status=200)
    except Exception as e:
        return Response(response=str(e), status=500)

if __name__ == '__main__':
    app.run(debug=True)
