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
                "Electricity (on site electricity: estimate)": "B",
                "Electricity (on site electricity: consumption known)": "B",
                "Diesel generator (consumption known)": "D",
                "Diesel generator (consumption estimate)": "D",
                "Indirect emissions, measured externally": None,
            },
            "Power consumption": {
                "Unknown power consumption": None,
                "Low power consumption": "A",
                "Average power consumption": "C",
                "Higher power consumption": "D",
            },
            "Power supply lighting": {
                "Including set lighting": "D",
                "Excluding set lighting": "B",
            },
        },
        "Location": {
            "Source": {
            "Locations: Green electricity (consumption known)": "A",
            "Locations: Electricity (consumption known)": "B",
            "Locations: Green electricity (generic)": "A",
            "Locations: Electricity demand (generic)": "B",
            "Indirect emissions, measured externally": None,
            }
        },
        "Film Studio": {
            "Source": {
                "Green electricity film studio (estimate)": "A",
                "Green electricity film studio (consumption known)": "A",
                "Electricity film studio (estimate)": "B",
                "Electricity film studio (consumption known)": "B",
                "Natural gas": "D",
                "Heating oil light": "D",
                "Liquefied petroleum gas": "D",
                "Indirect emissions, measured externally": None,
            },
            "Power consumption": {
                "Unknown power consumption": None,
                "Low power consumption": "A",
                "Average power consumption": "C",
                "Higher power consumption": "D",
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
                "Indirect emissions, measured externally": None,
            },
        },
        "Post-production (Sound editing)": {
            "Source": {
                "Sound design workstation": "B",
                "Sound design workstation (green electricity)": "A",
                "Indirect emissions, measured externally": None,
            },
        },
        "Post-production (Other)": {
            "Source": {
                "Hard disk archive": "C",
                "Cloud-Storage": "B",
                "Generic postproduction workstation": "C",
                "Generic postproduction workstation (green electricity)": "A",
                "Indirect emissions, measured externally": None,
            },
        },
        "Offices": {
            "Source": {
                "Offices: Heat demand (generic)": "D",
                "Offices: Electricity demand (generic)": "B",
                "Offices: Green electricity (generic)": "A",
                "Indirect emissions, measured externally": None,
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
                "Electricity (average mix, CH)": "B",
                "Green electricity": "A",
            },
            "Building type": {
                "Office building, heated only": "B",
                "Office building, heated and air-conditioning": "C",
            },
            "Heat consumption": {
                "Average heat consumption": "C",
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
                "Indirect emissions, measured externally": None,
            },
        },
        "Passenger transport": {
            "Source": {
                "Diesel": "D",
                "Diesel by distance": "D",
                "Petrol": "D",
                "Petrol by distance": "D",
                "Electricity consumption": "B",
                "Electricity by distance": "B",
                "Green electricity consumption": "A",
                "Green electricity by distance": "A",
                "Car (distance estimate)": "D",
                "Public transport mix (Switzerland)": "A",
                "Autobus (Switzerland)": "B",
                "Cable car (Switzerland)": "B",
                "Coach": "C",
                "Long distance rail (Switzerland)": "A",
                "Long distance rail (Europe)": "A",
                "Passenger ship (Switzerland)": "B",
                "Indirect emissions, measured externally": None,
            },
            "Average fuel consumption": {
                "Between 2-5 L/100km": "A",
                "Between 5-7 L/100km": "B",
                "Between 7-10 L/100km": "C",
                "More than 10 L/100km": "D",
            },
        },
        "Logistics": {
            "Source": {
                "Diesel consumption (NEW 2024)": "D",
                "Petrol consumption (NEW 2024)": "D",
                "Natural gas (CNG) consumption (NEW 2024)": "D",
                "Biomethane (Bio-CNG) Consumption (NEW 2024)": "B",
                "Electricity consumption (NEW 2024)": "B",
                "Green electricity consumption (NEW 2024)": "A",
                "Logistics (road) external provider, generic (NEW 2024)": "D",
                "Logistics (road) own, Ø consumption known (NEW 2024)": None,
                "Van 3.5t (NEW 2024)": "C",
                "Truck 7.5t (NEW 2024)": "C",
                "Truck 18t (NEW 2024)": "C",
                "Truck 26t (NEW 2024)": "C",
                "Truck 32t (NEW 2024)": "D",
                "Truck 40t (NEW 2024)": "D",
                "Transporter 3.5t (battery electric) (NEW 2024)": "A",
                "Lorry 7.5t (battery electric) (NEW 2024)": "A",
                "Lorry 18t (battery electric) (NEW 2024)": "A",
                "Lorry 26t (battery electric) (NEW 2024)": "B",
                "Articulated lorry 32t (battery electric) (NEW 2024)": "B",
                "Articulated lorry 40t (battery electric) (NEW 2024)": "B",
                "Train (average) (NEW 2024)": "A",
                "Container vessel (average) (NEW 2024)": "C",
                "Diesel consumption": "D",
                "Petrol consumption": "D",
                "LPG consumption": "D",
                "Natural gas (CNG) consumption": "D",
                "Biomethane (Bio-CNG) Consumption": "C",
                "Container vessel (average)": "C",
                "Externally determined indirect emissions": None,
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
                "Indirect emissions, measured externally": None,
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
                "wood construction: medium density fibreboard (MDF)": "D",
                "Timber construction (monetary estimate)": "B",
                "EPS hard foam for scenery construction (Styropor®)": "D",
                "plasterboard: monetary estimation": "C",
                "Dispersion wall paint (m2)": "C",
                "Solvent-based varnish (m2)": "D",
                "Water-based paint (m2)": "C",
                "other materials: foil roll": "D",
                "other materials: gaffer tape": "D",
                "Indirect emissions, measured externally": None,
            },
        },
        "Prop vehicles": {
            "Source": {
                "Petrol": "D",
                "Diesel": "D",
                "Maritime Diesel Oil (MDO)": "D",
                "Indirect emissions, measured externally": None,
            },
        },
        "Costumes": {
            "Source": {
                "Costume rental/reuse": "A",
                "Costume purchase": "C",
                "Indirect emissions, measured externally": None,
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
                "Organic": "A",
            },
        },
        "Waste": {
            "Source": {
                "Residual waste (for incineration, kg)": "D",
                "Residual waste (for incineration, bags)": "D",
                "Indirect emissions, measured externally": None,
            },
        },
    },
}

# Map letter scores to numeric values
score_map = {"A": 1, "B": 2, "C": 3, "D": 4}

# Function to get color based on score (letter grades)
def get_score_color(letter_score):
    # Define colors for valid letter scores
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

    # Handle invalid or missing scores
    if not letter_score or letter_score == "None" or letter_score == "No score":
        return "#9E9E9E"  # Gray for invalid or missing scores
    
    # Get the corresponding color or default to gray
    return score_colors.get(letter_score.upper(), "#9E9E9E")  # Default to gray

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

        subcategory_scores = {}  # Dictionary to store subcategory scores

        for subcategory, groups in subcategories.items():
            subcategory_total = 0
            subcategory_count = 0

            for group, group_data in groups.items():
                # Retrieve the score (letter score) for each group
                group_scores = group_data.get("scores", [])
                if group_scores:  # Calculate the average score for the group
                    if len(group_scores) == 1:
                        group_avg_score = score_map[group_scores[0].upper()]  # Single option selected
                    else:
                        group_avg_score = sum(score_map[score.upper()] for score in group_scores) / len(group_scores)  # Average score for multiple options

                    # Store the average score for this group
                    group_data["group_score"] = group_avg_score
                    subcategory_total += group_avg_score
                    subcategory_count += 1    
                    
                else:
                    # If no scores are selected, do not include the group
                    group_data["group_score"] = None
            
            # Compute subcategory average
            if subcategory_count > 0:
                subcategory_avg_score = subcategory_total / subcategory_count
                subcategory_scores[subcategory] = subcategory_avg_score
                category_total += subcategory_avg_score
                category_count += 1
            else:
                subcategory_scores[subcategory] = None  # No score for this subcategory


        if category_count > 0:
            category_avg_score = category_total / category_count
            category_scores[category] = category_avg_score
            total_score += category_total
            total_count += category_count
        else:
            category_scores[category] = None  # No valid data for this category
    
    # Compute overall score
    overall_score = total_score / total_count if total_count > 0 else None # The overall score is the average of averages
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
            
            # Use st.multiselect to allow selecting multiple options
            selected_options_group = st.multiselect(
                f"Select options for {group}",
                options=list(options.keys()),
                key=f"{category}_{subcategory}_{group}",
            )

            # Store the selected options and their corresponding scores
            selected_options[category][subcategory][group] = {
                "options": selected_options_group,  # List of selected options
                "scores": [options[opt] for opt in selected_options_group if options[opt] is not None],  # Corresponding scores
            }
            
# Unified function to display results in a layout
def display_score_layout(label, numeric_score, letter_score, is_category=False):
    score_color = get_score_color(letter_score)
    neutral_color = "#E0E0E0"  # Neutral color for background boxes

    # Smaller padding for category results
    padding = "10px" if is_category else "20px"
    font_size = "18px" if is_category else "24px"

    # Convert numeric_score to a formatted string or "N/A" if it's not a number
    if isinstance(numeric_score, (int, float)):
        formatted_numeric_score = f"{numeric_score:.2f}"
    else:
        formatted_numeric_score = "N/A"
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


# Function to display subcategories with their numeric scores and letter scores
def display_subcategories(category, subcategories, score_map):
    for subcategory_name, groups in subcategories.items():
        # Retrieve the subcategory score
        subcategory_score = subcategories[subcategory_name].get("subcategory_score", None)
        subcategory_letter_score = numeric_to_letter(subcategory_score) if subcategory_score is not None else "No score"
        subcategory_numeric_score = f"{subcategory_score:.2f}" if subcategory_score is not None else "N/A"

        # Display subcategory header with score
        st.markdown(
            f"""
            <div style="font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #8B0000;">
                {subcategory_name} (Score: {subcategory_letter_score}, Numeric: {subcategory_numeric_score:.2f})
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Display group details indented to the right
        st.markdown(
            """
            <div style="margin-left: 30px;">
            """,
            unsafe_allow_html=True,
        )

        for group, group_data in groups.items():
            group_score = group_data.get("group_score", None)
            if group_score is not None:
                group_letter_score = numeric_to_letter(group_score)
                selected_options = group_data.get("options", [])
            
                # Display group name and score
                st.markdown(f"**Group: {group}** (Score: {group_letter_score})")
            
                # Use columns to display selected options and their scores
                for option in selected_options:
                    # Retrieve letter score and color for the option
                    option_score = score_map.get(option.upper(), "No score")
                    letter_score = option_score.upper() if option_score != "No score" else None
                    score_color = get_score_color(letter_score)

                    # Display option name and score in colored boxes
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"- {option}")
                    with col2:
                        st.markdown(
                            f"""
                            <div style="background-color: {score_color}; padding: 5px; border-radius: 5px; text-align: center; color: white;">
                                <span style="font-size: 14px; font-weight: bold;">{option_score}</span>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
            else:
                st.markdown(f"**Group: {group}**: No options selected")


# Main display logic
if st.button("Calculate Eco-Score"):
    # Compute category and overall scores
    category_scores, overall_numeric_score = compute_score(selected_options)
    overall_score_letter = numeric_to_letter(overall_numeric_score) if overall_numeric_score is not None else "No score"
    
    # Display overall score
    display_score_layout("Overall Eco-Score", overall_numeric_score if overall_numeric_score is not None else "N/A", overall_score_letter)

    st.markdown("<hr>", unsafe_allow_html=True)  # Separator

    # Display category scores
    for category, subcategories in selected_options.items():
        category_numeric_score = category_scores.get(category, None)
        category_letter_score = numeric_to_letter(category_numeric_score) if category_numeric_score is not None else "No score"

        # Display category score in smaller boxes
        display_score_layout(category, category_numeric_score if category_numeric_score is not None else "N/A", category_letter_score, is_category=True)

        # Expander for subcategories within this category
        with st.expander(f"Show details for {category}", expanded=False):
            display_subcategories(category, subcategories, score_map)

    st.markdown("<hr>", unsafe_allow_html=True)
