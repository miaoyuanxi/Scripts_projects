require 'sketchup'
require 'logger'

#2016-06-28 version 1.0

module SketchupSubmitModule

    def openprojectfile
        outputLog("start...")
        # $OpenFile, $Page_name, $Width, $Height, $Total_Frame, $$output_directory ,$output_name, $format, $Total_time, $use_vray
        begin
            outputLog("startup  sketchup.exe")
            Sketchup.active_model.save("C:/null")
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
    end

    def getFileInfo
        outputLog("")
        outputLog("------------------------[openfile info]------------------------")
        openprojectfile
        
        outputLog("")
        outputLog("------------------------[get render parameter info]------------------------")
        outputLog("start...")
        $model=Sketchup.active_model
        $view=$model.active_view
        $pages=$model.pages
        $total_time=$pages.slideshow_time
        $SketchUp_version=Sketchup.version
        
        if $use_vray=="True"
            outputLog("render:VRay-rander")
            outputLog("get VRay-version info")
            $Render_version=VRayForSketchUp.getVRayForSketchUpVersion
            outputLog("get VRay-width info")
            $width=VRayForSketchUp.get_option_value("/SettingsOutput", "img_width", "integer")
            outputLog("get VRay-height info")
            $height=VRayForSketchUp.get_option_value("/SettingsOutput", "img_height", "integer")
            outputLog("get VRay-output path info")
            $output_file=VRayForSketchUp.get_option_value("/SettingsOutput", "img_file", "string")
            if $output_file==""
                $output_file=File.basename( $model.path,".skp" )+".png"
            end
            outputLog("get VRay-save_alpha_separate info")
            $save_alpha_separate=VRayForSketchUp.get_option_value("/SettingsOutput", "img_separateAlpha", "bool")
            outputLog("get VRay-animation_on info")
            $animation_on=VRayForSketchUp.get_option_value("/SettingsOutput", "do_animation", "bool")            
            if $animation_on==true
                $frame_rate=VRayForSketchUp.get_option_value("/SettingsOutput", "frames_per_second", "float")
                $total_Frame=$total_time*$frame_rate
            else
                $frame_rate="0"
                $total_Frame="1"
            end
            outputLog("get VRay-render_only_specified_frames info")
            $render_only_specified_frames=VRayForSketchUp.get_option_value("/SettingsOutput", "render_frame_range", "bool")
            
            #Irradiance_map--------------------------------------------
            outputLog("get VRay-irradiance_mode_type info")
            $irradiance_mode_num=VRayForSketchUp.get_option_value("/SettingsIrradianceMap", "mode", "integer")
            if $irradiance_mode_num==0
                $irradiance_mode_type="Single Frame"
            elsif $irradiance_mode_num==4
                $irradiance_mode_type="Incremental add to current map"
            elsif $irradiance_mode_num==5
                $irradiance_mode_type="Bucket mode"
            else $irradiance_mode_num==2
                $irradiance_mode_type="From File"  
                $irradianceMap_From_file=VRayForSketchUp.get_option_value("/SettingsIrradianceMap", "file", "string")
            end
            
            #light_cache_map-------------------------------------
            outputLog("get VRay-lightcache_mode_type info")
            $Lightcache_mode_num=VRayForSketchUp.get_option_value("/SettingsLightCache", "mode", "integer")
            if $Lightcache_mode_num==0
                $lightcache_mode_type="Single frame"
            elsif $Lightcache_mode_num==1
                $lightcache_mode_type="Fly-through"
            elsif $Lightcache_mode_num==2
                $lightcache_mode_type="From file"
                $lightCache_From_file=VRayForSketchUp.get_option_value("/SettingsLightCache", "file", "string")
            else $Lightcache_mode_num==3
                $lightcache_mode_type="Progressive path tracing" 
            end
            
        else
            outputLog("render: default Render")
            $Render_version="default Render"
        end

        $file_name=File.basename( $model.path )
        outputLog("start...")
        
        #print view log-------------------------------------------------- 
        outputLog("")
        outputLog("------------------------[output get info]------------------------")
        if $use_vray=="True"
            outputLog("output get vrayrender parameter info")
            outputLog("start...")
            aFile = File.new($outputinfo,"w")
            
            aFile.puts "SketchUp_version: #{$SketchUp_version}"
            aFile.puts "Render_version: VRay #{$Render_version}" 
            aFile.puts "openfile: #{$openfile}"
            aFile.puts "file_name: #{$file_name}"
            
            if $pages[0]==nil 
                aFile.puts "There is no page labels"
            else
                page_Array=[]
                for page in $pages                
                    page_Array.push(page.name)
                end
                $pageName=page_Array
                aFile.puts "Page_name: #{$pageName}"
            end
            
            aFile.puts "width: #{$width}"
            aFile.puts "height: #{$height}"
            aFile.puts "total_Frame: #{$total_Frame.to_i}"
            aFile.puts "output_file: #{$output_file}"
            aFile.puts "save_alpha_separate: #{$save_alpha_separate}"
            aFile.puts "animation_on: #{$animation_on}"
            aFile.puts "frame_rate: #{$frame_rate}"
            aFile.puts "total_time: #{$total_time}"
            aFile.puts "render_only_specified_frames: #{$render_only_specified_frames}"
            aFile.puts "irradiance_mode_type: #{$irradiance_mode_type}"
            aFile.puts "irradianceMap_From_file: #{$irradianceMap_From_file}"
            aFile.puts "lightcache_mode_type: #{$lightcache_mode_type}"
            aFile.puts "lightCache_From_file: #{$lightCache_From_file}"
            
            aFile.close
            outputLog("end...")
        else
            outputLog("output get defaultrender parameter info")
            outputLog("start...")
            aFile = File.new($outputinfo,"w")
            aFile.puts "SketchUp_version: #{$SketchUp_version}"
            aFile.puts "Render_version: #{$Render_version}" 
            aFile.puts "openfile: #{$openfile}"
            aFile.puts "file_name: #{$file_name}"
            aFile.close
            outputLog("end...")
        end

        close_sketchup
        outputLog("finished...")
        outputLog("It is OK!")
    end

    def is_win?
        (/cygwin|mswin|mingw|bccwin|wince|emx/ =~ RUBY_PLATFORM) != nil # Windows
    end

    def close_sketchup 
        if is_win?
            Sketchup.send_action(57665) # todo: always check this works on SU/ruby version updates (must be v7 or higher )
            $model.save("C:/null")
        else # unsupported platform
            puts "Error: Platform \"#{RUBY_PLATFORM}\" is not supported by SketchUp"
            return false
        end
    end
    
    def outputLog(str)
        my_log = Logger.new("#{$logpath}")
        my_log.formatter = proc { |severity, datetime, progname, msg |"#{datetime}: #{msg}\n" }
        my_log.info(str)
    end
   
end


