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

# Add an image at the top
st.image("https://cdn.unitycms.io/images/2lnv07LWaRb8rdPxOqTKwI.jpg?op=ocroped&val=1200,630,1000,1000,0,0&sum=0ZCX2CRVbos", use_column_width=True)  # Replace "your_image.png" with the path to your image

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

      
# Streamlit UI

# App title
st.title("Eco-Score Calculator")

# Display the results with collapsible sections
def display_results(category_scores, overall_score):
    overall_letter_score = numeric_to_letter(overall_score)
    overall_color = get_score_color(overall_letter_score)

    # Display overall score
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="display: inline-block; padding: 20px; border-radius: 10px; background-color: {overall_color}; color: white; font-weight: bold; font-size: 24px;">
                Overall Eco-Score
            </div>
            <div style="display: inline-block; padding: 20px; border-radius: 10px; background-color: #E0E0E0; color: black; font-weight: bold; font-size: 24px; margin-left: 10px;">
                {overall_score:.2f}
            </div>
            <div style="display: inline-block; padding: 20px; border-radius: 10px; background-color: {overall_color}; color: white; font-weight: bold; font-size: 24px; margin-left: 10px;">
                {overall_letter_score}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Display category results
    for category, category_score in category_scores.items():
        category_letter_score = numeric_to_letter(category_score)
        category_color = get_score_color(category_letter_score)

        # Display category header
        st.markdown(
            f"""
            <div style="background-color: #8B0000; padding: 10px; border-radius: 5px; color: white; font-size: 24px; font-weight: bold; text-align: left; width: 100%;">
                {category}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Display category scores in boxes
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
                <div style="flex: 1; text-align: center; background-color: #E0E0E0; padding: 10px; border-radius: 5px; font-weight: bold;">
                    {category}
                </div>
                <div style="flex: 1; text-align: center; background-color: #E0E0E0; padding: 10px; border-radius: 5px; font-weight: bold; margin-left: 10px;">
                    {category_score:.2f}
                </div>
                <div style="flex: 1; text-align: center; background-color: {category_color}; padding: 10px; border-radius: 5px; color: white; font-weight: bold; margin-left: 10px;">
                    {category_letter_score}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Add a collapsible section for subcategories
        with st.expander(f"View Subcategories for {category}"):
            for subcategory, groups in selected_options[category].items():
                # Calculate subcategory score
                subcategory_total = 0
                subcategory_count = 0
                for group, letter_score in groups.items():
                    if letter_score and letter_score != "No score":
                        score_value = score_map.get(letter_score.upper(), 0)
                        subcategory_total += score_value
                        subcategory_count += 1
                subcategory_score = (
                    subcategory_total / subcategory_count
                    if subcategory_count > 0
                    else 0
                )
                subcategory_letter_score = numeric_to_letter(subcategory_score)
                subcategory_color = get_score_color(subcategory_letter_score)

                # Display subcategory scores
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <div style="flex: 2; text-align: left; font-weight: bold;">
                            {subcategory}
                        </div>
                        <div style="flex: 1; text-align: center; background-color: #E0E0E0; padding: 5px; border-radius: 5px; font-weight: bold; margin-left: 10px;">
                            {subcategory_score:.2f}
                        </div>
                        <div style="flex: 1; text-align: center; background-color: {subcategory_color}; padding: 5px; border-radius: 5px; color: white; font-weight: bold; margin-left: 10px;">
                            {subcategory_letter_score}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Add another collapsible section for groups in the subcategory
                with st.expander(f"View Groups for {subcategory}"):
                    for group, letter_score in groups.items():
                        if letter_score:
                            group_color = get_score_color(letter_score)
                            st.markdown(
                                f"""
                                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                    <div style="flex: 2; text-align: left;">
                                        {group}
                                    </div>
                                    <div style="flex: 1; text-align: center; background-color: {group_color}; padding: 5px; border-radius: 5px; color: white; font-weight: bold; margin-left: 10px;">
                                        {letter_score}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )


# Add the "Calculate Eco-Score" button
if st.button("Calculate Eco-Score"):
    category_scores, overall_score = compute_score(selected_options)
    display_results(category_scores, overall_score)
