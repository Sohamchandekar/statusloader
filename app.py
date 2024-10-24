import streamlit as st
import pandas as pd
import os
import re

# Sample dataframeSafai function as defined above
def dataframeSafai(csv_file):
    df = pd.read_csv(csv_file)
    columns_to_drop = ['certificate_preview', 'extension_preview', 'appeal_status', 'complain_against_status', 'additional_data']
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


# Function to load user data from CSV
def load_user_data():
    return pd.read_csv('users.csv')


# Function to authenticate user
def authenticate_user(user_id, password, user_data):
    if user_id in user_data['user_id'].values:
        stored_password = user_data[user_data['user_id'] == user_id]['password'].values[0]
        return stored_password == password
    return False


# Load or create persistent data file
def load_persistent_data():
    if os.path.exists('uploaded_data.csv'):
        return pd.read_csv('uploaded_data.csv')
    return pd.DataFrame()


def save_persistent_data(df):
    df.to_csv('uploaded_data.csv', index=False)


# # Function to add custom styling to tables
# def style_dataframe(df):
#     styled_df = df.style.set_table_styles(
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
    
def style_dataframe(df):
    def apply_status_colors(val):
        color = ''
        if isinstance(val, str):
            if "pending" in val.lower():
                color = 'red'
            elif "done" in val.lower():
                color = 'green'
            elif "in process" in val.lower():
                color = 'orange'
        return f'color: {color}' if color else ''

    # Apply color based on conditions for specific columns
    styled_df = df.style.map(apply_status_colors, subset=['application_status', 'payment_status', 'scrutiny_status'])

    styled_df = styled_df.set_table_styles(
        [
            {'selector': 'thead th',
             'props': 'background-color: #003366; color: white; text-align: center; font-size: 16px; font-family: Arial;'},
            {'selector': 'tbody td', 'props': 'text-align: center; font-family: Arial; border: 1px solid black;'},
        ]
    ).set_properties(**{
        'border': '1px solid black',
        'font-size': '14px'
    })

    styled_df = styled_df.applymap(lambda x: '', subset=pd.IndexSlice[::2, :]).set_properties(
        subset=pd.IndexSlice[::2, :], **{'background-color': 'lightgray'}
    ).set_properties(
        subset=pd.IndexSlice[1::2, :], **{'background-color': 'white'}
    )

    return styled_df



# Main Streamlit application
def main():
    st.set_page_config(layout="wide")

    # Session state for user authentication
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['user_role'] = None

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
                st.rerun()  # Force rerun after login to go to main content
            else:
                st.error('Invalid credentials')
    else:
        # Display tabs after login
        tab1, tab2 = st.tabs(['Dashboard', 'Admin'])

        # Dashboard Tab (Visible to all users)
        with tab1:
            st.subheader('Project Status')
            df = load_persistent_data()

            if not df.empty:
                # Columns to filter
                filter_columns = ['application_status', 'payment_status', 'scrutiny_status', 'correction_status', 'extension_status']
                filters = {}

                # Create a single row for filters
                filter_columns_count = len(filter_columns)
                cols = st.columns(filter_columns_count)

                # Dynamic filtering options based on unique values in columns
                for i, col in enumerate(filter_columns):
                    if col in df.columns:
                        unique_values = df[col].dropna().unique()  # Get unique values for the column
                        selected_values = cols[i].multiselect(f"Filter by {col}", unique_values, default=[], key=f"filter_{i}")
                        filters[col] = selected_values

                # Apply filtering based on user selections
                for col, selected_values in filters.items():
                    if selected_values:
                        df = df[df[col].isin(selected_values)]

                # Display styled DataFrame
                st.dataframe(style_dataframe(df), use_container_width=True)
            else:
                st.info('No data available. Please ask the admin to upload a CSV.')

        # Admin Tab (Visible only to admin users)
        if st.session_state['user_role'] == 'admin':
            with tab2:
                st.title('Admin Panel')

                # CSV Upload functionality
                uploaded_file = st.file_uploader('Upload CSV', type='csv')
                if uploaded_file is not None:
                    st.success('CSV uploaded successfully!')
                    df = dataframeSafai(uploaded_file)
                    save_persistent_data(df)
                    st.dataframe(style_dataframe(df), use_container_width=True)
        else:
            with tab2:
                st.error('You do not have admin privileges.')


# Run the Streamlit app
if __name__ == '__main__':
    main()
