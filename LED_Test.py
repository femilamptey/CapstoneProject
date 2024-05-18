#include all neccessary packages to get LEDs to work with Raspberry Pi
import time
import board
import neopixel

#Time Conversion Variables
FRAMETIME = 16.67/1000 # Time in seconds
LIGHT_DURATION = 10*FRAMETIME # Duration that light is shown 

# Neopixel configuration
LED_COUNT = 144  # Number of pixels in your Neopixel strip
LED_PIN = board.D18  # GPIO pin connected to the Neopixel data input

# Button pixel ranges (adjust once LEDs are set in the controller)
BUTTON_UP = [(0, 1), (6, 7), (12, 13)]  # Two non-sequential pixel ranges for Button A
BUTTON_LEFT = [(2, 3), (8, 9)]  # Two non-sequential pixel ranges for Button B
BUTTON_DOWN = [(4, 5), (10, 11)]  # Two non-sequential pixel ranges for Button X
BUTTON_RIGHT =[(14, 15), (18, 19)]
BUTTON_LP = [(16, 17), (22, 23)]
BUTTON_MP = [(20, 21), (26, 27)]
BUTTON_HP = [(24, 25), (30, 31)]
BUTTON_LK = [(28, 29), (34, 35)]
BUTTON_MK = [(32, 33), (38, 39)]
BUTTON_HK = [(36, 37), (42, 43)]
BUTTON_DI = [(40, 41), (46, 47)]
BUTTON_DP = [(44, 45), (48, 49)]

# Color values associated with each button
button_colors = {

    'HP': (255, 0, 0),  #Red for Button H
    'HK': (255, 0, 0),  #Red for Button H
    'MP': (255, 255, 0),  #Yellow for Button M
    'MK': (255, 255, 0),  #Yellow for Button M
    'LP': (0, 0, 255),   #Blue for Button L
    'LK': (0, 0, 255),   #Blue for Button L
    'DI': (0, 255, 0),   #Green for DI & DP
    'DP': (0, 255, 0)   #Green for DI & DP
}

# Incoming array
incoming_buttons = [['UP', 2], ['RIGHT', 30], ['HP', 70]]
#incoming_buttons[1][0] #move reference
#incoming_buttons[1][1] #frame num reference

# Convert the incoming array to button_sequence format
button_sequence = []

# Convert time to seconds from milliseconds
# def convert_to_ms(time):
# return time/1000

for button, frame in incoming_buttons:
    #time_ms = convert_to_ms((frame-1)*FRAMETIME) # Convert frame start time in ms to s
    time_value = (frame-1)*FRAMETIME
    color = button_colors.get(button, (255, 255, 255)) # Default to white if color is not defined
    button_sequence.append({'button': globals()[f'BUTTON_{button}'], 'time': time_value, 'color':color, 'duration': LIGHT_DURATION, 'set': False, 'cleared': False})
    # Add more conditions for other buttons if needed

# Initialize the Neopixel strip
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=0.5, auto_write=False)

# Function to set a specific range of pixels to a color
def set_pixel_range(start, end, color):
    for i in range(start, end + 1):
        pixels[i] = color
    pixels.show()

# Function to clear all pixels
def clear_pixels():
    pixels.fill((0, 0, 0))
    pixels.show()

# Main loop

demo_complete = False # Track completion of lights
try:
    clear_pixels()
    #time.sleep(2)
    start_time = time.time() # Capture the start time of the script
    while not demo_complete:
        current_time = time.time() - start_time # Time since script has started

        # Check if the current time matches any designated time in the button sequence
        for entry in button_sequence:
            if current_time >= entry['time'] and current_time <= entry['time'] + entry['duration']:
                if not entry['set']:
                    # Clear all previous lights only once per entry
                    clear_pixels()
                    for pixel_range in entry['button']:
                        set_pixel_range(*pixel_range, entry['color'])
                    entry['set'] = True
            elif current_time > entry['time'] + entry['duration']:
                if not entry['cleared']:
                    # Clear pixels after the specified duration only once per entry
                    clear_pixels()
                    entry['cleared'] = True
        
        # Check if all entries have been cleared
        demo_complete = all(entry['cleared'] for entry in button_sequence)

        # Delay for a short period to avoid continuous updates
        time.sleep(0.1) #Delay by fraction of frametime so timing isnt missed??

except KeyboardInterrupt:
    # Clear pixels and exit gracefully on keyboard interrupt
    clear_pixels()
    print("Program terminated by user.")
