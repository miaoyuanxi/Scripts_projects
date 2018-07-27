from Katana import KatanaFile, version, FarmAPI,Nodes3DAPI
import NodegraphAPI,sys,json,os,re

katana_scene = sys.argv[1]
anal_txt = sys.argv[2]
#_tid_from_cmd = sys.argv[2]
#_inf_from_cmd = sys.argv[3]
print katana_scene
print anal_txt
 
def kanana_analyse(katana_scene,anal_txt):


    #yourKatanaScene = "/home/ladaojeiang/yes/demos/katana_files/aovs_prman.katana"
    KatanaFile.Load( katana_scene ) # Loading scene /yourDirectory/yourFile.katana
    #katana_scene=FarmAPI.GetKatanaFileName()
    render_info_dict={}
    render_nodes = NodegraphAPI.GetAllNodesByType("Render")
    #graphState = NodegraphAPI.GetCurrentGraphState()
    if len(render_nodes) != 0:    
        for render_node in render_nodes:
            render_output_dict={}
            render_frame_dict={}
            render_name=render_node.getName() 
            #print render_node.getParameters().getXML()
            scene_name = os.path.basename(os.path.basename(katana_scene))
            print "the rener node name is  %s" % render_name
            num_re =re.compile(r"(\d+_\d+)[\D]*", re.I)
            if num_re.findall(scene_name):
                scene_num = num_re.findall(scene_name)[0]
                if render_name.startswith(scene_num):           
                    render_node.getParameter("lock").setValue(0,0)
                    #render_node_info=Nodes3DAPI.RenderNodeUtil.GetRenderNodeInfo(render_node,graphState)
                    render_node_info=Nodes3DAPI.RenderNodeUtil.GetRenderNodeInfo(render_node)

                    for i in xrange(render_node_info.getNumberOfOutputs()):
                        outputInfo = render_node_info.getOutputInfoByIndex(i, forceLocal=False)
                        
                        render_output_name = outputInfo['name']
                        render_output = outputInfo["outputFile"]
                        print render_output_name,render_output
                        if render_output.find('Temp')>0:
                            
                            print ("the %s output is %s ,it is tmp ,dont copy"  % (render_output_name,render_output))
                        else:                       
                            render_output_dict[render_output_name]=render_output
                    #print render_output_dict



                    #if render_node.getParameter('farmSettings.setActiveFrameRange').getValue(0)=="Yes":
                    render_start= render_node.getParameter('farmSettings.activeFrameRange.start').getValue(0)
                    render_end= render_node.getParameter('farmSettings.activeFrameRange.end').getValue(0)
                    #print range(0,Nodes3DAPI.RenderNodeUtil.GetNumRenderOutputs(render_node))
                    #print Nodes3DAPI.RenderNodeUtil.GetDefaultIncludedOutputs(render_node).keys()
                    render_frame_dict["start"]=render_start 
                    render_frame_dict["end"]=render_end    
                    #print render_start,render_end
                    #print render_frame_dict
                    render_info_dict[render_name]=render_output_dict,render_frame_dict
        print render_info_dict
        anal_txt_handle = file(anal_txt, 'w')
        anal_txt_handle.write(json.dumps(render_info_dict))
        anal_txt_handle.close()
    else:
        print 'the render node 0, analysis failed!'
        if  os.path.exists(anal_txt):
            os.remove(anal_txt)
        sys.exit(1)
        #render_info_dict["failed"]='the render node 0, analysis failed!'
        #print render_info_dict

kanana_analyse(katana_scene,anal_txt)