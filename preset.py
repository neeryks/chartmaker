

def presets(data):
    preset_dict = {
        "CWB":{"font_color":"Black",
               "chart_color":"White",
               "chartbg_color":"complex",
               },
        "CBB":{"font_color":"White",
               "chart_color":"White",
               "chartbg_color":"complex",
               },
        "SWB":{"font_color":"Black",
               "chart_color":"Black",
               "chartbg_color":"white",
               },
        "SBB":{"font_color":"White",
               "chart_color":"White",
               "chartbg_color":"black",
               }
    }
    return preset_dict[data]

def presets_size(data):
    preset_dict = {
        "A4":{"size":21,
               "width":21,
               "height":29.7,
               "crop_coords":(66,30,886,850),
               },
       "A3":{"size":29.7,
               "width":29.7,
               "height":42,
               "crop_coords":(68,30,1228,1190),
               },
       "DG":{"size":55,
               "width":55,
               "height":77.68,
               "crop_coords":(68,30,1228,1190),
               },
       
        
    }
    return preset_dict[data]

def presets_merge(data):
    preset_dict={
       "A3CWB":{
              "position":(80,100),
              "type":"White",
              "path":"chartmaker/media/A3White.png",
              "resize":(700,700),
              "line_coord":[900, 1000, 1030]
              },
       "A3CBB":{
              "position":(80,100),
              "type":"Black",
              "path":"chartmaker/media/A3Black.png",
              "resize":(700,700),
              "line_coord":[900, 1020, 1050]
              },
       "A3SBB":{
              "position":(80,100),
              "type":"White",
              "path":"chartmaker/media/A3Black.png",
              "resize":(700,700),
              "line_coord":[900, 1020, 1050]
              },
       "A3SWB":{
              "position":(80,100),
              "type":"White",
              "path":"chartmaker/media/A3White.png",
              "resize":(700,700),
              "line_coord":[900, 1020, 1050]
              },
       "A4CWB":{
              "position":(50,70),
              "type":"White",
              "path":"chartmaker/media/A4White.png",
              "resize":(500,500),
              "line_coord":[630, 720, 750]
              },
       "A4CBB":{
              "position":(50,70),
              "type":"Black",
              "path":"chartmaker/media/A4Black.png",
              "resize":(500,500),
              "line_coord":[630, 720, 750]
              },
       "A4SBB":{
              "position":(50,70),
              "type":"White",
              "path":"chartmaker/media/A4Black.png",
              "resize":(500,500),
              "line_coord":[630, 720, 750]
              },
       "A4SWB":{
              "position":(50,70),
              "type":"White",
              "path":"chartmaker/media/A4White.png",
              "resize":(500,500),
              "line_coord":[630, 720, 750]
              },
       "DGCWB":{
              "position":(80,100),
              "type":"White",
              "path":"chartmaker/media/A3White.png",
              "resize":(700,700),
              "line_coord":[900, 1000, 1030]
              },
       "DGCBB":{
              "position":(80,100),
              "type":"Black",
              "path":"chartmaker/media/A3Black.png",
              "resize":(700,700),
              "line_coord":[900, 1020, 1050]
              },
       "DGSBB":{
              "position":(80,100),
              "type":"White",
              "path":"chartmaker/media/A3Black.png",
              "resize":(700,700),
              "line_coord":[900, 1020, 1050]
              },
       "DGSWB":{
              "position":(200,300),
              "type":"White",
              "path":"chartmaker/media/A3White.png",
              "resize":(700,700),
              "line_coord":[900, 1020, 1050]
              },
    
    }
    return preset_dict[data]