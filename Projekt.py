import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import random
import time
import datetime
import lcddriver

button0 = "P8_12"
button1 = "P8_14"
button2 = "P8_16"
button3 = "P8_18"
led0 = "P8_7"
led1 = "P8_9"
led2 = "P8_8"
led3 = "P8_10"
BUZZER = "P9_14"
NOTES = [100, 400, 700, 999]
lcd = lcddriver.lcd()

game_array = []

current_round = 1
score = 0

GPIO.setup(button0, GPIO.IN)
GPIO.setup(button1, GPIO.IN)
GPIO.setup(button2, GPIO.IN)
GPIO.setup(button3, GPIO.IN)
GPIO.setup(led0, GPIO.OUT)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)


def blink(led, timer):
    if led == 0:
        GPIO.output(led0, GPIO.HIGH)
        PWM.start(BUZZER, 50, NOTES[0])
        time.sleep(timer)
        PWM.stop(BUZZER)
        GPIO.output(led0, GPIO.LOW)
    elif led == 1:
        GPIO.output(led1, GPIO.HIGH)
        PWM.start(BUZZER, 50, NOTES[1])
        time.sleep(timer)
        PWM.stop(BUZZER)
        GPIO.output(led1, GPIO.LOW)
    elif led == 2:
        GPIO.output(led2, GPIO.HIGH)
        PWM.start(BUZZER, 50, NOTES[2])
        time.sleep(timer)
        PWM.stop(BUZZER)
        GPIO.output(led2, GPIO.LOW)
    else:
        GPIO.output(led3, GPIO.HIGH)
        PWM.start(BUZZER, 50, NOTES[3])
        time.sleep(timer)
        PWM.stop(BUZZER)
        GPIO.output(led3, GPIO.LOW)
    time.sleep(timer)


def game():
    while True:
        if GPIO.input(button0) or GPIO.input(button1) or GPIO.input(button2) or GPIO.input(button3):
            print("Let's start the game!")
            return game_loop()


def generate_game_round():
    game_array.append(random.randint(0, 3))
    time.sleep(1.5)
    for x in range(0, current_round):
        blink(game_array[x], 0.5)


def player_turn():
    global score
    time_start = time.time()
    time_end = time.time()
    bad_move = False
    good_move = 0
    index = 0
    while ((time_end - time_start) < current_round + 3) and (not bad_move) and good_move < current_round:

        if GPIO.input(button0):
            if game_array[index] != 0:
                bad_move = True
            else:
                good_move += 1
            index += 1
            PWM.start(BUZZER, 50, NOTES[0])
            time.sleep(0.5)
            PWM.stop(BUZZER)

        if GPIO.input(button1):
            if game_array[index] != 1:
                bad_move = True
            else:
                good_move += 1
            index += 1
            PWM.start(BUZZER, 50, NOTES[1])
            time.sleep(0.5)
            PWM.stop(BUZZER)

        if GPIO.input(button2):
            if game_array[index] != 2:
                bad_move = True
            else:
                good_move += 1
            index += 1
            PWM.start(BUZZER, 50, NOTES[2])
            time.sleep(0.5)
            PWM.stop(BUZZER)

        if GPIO.input(button3):
            if game_array[index] != 3:
                bad_move = True
            else:
                good_move += 1
            index += 1
            PWM.start(BUZZER, 50, NOTES[3])
            time.sleep(0.5)
            PWM.stop(BUZZER)

        time_end = time.time()
    if good_move == current_round:
        score += 1
        lcd.lcd_display_string("Current Score: " + str(score), 1)
        return True
    else:
        return False


def game_loop():
    global current_round
    while True:
        generate_game_round()

        if not (player_turn()):
            return score
        else:
            current_round += 1


if __name__ == '__main__':
    file = open('Wyniki.txt', "r+")
    data = file.read().split()
    today = datetime.datetime.now()

    lcd.lcd_display_string("Highscore: " + str(data[0]), 3)  # 2 LINIA 3 zamienione z 2
    lcd.lcd_display_string("Current Score: 0", 1)  # 2 LINIA 3 zamienione z 2

    result = game()
    print("Your result: " + str(result))
    lcd.lcd_display_string("                ", 1)
    lcd.lcd_display_string("                ", 3)
    lcd.lcd_display_string("END GAME", 1)  # 2 LINIA 3 zamienione z 2
    lcd.lcd_display_string("Your result " + str(result), 3)  # 2 LINIA 3 zamienione z 2
    if result > int(data[0]):
        file.seek(0)
        file.write(str(result) + " " + str(today.strftime("%x")))
    file.close()
