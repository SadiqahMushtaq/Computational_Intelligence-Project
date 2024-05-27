import pygame
import pygame_gui
from EA_mine import *  # Importing Evolution class from EA_mine module
from pygame import Color
from pygame_gui.elements import UITextEntryLine
pygame.init()

# Render text with custom font color
def render_text(text, font, color):
    rendered_text = font.render(text, True, color)
    return rendered_text

# Screen dimensions
screen_width = 640
screen_height = 600
background_color = (211, 157, 141)  # Background color for the Pygame window
screen = pygame.display.set_mode((screen_width, screen_height))  # Set Pygame window dimensions

# Create a Pygame GUI manager
gui_manager = pygame_gui.UIManager((screen_width, screen_height), 'horizontal_slider.json')

# Create sliders
# Format for sliders_info: (position, value_range, start_value, object_id)
sliders_info = [
    ((220, 50), (20, 60), 40, "initial_population_slider"),
    ((220, 100), (1, 6), 3, "substitutions_slider"),
    ((220, 150), (0, 100), 100, "Vertical_slider"),
    ((220, 200), (0, 100), 90, "symmetry_slider"),
    ((220, 250), (0, 100), 0, "Photon_slider"),
    ((220, 300), (0, 100), 40, "stability_slider"),
    ((240, 350), (0, 100), 80, "branching_slider")
]

sliders = {}  # Dictionary to store slider objects
for info in sliders_info:
    slider_rect = pygame.Rect(info[0][0], info[0][1], 200, 20)  # Define slider rectangle
    slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=slider_rect,
        start_value=info[2],
        value_range=info[1],
        manager=gui_manager,
        object_id=info[3]
    )
    sliders[info[3]] = slider  # Add slider to dictionary

# Create labels for slider values
# Format for labels_slider_info: (position, object_id, value_object_id)
labels_slider_info = [
    (450, 50, "initial_population_slider_label", "initial_population_value"),
    (450, 100, "substitutions_slider_label", "substitutions_value"),
    (450, 150, "Vertical_slider_label", "Vertical_value"),
    (450, 200, "symmetry_slider_label", "symmetry_value"),
    (450, 250, "Photon_slider_label", "Photon_value"),
    (450, 300, "stability_slider_label", "stability_value"),
    (450, 350, "branching_slider_label", "branching_value")
]

labels_slider = {}  # Dictionary to store label objects for slider values
for info in labels_slider_info:
    label_rect = pygame.Rect(info[0], info[1], 50, 20)  # Define label rectangle
    label = pygame_gui.elements.UILabel(
        relative_rect=label_rect,
        text="",
        manager=gui_manager,
        object_id=info[3]
    )
    labels_slider[info[2]] = label  # Add label to dictionary

# Create the button
button_rect = pygame.Rect(50, 480, 150, 30)  # Define button rectangle
done_button = pygame_gui.elements.UIButton(
    relative_rect=button_rect,
    text="Optimize Tree!",
    manager=gui_manager
)

# Create the button
button_rect = pygame.Rect(200, 480, 150, 30)  # Define button rectangle
done_button1 = pygame_gui.elements.UIButton(
    relative_rect=button_rect,
    text="Optimize Serpinski!",
    manager=gui_manager
)

# Create the button
button_rect = pygame.Rect(350, 480, 150, 30)  # Define button rectangle
done_button2 = pygame_gui.elements.UIButton(
    relative_rect=button_rect,
    text="Optimize Dragon!",
    manager=gui_manager
)

# Create text boxes for inputting generations and mutation rate
textbox_rect1 = pygame.Rect(220, 400, 200, 20)  # Define text box rectangle for generations
generations_textbox = pygame_gui.elements.UITextEntryLine(
    relative_rect=textbox_rect1,
    manager=gui_manager,
    object_id="generations_textbox"  # Set object ID for generations text box
)

textbox_rect2 = pygame.Rect(220, 450, 200, 20)  # Define text box rectangle for mutation rate
mutation_rate_textbox = pygame_gui.elements.UITextEntryLine(
    relative_rect=textbox_rect2,
    manager=gui_manager,
    object_id="mutation_rate_textbox"  # Set object ID for mutation rate text box
)

# Create labels
labels_info = [
    (10, 50, "Choose Initial Population", "initial_population_label"),
    (10, 100, "Choose no of Substitutions", "substitutions_label"),
    (10, 150, "Positive Vertical", "Vertical_label"),
    (10, 200, "Bilateral Symmetry", "symmetry_label"),
    (10, 250, "Photon Gathering", "Photon_label"),
    (10, 300, "Structural Stability", "stability_label"),
    (10, 350, "Branching point proportion", "branching_label"),
    (10, 400, "No of Generations", "generations_label"),
    (10, 450, "Mutation Rate", "mutation_rate_label")
]

# Font setup
font = pygame.font.SysFont('Helvetica', 10)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        # Pass events to the GUI manager
        gui_manager.process_events(event)

        # Update slider values labels
        for slider_id, slider in sliders.items():
            current_value = str(slider.get_current_value())
            # labels_slider[f"{slider_id}_label"].set_text(current_value)

        # Handle button clicks
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == done_button or event.ui_element == done_button1 or event.ui_element == done_button2:

                    # Get input from the text boxes
                    generations_input = generations_textbox.get_text()
                    try:
                        generations = int(generations_input)
                    except ValueError:
                        # Handle invalid input
                        print("Invalid input for generations. Using default value.")
                        generations = 300  # Default value

                    mutation_rate_input = mutation_rate_textbox.get_text()
                    try:
                        mutation_rate = float(mutation_rate_input)
                    except ValueError:
                        # Handle invalid input
                        print("Invalid input for mutation rate. Using default value.")
                        mutation_rate = 0.1  # Default value

                    # Get values from sliders
                    sliders_values = {slider_id: slider.get_current_value() for slider_id, slider in sliders.items()}
                    InitialTrees = sliders_values["initial_population_slider"]
                    substitue_order = sliders_values["substitutions_slider"]
                    wa = sliders_values["Vertical_slider"]
                    wb = sliders_values["symmetry_slider"]
                    wc = sliders_values["Photon_slider"]  # Assuming wc is a constant
                    wd = sliders_values["stability_slider"]
                    we = sliders_values["branching_slider"]

                    offsprings = int(0.6 * InitialTrees)
                    print("Generations:", generations, "Mutation Rate:", mutation_rate)

                    if event.ui_element == done_button:
                        PatternType = 'Tree'
                    elif event.ui_element == done_button1:
                        PatternType = 'Serpinski'
                    elif event.ui_element == done_button2:
                        PatternType = 'Dragon'

                    # Initialize and run evolution
                    system = Evolution(InitialTrees, generations, mutation_rate, offsprings, substitue_order, False, wa, wb, wc, wd, we, PatternType)
                    result = system.run_evolution()
                    max_sublist = max(result, key=lambda x: x[0])
                    running = False  # Exit the main loop

                    # Generate and visualize L-system
                    s = Substitution_init(max_sublist[1], 4)
                    visualize_l_system(s, PatternType)
                    break

    # Update the GUI manager
    gui_manager.update(pygame.time.get_ticks() / 1000)

    # Draw the GUI manager to the screen
    screen.fill(background_color)
    gui_manager.draw_ui(screen)

    # Draw labels
    for info in labels_info:
        label_text = render_text(info[2], font, Color('black'))
        label_rect = label_text.get_rect(topleft=(info[0], info[1]))
        screen.blit(label_text, label_rect)

    # Draw slider values
    for slider_id, slider in sliders.items():
        current_value = str(slider.get_current_value())
        slider_value_text = render_text(current_value, font, Color('black'))
        slider_value_rect = slider_value_text.get_rect(topleft=(slider.rect.right + 10, slider.rect.top))
        screen.blit(slider_value_text, slider_value_rect)

    pygame.display.update()

pygame.quit()
