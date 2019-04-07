from lib import snowboydecoder_arecord
import os
import sys
import time
import signal
from pixel_ring import pixel_ring
import mraa

#
interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


def detected_callback():
    snowboydecoder_arecord.play_audio_file
    pixel_ring.listen()


def main():
    if len(sys.argv) < 2:
        print("Error: need to specify sensitivity")
        print("Usage: python main.py 0.36")
        sys.exit(-1)

    #pixel_ring
    en = mraa.Gpio(12)

    if os.geteuid() != 0:
        time.sleep(1)

    en.dir(mraa.DIR_OUT)
    en.write(0)

    pixel_ring.set_brightness(20)
    pixel_ring.change_pattern('echo')

    files = os.listdir("./res/*.*mdl")
    models = files

    sensitivity = sys.argv[1] * models.count()
    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    detector = snowboydecoder_arecord.HotwordDetector(models, sensitivity=sensitivity, audio_gain=2)
    print('Listening... Press Ctrl+C to exit')

    # main loop
    detector.start(detected_callback=detected_callback,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)

    pixel_ring.off()
    time.sleep(1)
    en.write(1)
    detector.terminate()


if __name__ == "__main__":
    main()
