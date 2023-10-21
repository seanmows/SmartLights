import functools
import signal
from time import sleep

from nanoleafapi import (
    Nanoleaf,NanoleafDigitalTwin, RED, ORANGE, YELLOW, GREEN, LIGHT_BLUE, BLUE, PINK, PURPLE, WHITE
)

WEATHER_TO_COLORS = {'Rain' : BLUE, 'Drizzle': LIGHT_BLUE, "Snow": PINK, "Atmoshphere": RED, "Thunderstorm": YELLOW, "COLD": PURPLE, "HOT":ORANGE, "GOOD": GREEN}
IP = "192.168.1.184"
WEATHER_PANEL_ID = 53557
MAX_TIMEOUT = 20

def timeout(seconds):
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            def handle_timeout(signum, frame):
                raise TimeoutError()

            signal.signal(signal.SIGALRM, handle_timeout)
            signal.alarm(seconds)

            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                print("An exception occurred:", str(e))
            finally:
                signal.alarm(0)  # Reset the alarm

        return wrapper
    return decorator

@timeout(MAX_TIMEOUT)
def turn_on_goal_effect(effect: str, length=10):
    print(f"Turning on effect for {effect}")
    nl = Nanoleaf(IP)
    old_effect = nl.get_current_effect()
    sleep(1)
    old_state = nl.get_power()
    sleep(1)
    nl.set_effect(effect)
    sleep(1)
    nl.power_on()
    sleep(length)
    
    if not old_state:
        nl.power_off()
        sleep(1)
    print(f"Turning off effect for {effect}")
    nl.set_effect(old_effect)

@timeout(MAX_TIMEOUT)
def turn_on_weather_effect(condition: str):
    nl = Nanoleaf(IP)
    digital_twin = NanoleafDigitalTwin(nl)
    old_state = digital_twin.get_all_colors()
    for panel, color in old_state.items():
        digital_twin.set_color(panel, color)
    digital_twin.set_color(53557, WEATHER_TO_COLORS.get(condition, WHITE))
    digital_twin.sync()
    nl.power_on()
