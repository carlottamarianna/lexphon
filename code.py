""" 

At each trial, the participants hear a word/nonword and
they must press a key as quickly as possible when they hear the target phoneme.
"""

import random
import pandas
import csv
from expyriment import design, control, stimuli

operatie = 'operatie.wav'
opelakoe = 'opelakoe.wav'


N_TRIALS = 20
MIN_WAIT_TIME = 1000
MAX_WAIT_TIME = 2000
MAX_RESPONSE_DELAY = 2000

exp = design.Experiment(name="Phonological Detection", text_size=40)
#control.set_develop_mode(on=True)
control.initialize(exp)


target1 = stimuli.Audio(operatie)
target2 = stimuli.Audio(opelakoe)



blankscreen = stimuli.BlankScreen()

targlist = [target1,target2] *(N_TRIALS //2)
random.shuffle(targlist)

words = [target1]
pseudos = [target2]


#if item in targlist == :
    #trials.append(("W", item, stimuli.TextLine(item)))
#else:
    #trials.append(("P", item, stimuli.TextLine(item)))

instructions = stimuli.TextScreen("Instructions",
    f"""From time to time, you will hear a word or a non-word.

    Your task is to press the SPACEBAR as quickly as possible when you hear the /p/ sound (We measure your reaction-time).

    Press the spacebar to hear the sound, then press again the spacebar to start the experiment.""")
    
    #example.plot(instructions)

exp.add_data_variable_names(['trial', 'wait', 'respkey', 'RT', 'word/pseudo'])

control.start(skip_ready_screen=True)
instructions.present()
exp.keyboard.wait()
#present sound here
#exp.keyboard.wait()

results = []


for i_trial in range(N_TRIALS):
    blankscreen.present()
    waiting_time = random.randint(MIN_WAIT_TIME, MAX_WAIT_TIME)
    exp.clock.wait(waiting_time)
    target3 = targlist[i_trial]
    target3.present()
    key, rt = exp.keyboard.wait(duration=MAX_RESPONSE_DELAY)
    if target3 in words:
        item = "WWW"
    elif target3 in pseudos:
        item = "PPP"
    else:
        item = "NA"
    exp.data.add([i_trial, waiting_time, key, rt, item])
    results.append([i_trial, waiting_time, key, rt, item])

with open('lexphon_results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['trial', 'wait', 'respkey', 'RT', 'word/pseudo'])
        writer.writerows(results)



control.end()
