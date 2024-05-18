#include all neccessary packages to get LEDs to work with Raspberry Pi
import time
import board
import neopixel

BUTTON_UP = [(0, 9)]  # Two non-sequential pixel ranges for Button A
BUTTON_BACK = [(61, 66)]  # Two non-sequential pixel ranges for Button B
BUTTON_DOWN = [(57, 60)]  # Two non-sequential pixel ranges for Button X
BUTTON_FORWARD =[(52, 55)]
BUTTON_NEUTRAL = []
BUTTON_DOWNBACK = [(58, 62), (64, 68)]
BUTTON_DOWNFORWARD = [(58, 62), (53, 56)]
BUTTON_UPBACK = [(0, 9), (64, 68)]
BUTTON_UPFORWARD = [(0, 9), (53, 56)]
BUTTON_LP = [(48, 51)]
BUTTON_MP = [(44, 47)]
BUTTON_HP = [(39, 42)]
BUTTON_LK = [(11, 14)]
BUTTON_MK = [(16, 19)]
BUTTON_HK = [(20, 24)]
BUTTON_DI = [(33, 38)]
BUTTON_PARRY = [(25, 29)]


class ledCode:
    def __init__(self, savedCombo):
        #Time Conversion Variables
        self.FRAMETIME = 0.25 # Time in seconds
        self.LIGHT_DURATION = 2*self.FRAMETIME # Duration that light is shown

        # Neopixel configuration
        self.LED_COUNT = 144  # Number of pixels in your Neopixel strip
        self.LED_PIN = board.D18  # GPIO pin connected to the Neopixel data input

        # Color values associated with each button
        self.button_colors = {

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
        self.incoming_buttons = self.convert_input_array(savedCombo)

        # Convert the incoming array to button_sequence format
        self.button_sequence = []
        # Convert time to seconds from milliseconds
        # def convert_to_ms(time):
        # return time/1000

    def sequenceinit(self):
        print("incoming buttons")
        print(self.incoming_buttons)
        for button, frame in self.incoming_buttons:
            #time_ms = convert_to_ms((frame-1)*FRAMETIME) # Convert frame start time in ms to s
            time_value = (frame-1)*self.FRAMETIME
            color = self.button_colors.get(button, (255, 255, 255)) # Default to white if color is not defined
            self.button_sequence.append({'button': globals()[f'BUTTON_{button}'], 'time': time_value, 'color':color, 'duration': self.LIGHT_DURATION, 'set': False, 'cleared': False})
            # Add more conditions for other buttons if needed
        print("processed sequence")
        print(self.button_sequence)

    def convert_input_array(self, incoming_array):
        incoming_array[0][-1] = 1
        for i in range(1, len(incoming_array)):
            incoming_array[i][-1] = 8
        result = []
        frame_time_button = 0
        for entry in incoming_array:
            directions = []
            button = ""
            frame_time_button += entry[1]  # Second entry is the frame number

            for char in entry[0]:
                if char.isdigit():
                    directions.append(char)
                else:
                    button += char

            # Map directions to their corresponding names
            direction_names = {'1': 'DOWNBACK', '2': 'DOWN', '3': 'DOWNFORWARD', '4': 'BACK', '5': 'NEUTRAL', '6': 'FORWARD', '7': 'UPBACK', '8': 'UP', '9': 'UPFORWARD'}
            directions = [direction_names.get(d, d) for d in directions]


            # Append the result in the format of the desired output
            # Stagger directional inputs such that the last input occurs on the button press frame
            frame_time_direction = frame_time_button - len(directions)*self.LIGHT_DURATION + 1 #add scalar multiple of LED duration variable to len()?
            for direction in directions:
                result.append([direction, frame_time_direction])
                frame_time_direction += self.LIGHT_DURATION #replace 1 with LED duration variable?

            if button == "K":
                result.append(["LK", frame_time_direction])
            elif button == "P":
                result.append(["LP", frame_time_direction])
            elif button:
                result.append([button, frame_time_direction])


        return result

    # Function to set a specific range of pixels to a color
    def set_pixel_range(self, pixels, start, end, color):
        for i in range(start, end + 1):
            pixels[i] = color
        pixels.show()

    # Function to clear all pixels
    def clear_pixels(self, pixels):
        pixels.fill((0, 0, 0))
        pixels.show()

    def startSequence(self):
        pixels = neopixel.NeoPixel(self.LED_PIN, self.LED_COUNT, brightness=0.5, auto_write=False)
        self.clear_pixels(pixels)
        pixels.fill((255, 0, 0))
        pixels.show()
        time.sleep(1)
        pixels.fill((255, 255, 0))
        pixels.show()
        time.sleep(1)
        pixels.fill((0, 255, 0))
        pixels.show()
        time.sleep(1)
        self.clear_pixels(pixels)
        pixels.show()

# Main loop
    def run(self):
        self.sequenceinit()
        pixels = neopixel.NeoPixel(self.LED_PIN, self.LED_COUNT, brightness=1.0, auto_write=False)
        demo_complete = False # Track completion of lights
        self.clear_pixels(pixels)
        start_time = time.time() # Capture the start time of the script
        while not demo_complete:
            current_time = time.time() - start_time # Time since script has started
            # Check if the current time matches any designated time in the button sequence
            for entry in self.button_sequence:
                if current_time >= entry['time'] and current_time <= entry['time'] + entry['duration']:
                    if not entry['set']:
                        # Clear all previous lights only once per entry
                        self.clear_pixels(pixels)
                        for pixel_range in entry['button']:
                            self.set_pixel_range(pixels, *pixel_range, entry['color'])
                        entry['set'] = True
                elif current_time > entry['time'] + entry['duration']:
                    if not entry['cleared']:
                        # Clear pixels after the specified duration only once per entry
                        self.clear_pixels(pixels)
                        entry['cleared'] = True

            # Check if all entries have been cleared
            demo_complete = all(entry['cleared'] for entry in self.button_sequence)

            # Delay for a short period to avoid continuous updates
            time.sleep(0.1) #Delay by fraction of frametime so timing isnt missed??

# def main():
#     test = ledCode([['236MK', 5]])
#     test.run()

# main()
