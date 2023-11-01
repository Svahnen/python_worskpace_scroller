from pynput import mouse
import subprocess
import time

# Counter for horizontal scroll steps
scroll_counter = 0

# Variable to keep track of the last scroll direction
last_direction = None

# Variable to keep track of the last scroll time
last_time = 0

def on_scroll(x, y, dx, dy):
    global scroll_counter, last_direction, last_time

    # Get the current time
    current_time = time.time()

    # Detect horizontal scroll (dy is for vertical scroll)
    if dx != 0:
        # Check if more than X second has passed since the last scroll
        if current_time - last_time > 0.1:
            scroll_counter = 0

        # Check if the direction has changed
        if last_direction is not None and last_direction != dx:
            # Reset the counter if the direction changes
            scroll_counter = 0

        # Update the last direction and time
        last_direction = dx
        last_time = current_time

        # Increment the counter
        scroll_counter += 1

        # Trigger the xdotool command after X horizontal scroll steps
        if scroll_counter >= 8:
            if dx > 0:
                # Scroll right
                subprocess.run(["xdotool", "key", "ctrl+Super+Up"])
            else:
                # Scroll left
                subprocess.run(["xdotool", "key", "ctrl+Super+Down"])
            
            # Reset the counter
            scroll_counter = 0

# Listen to mouse events
with mouse.Listener(on_scroll=on_scroll) as listener:
    listener.join()
