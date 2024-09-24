"Veles tutorial script"
import velesresearch as vls

###############################
##### QUESTION PARAMETERS #####
###############################

defaultOptions = {"isRequired": True, "hideNumber": True}
radioOptions = {"hideNumber": False, "colCount": 2}


demographics = vls.page(
    "demographics",
    vls.text(
        "initials",
        "What are your initials?",
        validators=vls.textValidator(
            2, 3, allowDigits=False, error="Please enter proper initials"
        ),
    ),
    vls.radio(
        "gender",
        "What is your gender?",
        "Woman",
        "Man",
        "I don't want to answer",
        showOtherItem=True,
        **defaultOptions | radioOptions,
    ),
    vls.yesno("marriage", "Are you married?", **defaultOptions),
    vls.text(
        "age", "How old are you?", inputType="number", min=1, textUpdateMode="onTyping"
    ),
    vls.yesno(
        "retirement", "Since you are {age}, are you retired?", visibleIf="{age} >= 60"
    ),
    vls.rating(
        "enjoyment",
        "How do you enjoy your retirement?",
        visibleIf="{retirement} = true",
    ),
    title="Demographics",
)

#####################
##### INFOBOXES #####
#####################

intro = vls.page(
    "intro",
    vls.info(
        "intro",
        """## Welcome to the <span style="all: revert; color: #CC0000">survey</span>!
Please answer all the questions.""",
    ),
    vls.consent(),
)

RSES = vls.page(
    "RSES",
    vls.info(
        "instruction",
        """Please record the appropriate answer <span style="color: #edb418;">**for each item**</span>, depending on whether you
_strongly agree_, _agree_, _disagree_, or _strongly disagree_ with it.""",
    ),
    vls.radio(
        "RSES",
        """I feel that I am a person of worth, at least on an equal plane with others.
I feel that I have a number of good qualities.
All in all, I am inclined to feel that I am a failure.
I am able to do things as well as most other people.
I feel I do not have much to be proud of.
I take a positive attitude toward myself.
On the whole, I am satisfied with myself.
I wish I could have more respect for myself.
I certainly feel useless at times.
At times I think I am no good at all.""".split(
            "\n"
        ),
        "Strongly Agree; Agree; Disagree; Strongly Disargee".split("; "),
        hideNumber=True,
    ),
)

##############################
##### LIST COMPREHENSION #####
##############################

drinks_list = "tea, coffee, water, orange juice".split(", ")
drinks_list = [f"How do you like {drink}?" for drink in drinks_list]

drinks = vls.page(
    "drink_preferences",
    vls.rating("drink", drinks_list),
)


##################
##### IMAGES #####
##################

animals = vls.page(
    "animals",
    vls.info(
        "images",
        f"""
<div style="display: flex; gap: 30px; justify-content: center;">
    <img src="{vls.convertImage("images/jam.jpg")}" style="width: 50%; height: auto;">
    <img src="{vls.convertImage("images/langouste.jpg")}" style="width: 50%; height: auto;">
</div>
""",
    ),
    vls.yesno(
        "langouste", "Would the langouste eat jam if it could?", correctAnswer="true"
    ),
)

##################################
##### CONDITIONAL VISIBILITY #####
##################################

manipulation = vls.page(
    "manipulation",
    vls.info("manipulation", "## You are stupid!"),
    visibleIf="{group} = 2",
)

#########################
##### DYNAMIC TEXTS #####
#########################

BMI = vls.page(
    "BMI",
    vls.text(
        "weight",
        "What is your weight in kilograms?",
        inputType="number",
        min=1,
    ),
    vls.text(
        "height",
        "What is your height in centimeters?",
        inputType="number",
        min=1,
    ),
    vls.info(
        "BMI",
        """Weight = {weight} kg
             
Height = {meters} m

**BMI = {BMI}**

<span style="color: {bmiColor};">**{overweight}**</span>""",
        visibleIf="{weight} notempty and {height} notempty",
    ),
)

######################
##### VALIDATORS #####
######################

special_number = vls.page(
    "special_number",
    vls.text(
        "special_number",
        "Please enter the code that was given to you",
        validators=vls.regexValidator("^\\w\\d{2}$"),
        autocomplete="off",
    ),
    vls.text(
        "academic_email",
        "Please enter your academic email",
        inputType="email",
        validators=vls.regexValidator("@uwr.edu.pl$"),
    ),
)

###################
##### HOSTING #####
###################

vls.survey(
    intro,
    BMI,
    manipulation,
    RSES,
    animals,
    drinks,
    demographics,
    special_number,
    numberOfGroups=2,
    showTOC=True,
    calculatedValues=[
        {
            "name": "meters",
            "expression": "{height} / 100",
            "includeIntoResult": False,
        },
        {"name": "BMI", "expression": "round({weight} / ({meters} * {meters}), 1)"},
        {
            "name": "overweight",
            "expression": "iif({BMI} >= 25, 'You are overweight', 'You are not overweight')",
            "includeIntoResult": False,
        },
        {
            "name": "bmiColor",
            "expression": "iif({BMI} >= 25, 'red', 'green')",
            "includeIntoResult": False,
        },
    ],
    completedHtml="Thank you for completing the survey!",
    buildForPublication=True,
)
