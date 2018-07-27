# -*- coding:utf-8 -*-  
import os
import re 

texture_tag              = "------------texture-----------------"
image_size_tag           = "------------Image Size-----------------"
render_frame_tag         = "------------Render Frame-----------------"
render_format_tag        = "------------Render Format-----------------"
multi_pass_tag           = "------------Multi-Pass-----------------"
camera_tag               = "------------camera-----------------"
rfmesh_name_path_tag     = "------------RFMesh_name_path-----------------"
rfparticle_name_path_tag = "------------RFParticle_name_path-----------------"

def parse_analyze_result():
    with open('./analyse_net.txt', 'r') as f:
        #for line in f.readlines():
        #    extract_texture(line.strip())
        content = f.read()
        
        tex_start_pos = content.find(texture_tag) + len(texture_tag)
        tex_end_pos = content.find(image_size_tag)
        if tex_end_pos != -1 and tex_end_pos != -1:
            parse_texture(content[tex_start_pos:tex_end_pos])
        
def parse_texture(textures):
    items = [item for item in textures.split('\n\n') if item]
    extract_texture(items)

#(21, 'T:\\195_NOVA\\_mg\\Jason\\for_renderbus\\Green_v008\\tex\\3d66Model-364628-2-97_1.jpg')            
def extract_texture(items):
    for item in items:
        r = re.compile(r'\((\d+), (\S+)\)')
        texture = r.split(item)[2]
        if texture.find(':') or texture.find('//'): 
            # is abs path
            if os.path.exists(texture) == False:
                print(texture, "not exists")
                
                
if __name__ == "__main__":
    parse_analyze_result()