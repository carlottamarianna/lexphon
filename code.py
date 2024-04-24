""" 

At each trial, the participants hear a word/nonword and
they must press a key as quickly as possible.
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

exp = design.Experiment(name="Visual Detection", text_size=40)
#control.set_develop_mode(on=True)
control.initialize(exp)


target1 = stimuli.Audio(operatie)
target2 = stimuli.Audio(opelakoe)

#words = [operatie]
#pseudos = [opelakoe]

#trials = []
#for item in words:
    #trials.append(("W", item, stimuli.TextLine(item)))
#for item in pseudos:
    #trials.append(("P", item, stimuli.TextLine(item)))

##random.shuffle(trials)

blankscreen = stimuli.BlankScreen()

targlist = [target1,target2] *(N_TRIALS //2)
random.shuffle(targlist)

instructions = stimuli.TextScreen("Instructions",
    f"""From time to time, you will hear a word or a non-word.

    Your task is to press the SPACEBAR as quickly as possible when you hear the /p/ sound (We measure your reaction-time).

    There will be {N_TRIALS} trials in total.

    Press the spacebar to start.""")

exp.add_data_variable_names(['trial', 'wait', 'respkey', 'RT'])

control.start(skip_ready_screen=True)
instructions.present()
exp.keyboard.wait()




for i_trial in range(0,7):
    blankscreen.present()
    waiting_time = random.randint(MIN_WAIT_TIME, MAX_WAIT_TIME)
    exp.clock.wait(waiting_time)
    target3 = targlist[i_trial]
    target3.present()
    key, rt = exp.keyboard.wait(duration=MAX_RESPONSE_DELAY)
    exp.data.add([i_trial, waiting_time, key, rt])
    with open('lexphon_results.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['trial', 'wait', 'respkey', 'RT'])
        writer.writerow([i_trial, waiting_time, key, rt])


control.end()
