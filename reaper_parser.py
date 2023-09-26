import sys
import os
import json
from reaper_python import * 

def msg(m):
    RPR_ShowConsoleMsg(str(m) + "\n")
    
def get_curr_project_info(proj, infoName, id3):
  return RPR_GetSetProjectInfo_String(proj, infoName, id3, False)[3]
  
def get_path_input():
  return RPR_GetUserInputs("JSON path", 1, "Path to output JSON file: ", "", 512)


RPR_ClearConsole()
proj = RPR_EnumProjects(-1, "", 512)
if proj[2] == "":
  msg("Unsaved project!")
else:
  data = {}
  data['Project Info'] = {
      'Project Name': get_curr_project_info(proj, 'PROJECT_NAME',''),
      'Project Path': proj[2],
      'Project Title': get_curr_project_info(proj, 'PROJECT_TITLE',''),
      'Project Author': get_curr_project_info(proj, 'PROJECT_AUTHOR',''),
      'Artist Name': get_curr_project_info(proj, 'RENDER_METADATA','ID3:TPE1'),
      'Album Name': get_curr_project_info(proj, 'RENDER_METADATA','ID3:TALB'),
      'Song Number': get_curr_project_info(proj, 'RENDER_METADATA','ID3:TRCK'),
      'Genre': get_curr_project_info(proj, 'RENDER_METADATA','ID3:TCON'),
      'Tempo': RPR_Master_GetTempo()
  }
  data['Tracks'] = []  
  for i in range(RPR_CountTracks(proj)):
    currTrack = {}
    track = RPR_GetTrack(proj, i)
    currTrack['Track Info'] = {
      'Track Number': i,
      'Track Name': RPR_GetTrackName(track,"",512)[2]
    }
    currTrack['Used VSTs'] = []
    for j in range(RPR_TrackFX_GetCount(track)):
      currVST = {}
      currVST['VST Info'] = {
        'VST Number': j,
        'VST Name': RPR_TrackFX_GetFXName(track,j,"",512)[3]
      }
      currVST['Params'] = []
      for c in range(RPR_TrackFX_GetNumParams(track,j)): 
        currVST['Params'].append(RPR_TrackFX_GetParamName(track,j,c,"",512)[4])
      currTrack['Used VSTs'].append(currVST)
    data['Tracks'].append(currTrack)

  output_path = get_path_input()[4]
  if os.path.isdir(output_path):
    with open(output_path + "data.json", "w", encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent=4)
