import subprocess
import re

# Function to get the list of connected screens and their Persistent screen IDs and resolutions
def get_screen_info():
    # Running the 'displayplacer list' command to get screen information
    result = subprocess.run(["displayplacer", "list"], capture_output=True, text=True)
    
    screens = []
    current_screen = None
    
    for line in result.stdout.splitlines():
        if "Persistent screen id" in line:
            if current_screen:
                screens.append(current_screen)
            current_screen = {"id": line.split(":")[1].strip()}
        
        if "Resolution" in line:
            resolution = re.search(r"Resolution: (\d+x\d+)", line)
            if resolution:
                current_screen["resolution"] = resolution.group(1)
        
        # Collecting all screen info
        if current_screen and "resolution" in current_screen:
            screens.append(current_screen)
            current_screen = None
            
    return screens

# Function to display available screen options with their resolutions
def display_screen_options(screens):
    print("Available screens:")
    for i, screen in enumerate(screens):
        print(f"Display {i + 1}: Current Resolution: {screen['resolution']}")
    print()

# Function to configure a selected screen with default values for certain options
def configure_screen(screen):
    print(f"Configuring screen {screen['id']} with current resolution {screen['resolution']}")
    
    # Ask user for new resolution
    resolution_input = input(f"Enter new resolution (current: {screen['resolution']}): ")
    if not resolution_input:
        resolution_input = screen['resolution']  # Keep the current resolution if no input is provided
        
    hz = input("Enter refresh rate (e.g., 60): ")
    
    # Default values for color depth, scaling, origin positions, and rotation
    color_depth = "8"
    scaling = "off"
    origin_x = "0"
    origin_y = "0"
    degree = "0"

    # Constructing the displayplacer command with Persistent screen id
    command = f"displayplacer \"id:{screen['id']} res:{resolution_input} hz:{hz} color_depth:{color_depth} enabled:true scaling:{scaling} origin:({origin_x},{origin_y}) degree:{degree}\""
    
    # Running the command to configure the screen
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Screen with resolution {screen['resolution']} configured successfully!")
    except subprocess.CalledProcessError:
        print(f"Unable to find screen {screen['id']} - skipping changes for that screen.")

def main():
    print("########################################")
    print("#-----------DarwinCustomRes------------#")
    print("########################################")
    while True:
        screens = get_screen_info()
        
        if not screens:
            print("No screens detected.")
            break
        
        display_screen_options(screens)
        
        # Prompt user to select a screen
        selected_screen = int(input("Select screen number to configure (or 0 to exit): ")) - 1
        if selected_screen == -1:
            print("Exiting program.")
            break
        
        if selected_screen < 0 or selected_screen >= len(screens):
            print("Invalid selection.")
            continue

        screen = screens[selected_screen]
        configure_screen(screen)

if __name__ == "__main__":
    main()
