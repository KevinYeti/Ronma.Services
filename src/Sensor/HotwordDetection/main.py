from res import snowboydecoder
import os, sys
import signal

# Demo code for listening to two hotwords at the same time

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) < 2:
    print("Error: need to specify model names and sensitivity")
    print("Usage: python main.py 0.5")
    sys.exit(-1)

sensitivity = sys.argv[1]
files = os.listdir("./res/*.*mdl")
models = sys.argv[2:]



# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = sensitivity*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
callbacks = []
for i in range(len(models)):
    callbacks.append(lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING))

print('Listening... Press Ctrl+C to exit')

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()