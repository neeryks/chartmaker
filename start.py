
from flask import Flask, request, jsonify,send_file
from coordfinder import get_lat_lon,calculate_zenith_coordinates
from preset import presets,presets_size,presets_merge
from chart_maker import generate_config
from imageeditor import clean_crop, add_chart_background,merge,text_write
import os

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
        required_fields = ['orderid', 'location', 'date', 'time', 'chart_type', 'chart_font', 'title_text']
        for field in required_fields:
            if field not in starchart_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        orderid = starchart_data['orderid']
        location = starchart_data['location']
        date = starchart_data['date']
        time = starchart_data['time']
        size = starchart_data['size']
        chart_type = presets(starchart_data['chart_type'])
        chart_var = starchart_data['chart_type']
        chart_font = starchart_data['chart_font']
        title_text = starchart_data['title_text']

        latitude,longitude = get_lat_lon(location)
        ra,dec = calculate_zenith_coordinates(latitude,longitude,date,time)
        generate_config(ra,dec,f"{orderid}",chart_type['chart_color'],presets_size(size)['size'],"chartmaker/schfiles")
        clean_crop(f"chartmaker/charts/",size,f"{orderid}.png")
        add_chart_background(f"chartmaker/cropped-image/{orderid}.png",chart_type['chartbg_color'],f"chartmaker/cropped-image-underlayed/{orderid}.png")
        merge(presets_merge(f"{size}{chart_var}")['path'],f"chartmaker/cropped-image-underlayed/{orderid}.png",f"chartmaker/output/{orderid}.png",position=presets_merge(f"{size}{chart_var}")['position'],poster_type=f"{size}{chart_var}")
        text_write(f"chartmaker/output/{orderid}.png",presets_merge(f"{size}{chart_var}")['line_coord'],location,title_text,f"{date} {time}",presets(chart_var)['font_color'],f"chartmaker/output/{orderid}.png",size)

        image_url = f'/get_image/{orderid}'
        # Return a success response
        return jsonify({'success': True,"image_url":image_url}), 200

    except Exception as e:
        # Handle unexpected exceptions
        return jsonify({'error': str(e)}), 500

@app.route('/get_image/<orderid>')
def get_image(orderid):
    try:
        image_path = os.path.join('chartmaker', 'output', f'{orderid}.png')

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
    app.run(host='0.0.0.0', port=5000, debug=True)
