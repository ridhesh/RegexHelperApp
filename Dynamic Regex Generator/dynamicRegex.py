import re
import streamlit as st

def generate_regex(conditions):
    """
    Generate a regex pattern dynamically based on the selected conditions.
    
    Parameters:
    - conditions: A list of dictionaries containing condition names and parameters.
    
    Returns:
    - A string representing the generated regex pattern.
    """
    pattern_parts = []

    for condition in conditions:
        if condition["type"] == "letters":
            pattern_parts.append(r"[A-Za-z]+")
        elif condition["type"] == "digits":
            pattern_parts.append(r"\d+")
        elif condition["type"] == "alphanumeric":
            pattern_parts.append(r"[A-Za-z0-9]+")
        elif condition["type"] == "minimum_length":
            min_length = condition["value"]
            pattern_parts.append(r"(?=.{%d,})" % min_length)  # Lookahead for min length
        elif condition["type"] == "maximum_length":
            max_length = condition["value"]
            pattern_parts.append(r".{0,%d}" % max_length)  # Match up to max length
        elif condition["type"] == "special_characters":
            special_chars = re.escape(condition["value"])  # Escape special characters
            pattern_parts.append(r"[{}]+".format(special_chars))
        elif condition["type"] == "starts_with":
            start_char = condition["value"]
            pattern_parts.append(r"^{}".format(re.escape(start_char)))
        elif condition["type"] == "ends_with":
            end_char = condition["value"]
            pattern_parts.append(r"{}$".format(re.escape(end_char)))

    # Combine all parts into a complete regex
    full_pattern = "".join(pattern_parts)
    return full_pattern

def main():
    st.title("Dynamic Regex Generator with Infinite Conditions")

    st.subheader("Select and Configure Conditions")
    conditions = []

    # Options for conditions
    if st.checkbox("Only Letters"):
        conditions.append({"type": "letters"})

    if st.checkbox("Only Digits"):
        conditions.append({"type": "digits"})

    if st.checkbox("Alphanumeric"):
        conditions.append({"type": "alphanumeric"})

    if st.checkbox("Minimum Length"):
        min_length = st.number_input("Enter Minimum Length:", min_value=1, value=1)
        conditions.append({"type": "minimum_length", "value": min_length})

    if st.checkbox("Maximum Length"):
        max_length = st.number_input("Enter Maximum Length:", min_value=1, value=10)
        conditions.append({"type": "maximum_length", "value": max_length})

    if st.checkbox("Special Characters"):
        special_chars = st.text_input("Enter Special Characters:")
        if special_chars:
            conditions.append({"type": "special_characters", "value": special_chars})

    if st.checkbox("Starts With"):
        start_char = st.text_input("Enter Starting Character(s):")
        if start_char:
            conditions.append({"type": "starts_with", "value": start_char})

    if st.checkbox("Ends With"):
        end_char = st.text_input("Enter Ending Character(s):")
        if end_char:
            conditions.append({"type": "ends_with", "value": end_char})

    # Generate regex on button click
    if st.button("Generate Regex"):
        regex_pattern = generate_regex(conditions)
        st.write("Generated Regex Pattern: ", f"`{regex_pattern}`")

        # Testing it with sample input
        sample_input = st.text_input("Enter Sample Input for Testing:")
        if sample_input:
            if re.match(regex_pattern, sample_input):
                st.success("Input matches the regex!")
            else:
                st.error("Input does not match the regex.")

if __name__ == "__main__":
    main()
