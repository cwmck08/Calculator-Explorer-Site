from drafter import *
from dataclasses import dataclass
import math
import matplotlib.pyplot as plt


set_website_title("Concentration Explorer")
set_site_information(
    author="Carter McKissick",
    description="Calculate concentration and average reaction rate easily using this simple website.",
    sources="",
    planning=[],
    links=[]
)
hide_debug_information()

@dataclass
class Calculation:
    calculation_type: str
    initial_concentration: float
    final_concentration: float
    time: float
    result: float
    units: str


@dataclass
class State:
    initial_concentration: float
    rate_constant: float
    elapsed_time: float
    final_concentration: float
    average_reaction_rate: float
    calculations: list[Calculation]

def concentration_formula(initial: float, rate: float, time: float) -> float:
    '''
    Calculates the final concentrationn
    
    parameters:
    initial (float): The initial concentration in mol/L
    rate (float): The rate constant for the reaction
    time (float): The total time for the reaction in sec
    
    returns:
    float: The final concentration in mol/L
    
    '''
    return initial * math.exp(-rate * time)

assert_equal(concentration_formula(1.0, 0.2, 5.0), 0.3679)
assert_equal(concentration_formula(0.0, 0.2, 5.0), 0.0)
assert_equal(concentration_formula(1.0, 1.0, 5.0), 0.0067)
assert_equal(concentration_formula(1.0, 0.2, 0.0), 1.0)

def reaction_rate_formula(initial: float, final: float, time: float) -> float:
    '''
    Calculates average reaction rate
    
    parameters:
    initial (float): The initial concentration in mol/L
    rate (float): The rate constant for the reaction
    time (float): The total time for the reaction in sec
    
    returns:
    float: The average reaction rate in mol/L sec
    '''
    if final > initial:
        return 0.0
    return (initial - final) / time

assert_equal(reaction_rate_formula(0.8, 0.3, 10.0), 0.05)
assert_equal(reaction_rate_formula(0.0, 0.3, 10.0), 0.0)
assert_equal(reaction_rate_formula(2.5, 0.3, 4.0), 0.55)

def valid_reaction_rate(initial: float, final: float, time: float) -> bool:
    '''
    Checks and sees whether inputed user numbers will cause in invalid reaction rate
    
    parameters:
    initial (float): The initial concentration in mol/L
    rate (float): The rate constant for the reaction
    time (float): The total time for the reaction in sec
    
    returns:
    bool: Whether reaction is valid, True, or invalid, False
    '''

    if initial <= 0:
        return False
    elif final < 0:
        return False
    elif final > initial:
        return False
    elif time <= 0:
        return False
    else:
        return True
    
assert_equal(valid_reaction_rate(0.8, 0.3, 10.0), True)
assert_equal(valid_reaction_rate(-1.0, 0.3, 10.0), False)
assert_equal(valid_reaction_rate(0.8, -0.1, 10.0), False)
assert_equal(valid_reaction_rate(0.2, 0.3, 10.0), False)
assert_equal(valid_reaction_rate(0.8, 0.3, -2.0), False)

def describe_calculation(calculation: Calculation) -> str:
    '''
    Creates the description of a saved calculation for calculation history
    
    parameters:
    calculation (Calculation): All of the attributes of a calculation previously made
    
    returns:
    str: The type of calculation performed, concentration or reaction rate, with the rounded answer and the units associated with the answer
    '''
    return (calculation.calculation_type + ": " + str(round(calculation.result, 4)) + " " + calculation.units)

@route
def index(state: State) -> Page:
    '''
    Displays the home page of the website
    
    Gives a brief introduction into the website and provides navigation buttons to access other pages
    
    parameters:
    state(State): stores website information
    
    returns:
    the homepage as a page
    '''
    
    return Page(state, [
        Header("Concentration Explorer"),

        "Welcome to Concentration Explorer!",

        "A website designed to help students "
        "understand chemical reactions and concentration.",

        Header("Explore the Website", 2),

        Button("Concentration Calculator",
               "concentration_calculator"),

        Button("Reaction Rate Calculator",
               "reaction_rate_calculator"),

        Button("Concentration Graph",
               "concentration_graph"),

        Button("Learning Center",
               "learning_center"),

        Button("Calculation History",
               "calculation_history"),

        Button("Reaction Rate Examples",
               "reaction_rate_examples")
    ])

@route
def concentration_calculator(state: State) -> Page:
    '''
    Displays the concentration calculator page
    
    User enters initial concentration, reaction rate constant, and elapsed time
    
    parameters:
    state(State): stores current calculator information
    
    returns:
    A page containing concentration calculator inputs
    '''
    return Page(state, [
        Header("Concentration Calculator"),

        "Calculate how much of a reactant remains "
        "after a certain amount of time.",

        "\n Initial Concentration (mol/L):",

        TextBox("initial", state.initial_concentration, "number"),

        "\n Reaction Rate Constant:",

        TextBox("rate", state.rate_constant, "number"),

        "\n Elapsed Time (seconds):",

        TextBox("time_value", state.elapsed_time, "number"),

        Button("Calculate", "calculate_concentration"),

        Button("Home", "index")
    ])

@route
def calculate_concentration(state: State, initial: float, rate: float, time_value: float) -> Page:
    '''
    Calculates final concentration of a reactant
    
    Uses initial concentration, reaction rate constant, and elapsed time to calculate
    final concentration and saves the calculation in the calculation history
    
    parameters:
    state(State): stores website information
    initial (float): The initial concentration in mol/L
    rate (float): The rate constant for the reaction
    time_value (float): The total time for the reaction in sec
    
    returns:
    a page displaying calculation results 
    '''
    if initial <= 0:
        return Page(state, [
            "Initial concentration must be greater than zero.",
            Button("Try Again", "concentration_calculator")
        ])

    elif rate < 0:
        return Page(state, [
            "Reaction rate constant cannot be negative.",
            Button("Try Again", "concentration_calculator")
        ])

    elif time_value < 0:
        return Page(state, [
            "Time cannot be negative.",
            Button("Try Again", "concentration_calculator")
        ])

    state.initial_concentration = initial
    state.rate_constant = rate
    state.elapsed_time = time_value

    state.final_concentration = concentration_formula(
        initial, rate, time_value
    )


    state.calculations.append(
        Calculation(
            "Concentration",
            initial,
            state.final_concentration,
            time_value,
            state.final_concentration,
            "mol/L"
        )
    )

    return Page(state, [
        Header("Concentration Results"),

        "\n Initial Concentration: "
        + str(initial) + " mol/L",

        "\n Final Concentration: "
        + str(round(state.final_concentration, 4))
        + " mol/L",

        "\n Elapsed Time: "
        + str(time_value) + " seconds",

        Button("View Graph", "concentration_graph"),

        Button("View History", "calculation_history"),

        Button("Calculate Again", "concentration_calculator"),

        Button("Home", "index")
    ])


@route
def reaction_rate_calculator(state: State) -> Page:
    '''
    Displays the reaction rate calculator page

    User enters starting concentration, ending concentration, and elapsed time

    parameters:
    state(State): stores website information

    returns:
    A page containing reaction rate calculator input
    '''
    return Page(state, [
        Header("Reaction Rate Calculator"),

        TextBox("Starting Concentration (mol/L)", "starting_concentration"),

        TextBox("Ending Concentration (mol/L)", "ending_concentration"),

        TextBox("Reaction Time (seconds)", "reaction_time"),

        Button("Calculate Reaction Rate",
               "calculate_reaction_rate"),

        Button("Home", "index")
    ])

@route
def calculate_reaction_rate(state: State, starting_concentration: float, ending_concentration: float, reaction_time: float) -> Page:
    '''
    Calculates average reaction rate of a reactant
    
    Checks whether entered values are valid, calculates the average reaction rate, and saves calculation in the history
    
    parameters:
        state(State): stores website information
        starting_concentration (float): The starting concentration in mol/L
        ending_concentration (float): The ending concentration in mol/L
        reaction_time (float): Time it takes for the reaction to occur)
    
    returns:
    A page displaying the reaction rate or an error
    '''

    if not valid_reaction_rate(
        starting_concentration, ending_concentration, reaction_time
    ):
        return Page(state, [
            "Please enter valid reaction rate values.",

            Button("Try Again", "reaction_rate_calculator")
        ])


    state.average_reaction_rate = reaction_rate_formula(
        starting_concentration, ending_concentration, reaction_time
    )


    state.calculations.append(
        Calculation(
            "Reaction Rate",
            starting_concentration,
            ending_concentration,
            reaction_time,
            state.average_reaction_rate,
            "mol/L/s"
        )
    )

    return Page(state, [
        Header("Reaction Rate Results"),

        "Starting Concentration: "
        + str(starting_concentration) + " mol/L",

        "\n Ending Concentration: "
        + str(ending_concentration) + " mol/L",

        "\n Time Elapsed: "
        + str(reaction_time) + " seconds",

        "\n Average Reaction Rate: "
        + str(round(state.average_reaction_rate, 4))
        + " mol/L/s",

        Button("Calculate Again", "reaction_rate_calculator"),

        Button("View History", "calculation_history"),

        Button("Home", "index")
    ])

@route
def concentration_graph(state: State) -> Page:
    '''
    Creates a graph showing concentration changes over time
    
    Uses initial concentration, rate constant, and elapsed time to generate concentration values
    
    parameters:
    state(State): Stores calculator information
    
    returns:
    a page displaying the concentration graph
    '''
    times = []
    concentrations = []

    for step in range(11):

        point_time = state.elapsed_time * step / 10

        point_concentration = concentration_formula(
            state.initial_concentration,
            state.rate_constant,
            point_time
        )

        times.append(point_time)
        concentrations.append(point_concentration)

    plt.figure()

    plt.plot(times, concentrations, marker="o")

    plt.xlabel("Time (seconds)")
    plt.ylabel("Concentration (mol/L)")

    plt.title("Concentration Over Time")

    plt.grid(True)

    return Page(state, [
        Header("Concentration Graph"),

        "This graph shows how concentration changes over time.",

        MatPlotLibPlot(),

        Button("Calculator", "concentration_calculator"),

        Button("Home", "index")
    ])

@route
def learning_center(state: State) -> Page:
    '''
    displays education information about concentration and reaction rates
    
    parameters:
    state(State): stores the website information
    
    returns:
    a page containing chemistry information
    '''
    return Page(state, [
        Header("Learning Center"),

        Header("What is Concentration?", 2),

        "Concentration measures how much of a substance "
        "is present in a given volume.",

        Header("What is Reaction Rate?", 2),

        "Reaction rate measures how quickly reactants "
        "are consumed or products are formed.",

        Header("What is a Rate Constant?", 2),

        "The rate constant describes the speed of a reaction "
        "under specified conditions.",

        Header("First-Order Reaction Equation", 2),

        "[A]t = [A]0 * e^(-kt)",

        "This equation calculates concentration over time "
        "for a first-order reaction.",

        Header("Average Reaction Rate Equation", 2),

        "Rate = (Initial Concentration - Final Concentration) "
        "/ Time Elapsed",

        Button("Concentration Calculator",
               "concentration_calculator"),

        Button("Reaction Rate Calculator",
               "reaction_rate_calculator"),

        Button("Home", "index")
    ])

@route
def calculation_history(state: State) -> Page:
    '''
    Displays previously completed calculations
    
    parameters:
    state(State): stores website information and calculation history
    
    returns:
    a page displaying previous calculations
    '''

    history_items = []

    for calculation in state.calculations:

        history_items.append(
            describe_calculation(calculation)
        )

    if len(state.calculations) == 0:
        return Page(state, [
            Header("Calculation History"),

            "You have not completed any calculations yet.",

            Button("Concentration Calculator",
                   "concentration_calculator"),

            Button("Reaction Rate Calculator",
                   "reaction_rate_calculator"),

            Button("Home", "index")
        ])

    return Page(state, [
        Header("Calculation History"),

        "Here are your previous calculations:",

        BulletedList(history_items),

        Button("Concentration Calculator",
               "concentration_calculator"),

        Button("Reaction Rate Calculator",
               "reaction_rate_calculator"),

        Button("Home", "index")
    ])

@route
def reaction_rate_examples(state: State) -> Page:
    '''
    displays examples of average reaction rate problems
    
    parameters:
    state(State): stores the website information
    
    returns:
    a page containing reaction rate examples
    '''
    return Page(state, [
        Header("Reaction Rate Examples"),

        "Learn how to calculate average reaction rate "
        "using these examples.",

        Header("Formula", 2),

        "Rate = (Initial Concentration - Final Concentration) "
        "/ Time Elapsed",

        Header("Example 1", 2),

        "Initial Concentration: 0.80 mol/L",
        "Final Concentration: 0.30 mol/L",
        "Time Elapsed: 10 seconds",
        "Calculation: (0.80 - 0.30) / 10",
        "Answer: 0.05 mol/L/s",

        Header("Example 2", 2),

        "Initial Concentration: 1.20 mol/L",
        "Final Concentration: 0.60 mol/L",
        "Time Elapsed: 5 seconds",
        "Calculation: (1.20 - 0.60) / 5",
        "Answer: 0.12 mol/L/s",

        Header("Example 3", 2),

        "Initial Concentration: 2.00 mol/L",
        "Final Concentration: 1.50 mol/L",
        "Time Elapsed: 5 seconds",
        "Calculation: (2.00 - 1.50) / 5",
        "Answer: 0.10 mol/L/s",

        Header("Try It Yourself", 2),

        "Ready to calculate your own reaction rate?",

        Button("Reaction Rate Calculator",
               "reaction_rate_calculator"),

        Button("Home", "index")
    ])

#assert_equal tests for routes

#tests for index
test_state = State(1.0, 0.2, 5.0, 0.3679, 0.0, [])

assert_has(index(test_state), "Concentration Explorer")

assert_has(index(test_state), Button(
    "Reaction Rate Calculator",
    "reaction_rate_calculator"
))

#test for concentration_calculator
test_state = State(1.0, 0.2, 5.0, 0.3679, 0.0, [])

result = calculate_concentration(test_state, 1.0, 0.2, 5.0)

assert_state(result, State(1.0, 0.2, 5.0, 0.3679, 0.0, 
        [Calculation(
        "Concentration",
        1.0,
        0.3679,
        5.0,
        0.3679,
        "mol/L"
    )]
))

#test for calculate_concentration
test_state = State(1.0, 0.2, 5.0, 0.0, 0.0, [])

result = calculate_concentration(
    test_state, 1.0, 0.2, 5.0
)

assert_equal(
    round(test_state.final_concentration, 4),
    0.3679
)

assert_equal(len(test_state.calculations), 1)

#test for reaction rate calculator
test_state = State(1.0, 0.2, 5.0, 0.3679, 0.0, [])

result = calculate_reaction_rate(test_state, 0.8, 0.3, 10.0)

assert_state(result, State(1.0, 0.2, 5.0, 0.3679, 0.05,
    [Calculation(
        "Reaction Rate",
        0.8,
        0.3,
        10.0,
        0.05,
        "mol/L/s"
    )]
))

#test for calculate_reaction_rate
test_state = State(1.0, 0.2, 5.0, 0.0, 0.0, [])

result = calculate_reaction_rate(
    test_state, 0.8, 0.3, 10.0
)

assert_equal(
    test_state.average_reaction_rate,
    0.05
)

assert_equal(len(test_state.calculations), 1)

#test for calculation_history
test_state = State(1.0, 0.2, 5.0, 0.0, 0.0, [])

assert_has(
    calculation_history(test_state),
    "You have not completed any calculations yet."
)

start_server(State(
    1.0,
    0.2,
    5.0,
    0.3679,
    0.0,
    []
))
