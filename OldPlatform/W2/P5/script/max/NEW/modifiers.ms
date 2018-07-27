
fn collectmodifierClasses =
(
	
	
	local modifierClasses = #() -- array to hold all the unique modifier names
	local objectSets = #() -- array to hold corresponding object sets

	
	for obj in objects do 
	(
		
		
		for objMod in obj.modifiers do
		(	
			local objModClass=(classOf objMod as string)
			
			if hasProperty objMod "rememberPositions" then (
			--if objModClass=="Ox_Hair_from_Guides"  or objModClass=="Ox_Guides_from_Surface" then (
				format "obj.name=%\n" obj.name
				format "modifierClasses...%___name...%\n" (classOf objMod as string) objMod.name
				
				objMod.rememberPositions=true
					--showproperties objMod
				
			)
			
		)
	)
)

clearlistener()
collectmodifierClasses()



/*

obj.modifier...Ox Hair from Guides
  .method (Distribution_method) : integer
  .uvChannel (UV_Channel) : integer
  .count (Guide_count) : integer
  .useMatID (Use_material_ID) : boolean
  .matID (Material_ID) : integer
  .useSubSel (Use_Sub_Selection) : boolean
  .randSeed (Random_Seed) : integer
  .topoOrient (Topology_based_root_orientation) : boolean
  .rememberPositions (Remember_Root_Positions) : boolean
  .cacheFaces : int array
  .cacheBarycentricCoordinates : point3 array
  .cacheGuideDependencyIndices : int array
  .cacheGuideDependencyWeights : float array
  .rootTopo (Root_topology) : boolean
  .rootTM (Root_transform_matrix) : boolean
  .rootTopo (Surface_dependance) : boolean
  .guideDep (Guide_dependance) : boolean
  .denseCount (Render_Count) : integer
  .instance (Instance_Strands) : boolean
  .interpMeth (Interpolation_Method) : integer
  .interpNum (Interpolation_Number) : integer
  .distrMap (Distribution_Map) : texturemap
  .guideProx (Use_Guide_Proximity) : boolean
  .gpDist (Guide_Proximity_Distance) : float
  .useGuideFaces (Use_guide_faces) : boolean
  .gfIter (Guide_face_iterations) : integer
  .useUVCoords (Use_UV_coordinates) : boolean
  .exportType (Export_object_type) : integer
  .partPts : point3 array
  .partNorm : point3 array
  .autoPart (Auto_part_hair) : boolean
  .apAngThresh (Auto_parting_threshold) : float
  .apDistThresh (Distance_threshold) : float
  .partMap (Parting_map) : texturemap
  .partChan : integer
  .distrChan : integer
  .interpolateLength (Interpolate_Length) : boolean
  .uniformRandomness (Uniform_Randomness) : float

*/