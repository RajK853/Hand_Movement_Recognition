from microbit import display, Image, sleep, button_a, button_b, running_time, accelerometer
from micropython import const
# States
GET_DATA_NUM    = const(0)
READY_TO_SAMPLE = const(1)
SAMPLE_DATA     = const(2)
EXIT            = const(-1)
# Global constants
CHANNEL         = const(13)
MAX_FILES_NUM   = const(12)
MAX_ATTEMPT     = const(3)
SAMPLE_PERIOD   = const(10)                                                 # Sample period in ms
SAMPLE_DURATION = const(1500)                                               # Total sample time in ms
ACK             = const("0")
NACK            = const("1")
# LED Numbers; 3, 2, 1 
NUM_IMGS = const([Image("90909:90909:90909:99999:99999"), 
                  Image("99909:90909:90909:90909:90999"),
                  Image("00000:00090:99999:99999:00000")])

def countdown(t=3):
    """
    Display countdown animation of given second(s)
    @param t : Time (in seconds)
    @returns : Nothing
    """
    max_t = len(NUM_IMGS)
    if (t > max_t):
        t = max_t
    elif (t < 1):
        t = 1
    display.show(NUM_IMGS[-t:], loop=False, delay=1000)

def setPixelTill(cx, cy, value=9):
    """
    Sets all pixel from (0, 0) till the given (x, y) coordinate to given value
    @param cx    : X-coordiante of the final pixel
    @param cy    : Y-coordinate of the final pixel
    @param value : Value to set for the pixels
    @returns     : Nothing
    """
    for y in range(5):
        for x in range(5):
            display.set_pixel(x, y, value)
            if x==cx and y==cy:
                return

def main():
    data_sent = 0
    state = GET_DATA_NUM
    while True:
        # State 0
        if state == GET_DATA_NUM:
            data_num = 1
            attempt = 0
            while True:
                cy, cx = divmod(data_num-1, 5)                          # Cursor x and y depending on the data_num
                display.set_pixel(cx, cy, 9)
                if button_a.is_pressed() and button_b.is_pressed():
                    state = READY_TO_SAMPLE                                        # TODO: Change state to some other state
                    data_sent = 0
                    sleep(500)
                    break
                elif button_a.is_pressed():
                    if data_num > 1:
                        display.set_pixel(cx, cy, 0)                                # Clear LED pixel if data_num > 1
                    data_num = data_num - 1 if (data_num > 1) else 1
                elif button_b.is_pressed():
                    data_num = data_num + 1 if (data_num < MAX_FILES_NUM) else MAX_FILES_NUM
                sleep(200)
        # State 1
        elif state == READY_TO_SAMPLE:
            while True:
                if button_a.is_pressed():
                    state = SAMPLE_DATA
                    break
                elif button_b.is_pressed():
                    display.clear()
                    cy, cx = divmod(data_num-data_sent-1, 5)
                    setPixelTill(cx, cy, 9)
                else:
                    display.show(Image.ARROW_W)
                sleep(200)
        # State 2
        elif state == SAMPLE_DATA:
            countdown(1)
            display.show(Image.TARGET)
            with open("file_{}.csv".format(data_sent), "w") as data_file:
                data_file.write("x,y,z\n")
                initial_time = running_time()
                while (running_time()-initial_time) < SAMPLE_DURATION:
                    t0 = running_time()
                    data_file.write("{},{},{}\n".format(*accelerometer.get_values()))
                    t_diff = running_time()-t0
                    sleep(0 if (SAMPLE_PERIOD-t_diff)<0 else SAMPLE_PERIOD-t_diff)
            data_sent += 1
            if (data_num-data_sent)>0:
                state = READY_TO_SAMPLE  
            else:
                state = EXIT
        # State 3
        elif state == EXIT:
            display.show(Image.HAPPY)
            break

if __name__ == "__main__":
    main()