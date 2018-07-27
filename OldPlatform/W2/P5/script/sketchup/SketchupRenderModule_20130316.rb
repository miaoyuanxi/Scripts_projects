require 'sketchup'
require 'logger'

module SketchupRenderModule

    def render_vray
        begin
            outputLog("start... VRay rendering image")
            outputLog("modify output_directory path")
            if $total_frame==1
                outputLog("render mode:single frame")
                outputLog(""+"set img_separateAlpha:true"+"")
                VRayForSketchUp.set_option_value("/SettingsOutput", "img_separateAlpha", "bool",true)
                #outputLog(""+"set do_animation:false"+"")
                #VRayForSketchUp.set_option_value("/SettingsOutput", "do_animation", "bool", false)
                outputLog("outputfile:"+""+$output_directory+$output_name+".0000" + "#{$format}" +"")
                VRayForSketchUp.setOutputPath(""+$output_directory+$output_name+".0000" + "#{$format}" +"")
                VRayForSketchUp.setOutputSize($width, $height)
                VRayForSketchUp.launch_vray_render 
            else
                outputLog("render mode:sequence image")
                outputLog("update view to currentFrame view")
                $currentview=$total_time/$total_frame
                $pages.show_frame_at $currentview*$currentframe
                outputLog(""+"set img_separateAlpha:true"+"")
                VRayForSketchUp.set_option_value("/SettingsOutput", "img_separateAlpha", "bool",true)
                outputLog(""+"set do_animation:false"+"")
                VRayForSketchUp.set_option_value("/SettingsOutput", "do_animation", "bool", false)
                outputLog("outputfile:"+""+$output_directory+$output_name+".000"+ $currentframe.to_s + "#{$format}" +"")
                VRayForSketchUp.setOutputPath(""+$output_directory+$output_name+".000"+ $currentframe.to_s + "#{$format}" +"")
                VRayForSketchUp.setOutputSize($width, $height)
                VRayForSketchUp.launch_vray_render 
            end
            outputLog("end... VRay rendering image")
        rescue
            outputLog("error:VRay render Failed")
        end
    end

    # renders current view as image
    def render_image
        outputLog("")
        outputLog("------------------------[render info]------------------------")
        outputLog("start...")
        outputLog("SU_PROGRESS 0%")    
        $output_path = File.join( $output_directory, $output_name +".000" +"#{$format}" )
        begin
            if $use_vray == "True"
                render_vray
            else
                outputLog("start... default exporting 2d image")
                $view.write_image( $output_path, $width, $height )
                outputLog("end... default exporting 2d image")
            end
        rescue
            outputLog("Error: Failed to write image: #{$output_path}, check input and folder permissions")
            close_sketchup
        end
        
        outputLog("SU_PROGRESS 100%")
        outputLog("Finished rendering image to #{$output_path}")
            
        #make sketchup wait for vray to finish render before close
        if $use_vray == "True"
            outputLog("waiting VRay render finished")
            VRayForSketchUp.registerCb("Nill","renderFinished","close_sketchup")
            outputLog("shutdown sketchup.exe")
        else
            close_sketchup
            outputLog("shutdown sketchup.exe")
        end
        outputLog("start...")
        outputLog("render finished...")
        outputLog("it is OK!")
    end

    def is_win?
        (/cygwin|mswin|mingw|bccwin|wince|emx/ =~ RUBY_PLATFORM) != nil # Windows
    end

    def close_sketchup # SketchUp 2014 has Sketchup.quit
        if is_win?
            Sketchup.send_action(57665) # todo: always check this works on SU/ruby version updates (must be v7 or higher )
            $model.save("C:/null")
        else # unsupported platform
            outputLog("Error: Platform \"#{RUBY_PLATFORM}\" is not supported by SketchUp")
            return false
        end
    end

    def outputLog(str)
        my_log = Logger.new("#{$logpath}")
        my_log.formatter = proc { |severity, datetime, progname, msg |"#{datetime}: #{msg}\n" }
        my_log.info(str)
    end


    def readyfile
        outputLog("")
        outputLog("------------------------[delete page info]------------------------")
        outputLog("start ... ")
        $pages=Sketchup.active_model.pages
        if $pages.count==0
            outputLog("pages is not existed ")
        else
            #oldPages=["Scene 1","Scene 2","Scene 3"] 
            outputLog("delete don't render page ")
            oldpages=[]
            for page in $pages
                oldpages.push(page.name)
            end
            outputLog("filepages:"+"#{oldpages}")
            deletepage=oldpages-$page_name
            outputLog("renderpages:"+"#{$page_name}")
            aa=[]
            for pp in $pages
                for arrnew in deletepage
                    puts arrnew
                    puts pp.name
                    if pp.name==arrnew
                        aa.push(pp)
                    end   
                end  
            end 
            for hh in aa
                puts hh.name
                $pages.erase(hh)    
            end
            outputLog("delete #{deletepage} successed ")
        end
        outputLog("end ... ")
    end

       
    def main
        #show_p = `tasklist`
        #system('tskill SketchUp') if show_p.include? 'SketchUp' 
        
        $model = Sketchup.active_model
        $view = $model.active_view
        $pages = $model.pages
        
        outputLog("")
        outputLog("------------------------[openfile info]------------------------")
        outputLog("start...")
        # $OpenFile, $Page_name, $Width, $Height, $Total_Frame, $$output_directory ,$output_name, $format, $Total_time, $use_vray
        begin
            outputLog("startup  sketchup.exe")
            $model.save("C:/null")
            #$openfile = "E:/Sketchup_qsy/scene/SU.skp"
            outputLog("start Open the file")
            Sketchup.open_file $openfile
            Sketchup.send_action(10597)
            outputLog("Open the file successfully")
        rescue
            outputLog("Open the file error")
            close_sketchup
        end
        outputLog("end...")
        
        outputLog("")
        outputLog("------------------------[project file info]------------------------")
        outputLog(""+"openfile:"+"#{$openfile}"+"")
        outputLog(""+"page_name:"+"#{$page_name}"+"")
        outputLog(""+"width:"+"#{$width}"+"")
        outputLog(""+"height:"+"#{$height}"+"") 
        outputLog(""+"total_frame:"+"#{$total_frame}"+"(s)""") 
        outputLog(""+"total_time:"+"#{$total_time}"+"") 
        outputLog(""+"currentframe:"+"#{$currentframe}"+"") 
        outputLog(""+"output_directory:"+"#{$output_directory}"+"") 
        outputLog(""+"output_name:"+"#{$output_name}"+"") 
        outputLog(""+"format:"+"#{$format}"+"") 
        outputLog(""+"use_vray:"+"#{$use_vray}"+"") 
        
        if $format==""
            $format=".png"
        end
        
        if $output_name==""
            $output_name=File.basename($model.path,".skp")
        end
        
        #$width = 640
        #$height = 360
        #$total_frame=120    
        #$total_time=4.0   
        #$currentframe=40
        #$output_directory = "E:/Sketchup_qsy/output"        
        #$output_name = "ceshi"
        #$format = ".png"   
        #$use_vray = "True"
        
        readyfile
        render_image
    end   
end

