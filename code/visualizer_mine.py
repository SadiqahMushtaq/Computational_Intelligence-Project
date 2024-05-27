import turtle

class TurtleStack:
    def __init__(self):
        """
        Initialize the TurtleStack class.

        Initializes an empty stack to manage turtle state.
        """
        self.stack = []  # Initialize an empty stack for turtle state

    def push(self, item):
        """
        Push an item onto the stack.

        Args:
        - item: Item to be pushed onto the stack
        """
        self.stack.append(item)  # Push item onto the stack

    def pop(self):
        """
        Pop and return the top item from the stack.

        Returns:
        - item: Item popped from the stack
        """
        return self.stack.pop()  # Pop and return the top item from the stack

def draw_l_system(turtle_instance, l_system_string, PatternType):
    """
    Draw an L-system pattern using a turtle instance.

    Args:
    - turtle_instance: Turtle instance to draw the pattern
    - l_system_string: L-system string representing the pattern
    """
    stack = TurtleStack()  # Create an instance of TurtleStack to manage turtle state
    for command in l_system_string:  # Iterate over each command in the L-system string
        if command == 'F':
            turtle_instance.forward(8)  # Move turtle forward by 8 units
        elif PatternType:
            if PatternType == 'Tree':
                if command == '-':
                    turtle_instance.right(30)  # Turn turtle right by 30 degrees
                elif command == '+':
                    turtle_instance.left(30)  # Turn turtle left by 30 degrees
            elif PatternType == 'Serpinski':
                if command == '-':
                    turtle_instance.right(120)
                elif command == '+':
                    turtle_instance.left(120)
            elif PatternType == 'Dragon':
                if command == '-':
                    turtle_instance.right(90)
                elif command == '+':
                    turtle_instance.left(90)
        elif command == '[':
            x, y = turtle_instance.pos()  # Get turtle's current position
            heading = turtle_instance.heading()  # Get turtle's current heading
            stack.push((x, y, heading))  # Push current position and heading onto the stack
        elif command == ']':
            x, y, heading = stack.pop()  # Pop position and heading from the stack
            turtle_instance.penup()  # Lift pen up
            turtle_instance.setpos(x, y)  # Move turtle to popped position
            turtle_instance.seth(heading)  # Set turtle's heading to popped heading
            turtle_instance.pendown()  # Put pen down

    print("Drawing complete")  # Print message indicating drawing is complete

def visualize_l_system(l_system_string, PatternType):
    """
    Visualize an L-system pattern using turtle graphics.

    Args:
    - l_system_string: L-system string representing the pattern to visualize
    """
    turtle_instance = turtle.Turtle()  # Create a turtle instance
    window = turtle.Screen()  # Create a window for drawing

    # Customize turtle appearance and behavior
    turtle_instance.shape("turtle")
    turtle_instance.color("green")
    turtle_instance.speed(0)
    win_width, win_height, bg_color = 2000, 2000, 'white'
    TURTLE_SIZE = 20

    # Set up the turtle screen
    turtle.setup()
    turtle.tracer(False)
    turtle.screensize(win_width, win_height, bg_color)
    turtle_instance.seth(90)  # Set turtle's orientation to 90 degrees (upwards)
    turtle_instance.shape('classic')  # Set turtle's shape to classic arrow
    turtle_instance.color('Green')  # Set turtle's color to green
    turtle_instance.pensize(1)  # Set pen size to 1
    turtle_instance.penup()  # Lift pen up
    turtle_instance.setpos(0, -250)  # Set initial position for drawing
    turtle_instance.pendown()  # Put pen down
    turtle_instance.hideturtle()  # Hide turtle icon

    # Function to show coordinates when clicked
    def show_coordinates(x, y):
        turtle_instance.penup()  # Lift pen up to avoid drawing
        turtle_instance.goto(x, y)  # Move turtle to clicked coordinates
        turtle_instance.pencolor('black')
        turtle_instance.write(f"({x}, {y})", align="center", )  # Write coordinates at clicked position

    # Bind the function to the screen click event
    window.onscreenclick(show_coordinates)

    # Call function to draw L-system pattern
    draw_l_system(turtle_instance, l_system_string, PatternType)

    turtle.update()  # Update the window to show the drawn pattern
    window.exitonclick()  # Keep the window open until user clicks to close
