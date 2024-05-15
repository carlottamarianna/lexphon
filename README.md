# lexphon
""" 

At each trial, the participants hear a word/nonword and
they must press a key as quickly as possible when they hear the target phoneme.
"""

import random
import pandas
import csv
from expyriment import design, control, stimuli

example = 'example.wav'
operatie = 'operatie.wav'
opelakoe = 'opelakoe.wav'
episode = 'episode.wav'
apozabe = 'apozabe.wav'
sinaasappel = 'sinaasappel.wav'
zimaafopper = 'zimaafopper.wav'



N_TRIALS = 20
MIN_WAIT_TIME = 1000
MAX_WAIT_TIME = 2000
MAX_RESPONSE_DELAY = 2000

exp = design.Experiment(name="Phonological Detection", text_size=40)
#control.set_develop_mode(on=True)
control.initialize(exp)

ex = stimuli.Audio(example)
target1 = stimuli.Audio(operatie)
target2 = stimuli.Audio(opelakoe)
target3 = stimuli.Audio(episode)
target4 = stimuli.Audio(apozabe)
target5 = stimuli.Audio(sinaasappel)
target6 = stimuli.Audio(zimaafopper)



blankscreen = stimuli.BlankScreen()

targlist = [target1,target2, target3, target4, target5, target6] *(N_TRIALS //2)
random.shuffle(targlist)

words = [target1, target3, target5]
pseudos = [target2, target4, target6]

before_UP = [target1, target2, target3, target4]
after_UP = [target5, target6]



instructions = stimuli.TextScreen("Instructions",
    f"""From time to time, you will hear a word or a non-word.

    Your task will be to press the SPACEBAR as quickly as possible when you hear the /p/ sound (we measure your reaction-time).

    Now press the spacebar to hear an example of the /p/ sound. 
    (Please note that in this example you will hear the  sound accompanied by a random vowel, while in the actual experiment you will just have to look for the consonantal sound). 
    

    When you have finished listening to the example, press again the spacebar to start the experiment.""")
   

exp.add_data_variable_names(['trial', 'wait', 'respkey', 'RT', 'word/pseudo', 'where'])

control.start(skip_ready_screen=True)
instructions.present()
exp.keyboard.wait()
ex.present()
exp.keyboard.wait()

results = []


for i_trial in range(N_TRIALS):
    blankscreen.present()
    waiting_time = random.randint(MIN_WAIT_TIME, MAX_WAIT_TIME)
    exp.clock.wait(waiting_time)
    target = targlist[i_trial]
    target.present()
    key, rt = exp.keyboard.wait(duration=MAX_RESPONSE_DELAY)
    if target in words:
        item = "WORD"
    elif target in pseudos:
        item = "PSEUDO"
    else:
        item = "NA"

    if target in before_UP:
        where = "before UP"
    elif target in after_UP:
        where = "after UP"
    else:
        where = "NA"
        
    exp.data.add([i_trial, waiting_time, key, rt, item, where])
    results.append([i_trial, waiting_time, key, rt, item, where])

with open('lexphon_results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['trial', 'wait', 'respkey', 'RT', 'word/pseudo', 'where'])
        writer.writerows(results)



control.end()
