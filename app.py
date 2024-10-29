# import streamlit as st
# import pandas as pd
# import os
# import re

# # Sample dataframeSafai function as defined above
# def dataframeSafai(csv_file):
#     df = pd.read_csv(csv_file)
#     columns_to_drop = ['certificate_preview', 'extension_preview', 'appeal_status', 'complain_against_status', 'additional_data']
#     df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')

#     def format_scrutiny_status(status):
#         if isinstance(status, str):
#             if "In Process More Information Required" in status:
#                 desk_match = re.search(r"Desk -(\d+)", status)
#                 desk_number = desk_match.group(1) if desk_match else ""
#                 return f"In Process (Desk {desk_number} Comment)"
#             else:
#                 return status
#         return status

#     def format_comments(text):
#         if isinstance(text, str):
#             lines = text.split('\n')
#             formatted_text = ""
#             for line in lines:
#                 if re.match(r'^\d+\)', line) or re.match(r'^\d+\.', line):
#                     formatted_text += f'{line}'
#                 elif re.match(r'^[A-Z]\)', line):
#                     formatted_text += f'{line}'
#                 else:
#                     formatted_text += line + '\n'
#             formatted_text = formatted_text.strip()
#             return f'{formatted_text}'
#         return text

#     df['scrutiny_status'] = df['scrutiny_status'].apply(format_scrutiny_status)
#     df['comments'] = df['comments'].apply(format_comments)

#     return df


# # Function to load user data from CSV
# def load_user_data():
#     return pd.read_csv('users.csv')


# # Function to authenticate user
# def authenticate_user(user_id, password, user_data):
#     if user_id in user_data['user_id'].values:
#         stored_password = user_data[user_data['user_id'] == user_id]['password'].values[0]
#         return stored_password == password
#     return False


# # Load or create persistent data file
# def load_persistent_data():
#     if os.path.exists('uploaded_data.csv'):
#         return pd.read_csv('uploaded_data.csv')
#     return pd.DataFrame()


# def save_persistent_data(df):
#     df.to_csv('uploaded_data.csv', index=False)
    
# def style_dataframe(df):
#     def apply_status_colors(val):
#         color = ''
#         if isinstance(val, str):
#             if "pending" in val.lower():
#                 color = 'red'
#             elif "done" in val.lower():
#                 color = 'green'
#             elif "in process" in val.lower():
#                 color = 'orange'
#         return f'color: {color}' if color else ''

#     # Apply color based on conditions for specific columns
#     styled_df = df.style.map(apply_status_colors, subset=['application_status', 'payment_status', 'scrutiny_status'])

#     styled_df = styled_df.set_table_styles(
#         [
#             {'selector': 'thead th',
#              'props': 'background-color: #003366; color: white; text-align: center; font-size: 16px; font-family: Arial;'},
#             {'selector': 'tbody td', 'props': 'text-align: center; font-family: Arial; border: 1px solid black;'},
#         ]
#     ).set_properties(**{
#         'border': '1px solid black',
#         'font-size': '14px'
#     })

#     styled_df = styled_df.applymap(lambda x: '', subset=pd.IndexSlice[::2, :]).set_properties(
#         subset=pd.IndexSlice[::2, :], **{'background-color': 'lightgray'}
#     ).set_properties(
#         subset=pd.IndexSlice[1::2, :], **{'background-color': 'white'}
#     )

#     return styled_df

# # Main Streamlit application
# def main():
#     st.set_page_config(layout="wide")

#     # Session state for user authentication
#     if 'logged_in' not in st.session_state:
#         st.session_state['logged_in'] = False
#         st.session_state['user_role'] = None

#     # User login page
#     if not st.session_state['logged_in']:
#         st.title('Login')
#         user_id = st.text_input('User ID')
#         password = st.text_input('Password', type='password')
#         if st.button('Login'):
#             user_data = load_user_data()
#             if authenticate_user(user_id, password, user_data):
#                 st.session_state['logged_in'] = True
#                 st.session_state['user_role'] = 'admin' if user_id == 'admin' else 'user'
#                 st.success('Login successful!')
#                 st.rerun()  # Force rerun after login to go to main content
#             else:
#                 st.error('Invalid credentials')
#     else:
#         # Display tabs after login
#         tab1, tab2 = st.tabs(['Dashboard', 'Admin'])

#         # Dashboard Tab (Visible to all users)
#         with tab1:
#             st.subheader('Project Status')
#             df = load_persistent_data()

#             if not df.empty:
#                 # Columns to filter
#                 filter_columns = ['application_status', 'payment_status', 'scrutiny_status', 'correction_status', 'extension_status']
#                 filters = {}

#                 # Create a single row for filters
#                 filter_columns_count = len(filter_columns)
#                 cols = st.columns(filter_columns_count)

#                 # Dynamic filtering options based on unique values in columns
#                 for i, col in enumerate(filter_columns):
#                     if col in df.columns:
#                         unique_values = df[col].dropna().unique()  # Get unique values for the column
#                         selected_values = cols[i].multiselect(f"Filter by {col}", unique_values, default=[], key=f"filter_{i}")
#                         filters[col] = selected_values

#                 # Apply filtering based on user selections
#                 for col, selected_values in filters.items():
#                     if selected_values:
#                         df = df[df[col].isin(selected_values)]

#                 # Display styled DataFrame
#                 st.dataframe(style_dataframe(df), use_container_width=True)
#             else:
#                 st.info('No data available. Please ask the admin to upload a CSV.')

#         # Admin Tab (Visible only to admin users)
#         if st.session_state['user_role'] == 'admin':
#             with tab2:
#                 st.title('Admin Panel')

#                 # CSV Upload functionality
#                 uploaded_file = st.file_uploader('Upload CSV', type='csv')
#                 if uploaded_file is not None:
#                     st.success('CSV uploaded successfully!')
#                     df = dataframeSafai(uploaded_file)
#                     save_persistent_data(df)
#                     st.dataframe(style_dataframe(df), use_container_width=True)
#         else:
#             with tab2:
#                 st.error('You do not have admin privileges.')


# # Run the Streamlit app
# if __name__ == '__main__':
#     main()


################# 25th october 2024 update ###############


import streamlit as st
import pandas as pd
import os
import re
import time
# Load user data from CSV
def load_user_data():
    return pd.read_csv('users.csv')
# Authenticate user
def authenticate_user(user_id, password, user_data):
    if user_id in user_data['user_id'].values:
        stored_password = user_data[user_data['user_id'] == user_id]['password'].values[0]
        return stored_password == password
    return False

def dataframeSafai(csv_file):
    df = pd.read_csv(csv_file)
    columns_to_drop = ['certificate_preview', 'extension_preview', 'appeal_status', 'application_status', 'payment_status','correction_status',
                       'extension_status', 'additional_data', 'complain_against_status', 'Unnamed: 0']
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')

    def format_scrutiny_status(status):
        if isinstance(status, str):
            if "In Process More Information Required" in status:
                desk_match = re.search(r"Desk -(\d+)", status)
                desk_number = desk_match.group(1) if desk_match else ""
                return f"In Process (Desk {desk_number} Comment)"
            else:
                return status
        return status

    def format_comments(text):
        if isinstance(text, str):
            lines = text.split('\n')
            formatted_text = ""
            for line in lines:
                if re.match(r'^\d+\)', line) or re.match(r'^\d+\.', line):
                    formatted_text += f'{line}'
                elif re.match(r'^[A-Z]\)', line):
                    formatted_text += f'{line}'
                else:
                    formatted_text += line + '\n'
            formatted_text = formatted_text.strip()
            return f'{formatted_text}'
        return text

    df['scrutiny_status'] = df['scrutiny_status'].apply(format_scrutiny_status)
    df['comments'] = df['comments'].apply(format_comments)

    return df

# Load or create persistent data file
def load_persistent_data():
    if os.path.exists('uploaded_data.csv'):
        return pd.read_csv('uploaded_data.csv')
    return pd.DataFrame()

# Save persistent data
def save_persistent_data(df):
    df.to_csv('uploaded_data.csv', index=False)

# Function to add custom styling to tables with color based on status
def style_dataframe(df):
    # Apply custom colors based on status
    def apply_status_colors(val):
        color = ''
        if isinstance(val, str):
            if "pending" in val.lower():
                color = 'red'
            elif "done" in val.lower():
                color = 'green'
            elif "in process" in val.lower():
                color = 'orange'
        return f'color: {color}; font-weight: bold' if color else 'font-weight: bold'

    # Apply color based on conditions for specific columns and make all text bold
    styled_df = df.style.applymap(apply_status_colors,
                                  subset=['application_status', 'payment_status', 'scrutiny_status'])

    # Table styling
    styled_df = styled_df.set_table_styles(
        [
            # Header styling with bold text, background color, and larger font size
            {'selector': 'thead th',
             'props': 'background-color: #ff9900; color: black; text-align: center; font-size: 30px; font-family: Arial; font-weight: bolder;'},

            # Cell styling with border, alignment, and bold text for all cells
            {'selector': 'tbody td',
             'props': 'text-align: center; font-family: Arial; border: 1px solid black; font-size: 28px; font-weight: bolder;'},
        ]
    ).set_properties(**{
        'border': '1px solid black',  # Strong borders for visibility
    })

    # Alternating row colors for readability
    styled_df = styled_df.applymap(lambda x: '', subset=pd.IndexSlice[::2, :]).set_properties(
        subset=pd.IndexSlice[::2, :], **{'background-color': '#d3d3d3'}  # Light gray for even rows
    ).set_properties(
        subset=pd.IndexSlice[1::2, :], **{'background-color': '#ffffff'}  # White for odd rows
    )

    return styled_df

def main():
    st.set_page_config(layout="wide")
    st.title('Project Status Dashboard')

    # Session state for user authentication and current tab
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['user_role'] = None
        st.session_state['current_tab'] = 'Dashboard'  # Initialize current tab

    # User login page
    if not st.session_state['logged_in']:
        st.title('Login')
        user_id = st.text_input('User ID')
        password = st.text_input('Password', type='password')
        if st.button('Login'):
            user_data = load_user_data()
            if authenticate_user(user_id, password, user_data):
                st.session_state['logged_in'] = True
                st.session_state['user_role'] = 'admin' if user_id == 'admin' else 'user'
                st.success('Login successful!')

                # If admin, open Admin tab without rerunning
                if st.session_state['user_role'] == 'admin':
                    st.session_state['current_tab'] = 'Admin'  # Set to Admin tab
                else:
                    st.session_state['current_tab'] = 'Dashboard'  # Set to Dashboard tab
                    time.sleep(6)  # Wait for 60 seconds before sorting and filtering
                    st.rerun()  # Start sorting and filtering after 60 seconds

            else:
                st.error('Invalid credentials')
    else:
        # Display tabs after login
        tab1, tab2 = st.tabs(['Dashboard', 'Admin'])

        # Dashboard Tab
        with tab1:
            if st.session_state['user_role'] == 'user':
                st.subheader('Project Status')
                df = load_persistent_data()

                if not df.empty:
                    # Display area
                    display_area = st.empty()

                    # Get unique values of 'scrutiny_status'
                    unique_scrutiny_values = df['scrutiny_status'].dropna().unique()

                    # Infinite loop for live updates only when the Dashboard tab is active
                    while True:
                        if st.session_state['current_tab'] == 'Dashboard':
                            for value in unique_scrutiny_values:
                                # Filter rows with the current `scrutiny_status` value and shuffle within this subset
                                prioritized_rows = df[df['scrutiny_status'] == value].sample(frac=1).reset_index(
                                    drop=True)

                                # Shuffle remaining rows that do not have the current `scrutiny_status` value
                                remaining_rows = df[df['scrutiny_status'] != value].sample(frac=1).reset_index(
                                    drop=True)

                                # Concatenate the shuffled groups with prioritized rows on top
                                prioritized_df = pd.concat([prioritized_rows, remaining_rows]).reset_index(drop=True)

                                # Display with styling
                                display_area.dataframe(style_dataframe(prioritized_df), use_container_width=True)
                                time.sleep(25)  # Interval for each filter display
                        else:
                            # Pause live updates if not on Dashboard tab
                            time.sleep(1)  # Prevents tight loop

                else:
                    st.info('No data available. Please upload a CSV.')

        # Admin Tab (Visible only to admin users)
        with tab2:
            if st.session_state['user_role'] == 'admin':
                st.title('Admin Panel')
                uploaded_file = st.file_uploader('Upload CSV', type='csv')
                if uploaded_file is not None:
                    st.success('CSV uploaded successfully!')

                    df = dataframeSafai(uploaded_file)
                    save_persistent_data(df)
                    st.dataframe(style_dataframe(df), use_container_width=True)
                else:
                    st.warning('Please upload a CSV file.')
            else:
                st.error('You do not have admin privileges.')


if __name__ == '__main__':
    main()

