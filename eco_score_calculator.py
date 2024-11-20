import streamlit as st

# Function to inject custom CSS (optional for consistent styling)
def inject_custom_css():
    st.markdown(
        """
        <style>
        .main {
            background-color: #F5F5F5; /* Light grey background */
        }
        .bold-text {
            font-weight: bold;
        }
        .centered {
            text-align: center;
        }
        .red-band {
            background-color: #8B0000; 
            padding: 10px; 
            border-radius: 5px; 
            color: white; 
            font-size: 24px; 
            font-weight: bold; 
            text-align: left; 
            width: 100%;
        }
        .button-style {
            font-weight: bold;
            background-color: #4CAF50;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Set page configuration and image
st.set_page_config(page_title="Eco-Score Calculator", page_icon="🌱")

# Inject custom CSS
inject_custom_css()

# Add an image and a title at the top
st.image("https://cdn.unitycms.io/images/2lnv07LWaRb8rdPxOqTKwI.jpg?op=ocroped&val=1200,630,1000,1000,0,0&sum=0ZCX2CRVbos", use_column_width=True)  # Replace "your_image.png" with the path to your image

st.title("Eco-Score Calculator")

# Eco-score data structure
eco_data = {
    "Energy": {
        "Equipment": {
            "Source of electricity": {
                "Green electricity (on site electricity: estimate)": "A",
                "Green electricity (on site electricity: consumption known)": "A",
                "Electricity (on site electricity: estimate)": "C",
                "Electricity (on site electricity: consumption known)": "C",
                "Diesel generator (consumption known)": "D",
                "Diesel generator (consumption estimate)": "D",
                "Indirect emissions, measured externally": "D",
            },
            "Power consumption": {
                "Unknown power consumption": None,
                "low power consumption": "A",
                "average power consumption": "C",
                "higher power consumption": "D",
            },
            "Power supply lighting": {
                "including set lighting": "D",
                "excluding set lighting": "B",
            },
        },
        "Location": {
            "Source": {
            "Locations: Green electricity (consumption known)": "A",
            "Locations: Electricity (consumption known)": "C",
            "Locations: Green electricity (generic)": "A",
            "Locations: Electricity demand (generic)": "C",
            "Indirect emissions, measured externally": "D",
            }
        },
        "Film Studio": {
            "Source": {
                "Green electricity film studio (estimate)": "A",
                "Green electricity film studio (consumption known)": "A",
                "Electricity film studio (estimate)": "C",
                "Electricity film studio (consumption known)": "C",
                "Natural gas": "D",
                "Heating oil light": "D",
                "Liquefied petroleum gas": "D",
                "Indirect emissions, measured externally": "D",
            },
            "Power consumption": {
                "Unknown power consumption": None,
                "low power consumption": "A",
                "average power consumption": "C",
                "higher power consumption": "D",
            },
        },
        "Post-production (Film editing)": {
            "Source": {
                "Grading workstation": "B",
                "Grading workstation (green electricity)": "A",
                "Motion design workstation": "B",
                "Motion design workstation (green electricity)": "A",
                "Cutting/Editing workstation": "B",
                "Cutting/Editing workstation (green electricity)": "A",
                "Indirect emissions, measured externally": "D",
            },
        },
        "Post-production (Sound editing)": {
            "Source": {
                "Sound design workstation": "B",
                "Sound design workstation (green electricity)": "A",
                "Indirect emissions, measured externally": "D",
            },
        },
        "Post-production (Other)": {
            "Source": {
                "Hard disk archive": "C",
                "Cloud-Storage": "B",
                "Generic postproduction workstation": "C",
                "Generic postproduction workstation (green electricity)": "A",
                "Indirect emissions, measured externally": "D",
            },
        },
        "Offices (trucks in our case)": {
            "Source": {
                "Offices: Heat demand (generic)": "D",
                "Offices: Electricity demand (generic)": "C",
                "Offices: Green electricity (generic)": "A",
                "Indirect emissions, measured externally": "D",
            },
            "Fuel type": {
                "Unknown": None,
                "Natural gas": "D",
                "Liquid gas": "D",
                "Heating oil": "D",
                "Lignite": "D",
                "Coking coal": "D",
                "Wood general": "B",
                "Wood pellets": "B",
                "Wood chips": "B",
                "District heat (average mix)": "C",
                "Electricity (average mix, CH)": "C",
                "Green electricity": "A",
            },
            "Building type": {
                "Office building, heated only": "B",
                "Office building, heated and air-conditioning": "C",
            },
            "Heat consumption": {
                "Average heat consumption": "B",
                "Low heat consumption": "A",
                "High heat consumption": "D",
            },
        },
    },
    "Travel/Transport": {
        "Accommodation": {
            "Source": {
                "Youth Hostel, shared room": "A",
                "Hotel (average, Switzerland)": "B",
                "Hotel (average, international)": "C",
                "Hotel (certified, climate-friendly, Switzerland)": "A",
                "Hotel (luxury class, Switzerland)": "D",
                "Indirect emissions, measured externally": "D",
            },
        },
        "Passenger transport": {
            "Source": {
                "Diesel": "D",
                "Petrol": "D",
                "Electricity consumption": "B",
                "Green electricity consumption": "A",
                "Car (distance estimate)": "D",
                "Public transport mix (Switzerland)": "A",
                "Autobus (Switzerland)": "B",
                "Cable car (Switzerland)": "B",
                "Coach": "C",
                "Long distance rail (Switzerland)": "A",
                "Passenger ship (Switzerland)": "B",
                "Diesel by distance": "D",
                "Petrol by distance": "D",
                "Indirect emissions, measured externally": "D",
            },
        },
    },
    "Catering": {
        "Meals": {
            "Meat consumption": {
                "Mixed food diet": "C",
                "Meat-reduced": "B",
                "Vegetarian": "A",
                "Vegan": "A",
            },
            "Method of production": {
                "Conventional": "C",
                "Partially organic (ca. 50%)": "B",
                "Organic": "A",
            },
            "Regional, seasonal (specification of food)": {
                "Standard": "C",
                "Partially regional and seasonal": "B",
                "Regional and seasonal": "A",
            },
        },
        "Dishes": {
            "Source": {
                "Reusable cups": "A",
                "Disposable cups": "D",
                "Plates": "D",
                "Disposable cutlery": "D",
                "Indirect emissions, measured externally": "D",
            },
        },
    },
    "Material": {
        "Set construction": {
            "Source": {
                "flooring: linoleum floor": "B",
                "flooring: solid wood parquet": "B",
                "flooring: PVC": "D",
                "flooring: PVC vinyl tile floor": "D",
                "flooring: carpet": "C",
                "wood construction: Beam/four-by-two/timber/slats": "B",
                "wood construction: plywood": "B",
                "wood construction: medium density fibreboard (MDF)": "C",
                "Timber construction (monetary estimate)": "B",
                "EPS hard foam for scenery construction (Styropor®)": "D",
                "plasterboard: monetary estimation": "C",
                "Dispersion wall paint (m2)": "C",
                "Solvent-based varnish (m2)": "D",
                "Water-based paint (m2)": "C",
                "other materials: foil roll": "D",
                "other materials: gaffer tape": "D",
                "Indirect emissions, measured externally": "D",
            },
        },
        "Prop vehicles": {
            "Source": {
                "Petrol": "D",
                "Diesel": "D",
                "Maritime Diesel Oil (MDO)": "D",
                "Indirect emissions, measured externally": "D",
            },
        },
        "Costumes": {
            "Source": {
                "Costume rental/reuse": "A",
                "Costume purchase": "C",
                "Indirect emissions, measured externally": "D",
            },
        },
        "Laundry drying": {
            "Source": {
                "Tumble dryer": "D",
                "Clothesline": "A",
            },
        },
        "Laundry detergent": {
            "Source": {
                "Conventional": "D",
                "Organic": "B",
            },
        },
        "Waste": {
            "Source": {
                "Residual waste (for incineration, kg)": "D",
                "Residual waste (for incineration, bags)": "D",
                "Indirect emissions, measured externally": "D",
            },
        },
    },
}

# Map letter scores to numeric values
score_map = {"A": 1, "B": 2, "C": 3, "D": 4}

# Function to get color based on score (letter grades)
def get_score_color(letter_score):
    score_colors = {
        "A": "#4CAF50",         # Green
        "A-": "#8BC34A",        # Light Green
        "B+": "#FFEB3B",        # Light Yellow
        "B": "#FFC107",         # Yellow
        "B-": "#FFB300",        # Dark Yellow
        "C+": "#FF9800",        # Light Orange
        "C": "#FF5722",         # Orange
        "C-": "#E64A19",        # Dark Orange
        "D+": "#FF5252",        # Light Red
        "D": "#F44336",         # Red
    }
    return score_colors.get(letter_score, "#9E9E9E")  # Default to gray for invalid scores

# Function to convert numeric score to letter score
def numeric_to_letter(score):
    if score == 1:
        return "A"
    elif 1 < score <= 1.5:
        return "A-"
    elif 1.5 < score <= 2:
        return "B+"
    elif score == 2:
        return "B"
    elif 2 < score <= 2.5:
        return "B-"
    elif 2.5 < score <= 3:
        return "C+"
    elif score == 3:
        return "C"
    elif 3 < score <= 3.5:
        return "C-"
    elif 3.5 < score < 4:
        return "D+"
    elif score == 4:
        return "D"
    else:
        return "N/A"

# Initialize selected_options as an empty dictionary
selected_options = {}

# Function to calculate the eco-score
def compute_score(selected_options):
    category_scores = {}
    total_score = 0
    total_count = 0
    
    for category, subcategories in selected_options.items():
        category_total = 0
        category_count = 0
        for subcategory, groups in subcategories.items():
            for group, letter_score in groups.items():
                if letter_score and letter_score != "No score":  # Ignore "No score" (not considered when computing the mean)
                    score_value = score_map.get(letter_score.upper(), 0)
                    category_total += score_value
                    category_count += 1
        if category_count > 0:
            category_avg = category_total / category_count
            category_scores[category] = category_avg
            total_score += category_total
            total_count += category_count

    overall_score = total_score / total_count if total_count > 0 else 0 # The overall score is the average of all individual scores, not the average of averages
    return category_scores, overall_score

# Dynamically display options for each category
for category, subcategories in eco_data.items():
    st.markdown(f"<div class='red-band'>{category}</div>", unsafe_allow_html=True)
    selected_options[category] = {}
    for subcategory, groups in subcategories.items():
        st.subheader(subcategory)
        selected_options[category][subcategory] = {}
        for group, options in groups.items():
            st.markdown(f"<div class='bold-text'>{group}</div>", unsafe_allow_html=True)
            selected_option = st.selectbox(
                f"Select an option for {group}",
                options=list(options.keys()),
                key=f"{category}_{subcategory}_{group}",
            )
            selected_options[category][subcategory][group] = options[selected_option]

# Unified function to display results in a layout
def display_score_layout(label, numeric_score, letter_score, is_category=False):
    score_color = get_score_color(letter_score)
    neutral_color = "#E0E0E0"  # Neutral color for background boxes

    # Smaller padding for category results
    padding = "10px" if is_category else "20px"
    font_size = "18px" if is_category else "24px"

    # Streamlit columns to organize layout
    col1, col2, col3 = st.columns([1, 1, 1], gap="large")

    # Label box (Category or Overall)
    with col1:
        st.markdown(
            f"""
            <div style="background-color: {neutral_color}; padding: {padding}; border-radius: 5px; text-align: center; margin: 10px 0;">
                <span style="font-size: {font_size}; font-weight: bold;">{label}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Numeric score box
    with col2:
        st.markdown(
            f"""
            <div style="background-color: {neutral_color}; padding: {padding}; border-radius: 5px; text-align: center; margin: 10px 0;">
                <span style="font-size: {font_size}; font-weight: bold;">{numeric_score:.2f}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Letter score box (with color)
    with col3:
        st.markdown(
            f"""
            <div style="background-color: {score_color}; padding: {padding}; border-radius: 5px; text-align: center; color: white; margin: 10px 0;">
                <span style="font-size: {font_size}; font-weight: bold;">{letter_score}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# Initialize session state for toggling subcategory visibility
if "show_subcategories" not in st.session_state:
    st.session_state["show_subcategories"] = False

# Function to toggle subcategories state
def toggle_subcategories():
    st.session_state["show_subcategories"] = not st.session_state["show_subcategories"]

# Function to compute and display subcategories
def display_subcategories(category, subcategories, score_map):
    for subcategory, groups in subcategories.items():
        # Calculate subcategory average score
        subcategory_total = 0
        subcategory_count = 0
        for group, letter_score in groups.items():
            if letter_score and letter_score != "No score":  # Ignore invalid scores
                score_value = score_map.get(letter_score.upper(), 0)
                subcategory_total += score_value
                subcategory_count += 1
        subcategory_numeric_score = subcategory_total / subcategory_count if subcategory_count > 0 else 0
        subcategory_letter_score = numeric_to_letter(subcategory_numeric_score)
        subcategory_color = get_score_color(subcategory_letter_score)

        # Display subcategory scores
        st.markdown(
            f"""
            <div style="font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #8B0000;">
                {subcategory} (Score: {subcategory_letter_score}, Numeric: {subcategory_numeric_score:.2f})
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Expander for group details inside the subcategory
        with st.expander("Show more details", expanded=False):
            for group, letter_score in groups.items():
                group_color = get_score_color(letter_score)
                selected_option = selected_options[category][subcategory][group]

                # Display group details
                col1, col2, col3 = st.columns([3, 2, 1], gap="small")
                with col1:
                    st.markdown(f"**{group}**")
                with col2:
                    st.markdown(f"**{selected_option}**")
                with col3:
                    st.markdown(
                        f"""
                        <div style="background-color: {group_color}; padding: 5px; border-radius: 5px; text-align: center; color: white;">
                            <span style="font-size: 14px;">{letter_score}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

# Main display logic
if st.button("Calculate Eco-Score"):
    # Compute category and overall scores
    category_scores, overall_numeric_score = compute_score(selected_options)
    overall_score_letter = numeric_to_letter(overall_numeric_score)

    # Display overall score
    display_score_layout("Overall Eco-Score", overall_numeric_score, overall_score_letter)

    st.markdown("<hr>", unsafe_allow_html=True)  # Separator

    # Display category scores
    for category, subcategories in selected_options.items():
        category_numeric_score = category_scores[category]
        category_letter_score = numeric_to_letter(category_numeric_score)

        # Display category score in smaller boxes
        display_score_layout(category, category_numeric_score, category_letter_score, is_category=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Add the "Show more details" toggle button
    if st.session_state["show_subcategories"]:
        if st.button("Hide details"):
            toggle_subcategories()
    else:
        if st.button("Show more details"):
            toggle_subcategories()

    # Display subcategories if toggled
    if st.session_state["show_subcategories"]:
        for category, subcategories in selected_options.items():
            display_subcategories(category, subcategories, score_map)

    st.markdown("<hr>", unsafe_allow_html=True)