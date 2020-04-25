# Requires Python 3.5 or later

# Assumptions
#    This script is run in a directory containing 1 or more csv files
#    Only csv files containing information you want are in this directory

# Output
#    three columns, 'Performance', 'Joke', 'HumanScorePostJokeOnly'
#    HumanScorePostJokeOnly is mean average of all ratings

import os
import glob
import pandas as pd

joke = {"robot_name_joke_2.ogg.wav":1,"gdpr_joke.ogg.wav":2,"siri_backpropagate.ogg.wav":3,"silicon_valley_joke_pt1.wav":4,"silicon_valley_joke_pt2.wav":5,"rent_prices_oregon.ogg.wav":28, "job_joke.ogg.wav":7,"inverse_kinematics_equations.ogg.wav":8,"family_joke.ogg.wav":9,"too_robotic_joke.ogg.wav":10,"c3po_joke.ogg.wav":11,"rosie_joke.ogg.wav":12,"wall-e_joke.ogg.wav":13, "plastic_surgery_joke.ogg.wav":14,"bender_joke.ogg.wav":15,"for_all_my_robots_joke.ogg.wav":16,"white_people_joke.ogg.wav":17,"terminator_joke.ogg.wav":18,"baha_men_joke_oregon.ogg.wav":29, "light_bulb_joke.ogg.wav":20,"robot_tinder_2.ogg.wav":30,"big_chips_joke.ogg.wav":22,"catfish_joke_2.ogg.wav":31,"ip_address_joke_2.ogg.wav":32,"encryption_joke.ogg.wav":25, "robot_sexy_times.ogg.wav":26,"closing_take_jobs.ogg.wav":27,"congratulations_youve_won_joke.wav":33,"congratulations_im_feeling_lucky.wav":34,"power_cord_joke.wav":35, "domain_name_joke.wav":36,"domain_name_dot_com.wav":37,".DS_Store":38,"420_joke.wav":39,"agt":40,"baha_men_india.wav":41,"baha_men_joke.ogg.wav":42,"baha_men_joke_sanfran.wav":43, "boogie.ogg.wav":44,"catfish_joke.ogg.wav":45,"floppy_1.ogg.wav":46,"floppy_2.ogg.wav":47,"floppy_3.ogg.wav":48,"floppy_4.ogg.wav":49,"ganja_1.ogg.wav":50,"ganja_2.ogg.wav":51, "ganja_3.ogg.wav":52,"hahahaha.wav":53,"happy_birthday.wav":54,"happy_birthday_taylor.wav":55,"hot_singles.ogg.wav":56,"human_date_1.ogg.wav":57,"human_date_2.ogg.wav":58, "human_date_3.ogg.wav":59,"human_date_4.ogg.wav":60,"ip_address_joke.ogg.wav":61,"megaman.ogg.wav":62,"plane_0.ogg.wav":63,"plane_1.ogg.wav":64,"plane_2.ogg.wav":65,"plane_3.ogg.wav":66, "plane_4.ogg.wav":67,"plane_5.ogg.wav":68,"rent_prices.ogg.wav":69,"robot_babies.ogg.wav":70,"robot_drugs.ogg.wav":71,"robot_name_joke.ogg.wav":72,"robot_name_joke_1.ogg.wav":73, "robot_tinder.ogg.wav":74,"robotic.aiff":75,"robotic.aiff.wav":76,"self_driving_limo.ogg.wav":77,"selfie_drone.ogg.wav":78,"silence.wav":79,"silicon_valley_joke.ogg.wav":80, "smoking_joke.ogg.wav":81,"software_update.ogg.wav":82,"speech_20180703052826649.ogg.wav":83,"stripper_joke.ogg.wav":84,"stripper_vagina.ogg.wav":85,"stripper_vagina_joke.ogg.wav":86, "tags":87,"test_negative_tag.wav":88,"thank_you_nick.wav":89,"tinder_joke.ogg.wav":90,"training_data.ogg.wav":91,"transformers_1.ogg.wav":92,"transformers_2.ogg.wav":93, "vibrator.ogg.wav":94,"vibrator_pt_2.ogg.wav":95,"walken_1.ogg.wav":96,"walken_2.ogg.wav":97,"washing_machine_1.ogg.wav":98,"washing_machine_2.ogg.wav":99,"washing_machine_3.ogg.wav":100, "tags/catfish_joke_positive.ogg.wav":101, "tags/encryption_joke_positive_2.ogg.wav":102, "tags/family_joke_positive_2.ogg.wav":103, "tags/gdpr_joke_positive.ogg.wav":104, "tags/inverse_kinematics_equations_positive_2.ogg.wav":105, "tags/plastic_surgery_joke_negative.ogg.wav":106, "tags/rent_prices_oregon_negative.ogg.wav":107, "tags/robot_joke_positive.wav":108, "tags/robot_tinder_2_negative.ogg.wav":109, "tags/too_robotic_joke_positive_2.ogg.wav":110, "tags/white_people_joke_positive_2.ogg.wav":111, "tags/inverse_kinematics_equations_negative.ogg.wav":112, "tags/power_cord_joke_negative.wav":113, "tags/killing_tag.wav":114, "tags/power_cord_joke_positive.wav":115, "tags/too_robotic_joke_negative.wav":116, "tags/white_people_joke_negative.ogg.wav":117, "tags/robot_joke_negative_2.ogg.wav":118, "tags/robot_tinder_2_positive.ogg.wav":119, "tags/megaman_positive.ogg.wav":120, "tags/self_driving_limo_positive.ogg.wav":121, "tags/robot_babies_positive.ogg.wav":122, "tags/robot_drugs_positive.ogg.wav":123, "tags/robot_tinder_2_positive.ogg.wav":124, "tags/software_update_positive.ogg.wav":125, "tags/self_driving_limo_negative.ogg.wav":126, "tags/metal_ceiling_positive.ogg.wav":127, "tags/metal_ceiling_positive.ogg.wav":128, "tags/metal_ceiling_positive.ogg.wav":129, "tags/catfish_joke_negative.ogg.wav":130, "tags/encryption_joke_negative_2.ogg.wav":131, "tags/gdpr_joke_negative.ogg.wav":132, "tags/killing_joke_negative.wav":133, "tags/megaman_negative.ogg.wav":134, "tags/robot_drugs_negative.ogg.wav":135, "tags/software_update_negative.ogg.wav":136, "tags/robot_joke_negative.ogg.wav":137, "tags/plastic_surgery_joke_positive_2.ogg.wav":138, "tags/rent_prices_oregon_positive.ogg.wav":139, "tags/training_data_negative.ogg.wav":140, "tags/training_data_positive.ogg.wav":141, "robot_name_joke_1.ogg.wav":142
}
 
performance = {"2019-01-30 Class Performance (Weird)":0, "2019-04-13 Cienna Nerdy Show at The Drake":1,"2019-04-18 Bombs Away Cafe":2, "2019-04-19 Addison Performance (Weird)":3, "2019-04-19 Singu-hilarity":4,"2019-04-22 Class Performance":5, "2019-05-16 Bombs Away Cafe":6,"2019-06-19 Trek Theater":7,"2019-06-20 Bombs Away Cafe":8,"2019-08-15 Bombs Away Cafe":9, "2019-08-15 Phoebe (Weird)":10, "2019-08-23 Spectrum":11,"2019-09-05 Stand-up Science":12, "2019-09-06 Naomi and Sara Laugh at Routine (Weird)":13, "2019-09-06 RoboCom":14,"2019-09-19 Bombs Away Cafe":15,"2019-09-21 Laugh Track Town USA":16, "2019-09-28 OSU Cascades (Weird)":17, "2019-10-11 Singu-hilarity":18,"2019-11-29 Comedy the Musical":19,"2019-11-29 Crapshoot":20,"2019-12-06 Silent Background Recording":21,"2019-12-09 Singu-Hilarity in San Francisco":22, "2020-01-12 Singu-Hilarity in Corvallis":23, "2020-01-25 Sam Bond_s Bleeping Funny":24, "2020-01-29 Class Performance":25, "2020-01-31 Mt Caz":26, "2020-02-19 Soundbox":27, "2020-03-04 Bombs Away":28, 
}

#get all csv files
extension = 'csv'
all_files = [i for i in glob.glob('*.{}'.format(extension))]
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_files ], sort=False)
#remove notes
combined_csv = combined_csv.iloc[:, :-1]
#combine human ratings based on performance and joke
combined_csv = combined_csv.groupby(['Performance', 'Joke']).mean()
#round number
combined_csv['HumanScorePostJokeOnly'] = combined_csv['HumanScorePostJokeOnly'].round(0)
combined_csv = combined_csv.reset_index()[['Performance', 'Joke', 'HumanScorePostJokeOnly']]
#Add performance, joke ids
combined_csv.insert(0, 'PerformanceID', combined_csv['Performance'].map(performance))
combined_csv.insert(2, 'JokeID', combined_csv['Joke'].map(joke))
combined_csv.insert(4, 'HumanScore', combined_csv['HumanScorePostJokeOnly'])
#print to csv
combined_csv.to_csv("combined_ground_truths.csv", index=False)