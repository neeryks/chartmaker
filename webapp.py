import gradio as gr
import requests
import uuid
import os
from datetime import datetime

API_KEY = "Kill"
RECEIVE_DATA_ENDPOINT = "http://192.168.1.6:5003/receive_data"
SERVER_URL = "http://192.168.1.6:5003"


def generate_star_map(location, date, time, size, position, font_color, ring_color, title_text, font_size_chart, bg_color, background_image, chart_bg_color, chart_background_image):
    order_info = {
        "orderid": str(uuid.uuid4()),
        "location": location,
        "date": "-".join(date.split("-")[::-1]),
        "time": time,
        "size": size,
        "position": position,
        "bg_color": bg_color,
        "font_color": font_color,
        "ring_color": ring_color,
        "title_text": title_text,
        "font_size_chart": font_size_chart,
        "chart_background_image": "",
        "background_image": ""
    }

    if bg_color == "Photo" and background_image is not None:
        order_info["bg_color"] = "T"
        order_info["background_image"] = background_image
    elif bg_color == "White":
        order_info["bg_color"] = "W"
    elif bg_color == "Black":
        order_info["bg_color"] = "B"

    if chart_bg_color == "Photo" and chart_background_image is not None:
        order_info["chart_background_image"] = chart_background_image
    elif chart_bg_color == "Transparent":
        order_info["chart_background_image"] = "media/transparent.png"
    elif chart_bg_color == "Black":
        order_info["chart_background_image"] = ""

    if position == "Top":
        order_info["position"] = "T"
    elif position == "Center":
        order_info["position"] = "C"

    if ring_color == "White":
        order_info["ring_color"] = "W"
    elif ring_color == "Black":
        order_info["ring_color"] = "B"

    if font_color == "White":
        order_info["font_color"] = "white"
    elif font_color == "Black":
        order_info["font_color"] = "black"

    print(order_info)
    
    headers = {"Authorization": f"{API_KEY}", "Content-Type": "application/json"}
    response = requests.post(RECEIVE_DATA_ENDPOINT, json=order_info, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if 'image_url' in response_data:
            full_image_url = f"{SERVER_URL}{response_data['image_url']}"
            return full_image_url
        else:
            return "Failed to generate star map. Please try again later."
    else:
        return f"Failed to send order info. Status code: {response.status_code}, Response: {response.text}"

def main():
    with gr.Blocks() as demo:
        gr.Markdown("## Star Map Generator @neeryks")

        with gr.Row():
            location = gr.Textbox(label="Location", placeholder="Enter the location of the event")
            date = gr.Textbox(label="Date (DD-MM-YYYY)", placeholder="Enter the date of the event in DD-MM-YYYY format")
            time = gr.Textbox(label="Time (HH:MM:SS)", placeholder="Enter the time of the event in HH:MM:SS format")

        font_size_chart = gr.Radio(choices=["S", "M", "L"], label="Font Size for Chart")
        size = gr.Radio(choices=["A3", "A4"], label="Size")
        position = gr.Radio(choices=["Top", "Center"], label="Chart Position")
        font_color = gr.Radio(choices=["White", "Black"], label="Font Color")
        ring_color = gr.Radio(choices=["White", "Black"], label="Ring Color")
        title_text = gr.Textbox(label="Title Text", placeholder="Enter the title text (max 20 characters)")

        bg_color = gr.Radio(choices=["White", "Black", "Photo"], label="Background Color")
        background_image = gr.File(label="Upload Background Image ( 3508px X 4961px )", visible=False)

        def toggle_upload_bg(bg_choice):
            return gr.update(visible=(bg_choice == "Photo"))

        bg_color.change(fn=toggle_upload_bg, inputs=bg_color, outputs=background_image)

        chart_bg_color = gr.Radio(choices=["Black", "Transparent", "Photo"], label="Chart Background Color")
        chart_background_image = gr.File(label="Upload Chart Background Image (2395px X 2395px Only)", visible=False)

        def toggle_upload_chart_bg(chart_bg_choice):
            return gr.update(visible=(chart_bg_choice == "Photo"))

        chart_bg_color.change(fn=toggle_upload_chart_bg, inputs=chart_bg_color, outputs=chart_background_image)

        submit = gr.Button("Generate Star Map")
        output = gr.Image(label="Generated Star Map")

        submit.click(
            fn=generate_star_map, 
            inputs=[
                location, date, time, size, 
                position, font_color, ring_color, title_text, 
                font_size_chart, bg_color, background_image,
                chart_bg_color, chart_background_image
            ],
            outputs=output
        )

    demo.launch(share=True)

if __name__ == "__main__":
    main()
