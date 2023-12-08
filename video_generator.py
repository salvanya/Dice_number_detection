from function import dice_number_detector

video_paths_and_output = {"tirada_1.mp4" : "resultado_tirada_1.mp4", 
                          "tirada_2.mp4" : "resultado_tirada_2.mp4", 
                          "tirada_3.mp4" : "resultado_tirada_3.mp4", 
                          "tirada_4.mp4" : "resultado_tirada_4.mp4"}

for video_path in video_paths_and_output.keys():
    dice_number_detector(video_path, video_paths_and_output[video_path])

