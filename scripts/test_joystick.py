from drivers.joystick import PS4Joystick

if __name__ == "__main__":
    js = PS4Joystick()
    assert js.init() == True
    print(js.show_map())
    while True:
        button, button_state, axis, axis_val = js.poll()
        if axis == "left_stick_vert":
            print(f'{axis}: {axis_val}')
        if button == "R2":
            print(f"{button}: {button_state}")
