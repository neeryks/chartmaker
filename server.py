
from flask import Flask, request, jsonify,send_file
from coordfinder import get_zenith_ra_dec
from chart_maker import generate_config
from imageeditor import clean_crop, add_chart_background,merge,text_write
import os
import pandas as pd
import json

def loadpreset(filepath = "presets.json"):

    with open(filepath,'r') as file:
        data = json.load(file)
    return pd.DataFrame(data)

def find_template(df, size = None, chart_bg_color = None, position = None, ring_color = None):

    query_set = []
    if size and chart_bg_color and position is not None :
        query_set.append(f"size == '{size}'")
        query_set.append(f"bg_color == '{chart_bg_color}'")
        query_set.append(f"position == '{position}'")
        query_set.append(f"ring_color == '{ring_color}'")
    
    query = ' & '.join(query_set)
    results = df.query(query)
    if not results.empty:
        return results


app = Flask(__name__)

API_KEY = "Kill"

def authenticate(api_key):
    return api_key == API_KEY

@app.route('/receive_data', methods=['POST'])
def starchart():
    try:

        if 'Authorization' not in request.headers:
            return jsonify({'error': 'Missing API key'}), 401
        
        api_key = request.headers['Authorization']

        if not authenticate(api_key):
            return jsonify({'error': 'Invalid API key'}), 401

        starchart_data = request.get_json()

        # Ensure all required fields are present in the received JSON
        required_fields = ['orderid', 'location', 'date', 'time', 'bg_color', 'position', 'title_text']
        for field in required_fields:
            if field not in starchart_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        orderid = starchart_data['orderid']
        location = starchart_data['location']
        date = starchart_data['date']
        time = starchart_data['time']
        size = starchart_data['size']
        position = starchart_data['position']
        bg_color = starchart_data['bg_color']
        chart_font = starchart_data['font_color']
        title_text = starchart_data['title_text']
        font_color = starchart_data["font_color"]
        ring_color = starchart_data['ring_color']
        background_image = starchart_data['background_image']
        chart_background_image = starchart_data['chart_background_image']
        font_size_chart =  starchart_data['font_size_chart']

        if chart_background_image == "":
             chart_background_image = None

        if background_image == "":
             background_image = None

        print(font_color)
      
        ra,dec = get_zenith_ra_dec(date,time,location)
        df = loadpreset('presets.json')
        print("level-2")
        preset_data = find_template(df,size,bg_color,position,ring_color)
        print("level-1")
        print(preset_data.iloc[0]["template_location"])

        font_size_chart =  preset_data.iloc[0]["const_font_size"][font_size_chart]

        generate_config(ra,dec,f"{orderid}",preset_data.iloc[0]["map_type"],preset_data.iloc[0]["size_cms"],"schfiles",font_size_chart)
        print("level0")

        clean_crop(f"charts",preset_data.iloc[0]["crop_coords"],f"{orderid}.png")
        print("level1")

        add_chart_background(f"cropped-image/{orderid}.png",f"cropped-image-underlayed/{orderid}.png",chart_background_image)
        print("level2")

        merge(f"media/{preset_data.iloc[0]['template_location']}.png",f"cropped-image-underlayed/{orderid}.png",f"output/{orderid}.png",preset_data.iloc[0]["resize"],preset_data.iloc[0]["position_chart"],background_image)
        print("level3")

        text_write(f"output/{orderid}.png",preset_data.iloc[0]["line_coord"],location,title_text,date,time,font_color,f"output/{orderid}.png",size)
        print("level4")

        
        image_url = f'/get_image/{orderid}'
        # Return a success response
        return jsonify({'success': True,"image_url":image_url}), 200

    except Exception as e:
        # Handle unexpected exceptions
        return jsonify({'error': str(e)}), 500

@app.route('/get_image/<orderid>')
def get_image(orderid):
    try:
        image_path = os.path.join('output', f'{orderid}.png')

        # Check if the file exists
        if not os.path.isfile(image_path):
            return jsonify({'error': 'Image not found'}), 404

        # Read the file content
        with open(image_path, 'rb') as file:
            image_data = file.read()

        # Set the appropriate content type for PNG images
        response_headers = {'Content-Type': 'image/png'}

        # Return the image data with the appropriate headers
        return image_data, 200, response_headers

    except FileNotFoundError:
        return jsonify({'error': 'Image not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
