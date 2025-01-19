import pandas as pd


def save_session_data(data, s_ID, user_name):
    df = pd.DataFrame(data)
    df.to_csv(f"{user_name}_{s_ID}.csv")
    print(f"Session Data saved successfully, file name: {user_name}_{s_ID}.csv")


