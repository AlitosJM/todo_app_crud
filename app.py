
import streamlit as st
import pandas as pd
import plotly.express as px
from db_fxns import (create_table, add_data, view_all_data,
                     view_unique_column, get_tasks, edit_task_data, delete_data)


def fx(string0: str = 'Hi') -> None:
    print(string0)


def main():
    st.title("ToDo App with Streamlit")
    menu = ["Create", "Read", "Update", "Delete", "About"]

    choice = st.sidebar.selectbox("Menu", menu)

    create_table()

    if choice == 'Create':
        st.subheader("Add Items")
        # Layout
        col1, col2 = st.beta_columns(2)

        with col1:
            task = st.text_area("Task To Do")

        with col2:
            task_status = st.selectbox("Status", ["ToDo", "Doing"])
            task_due_date = st.date_input("Due date")

        if st.button("Add Task"):
            add_data(task, task_status, task_due_date)
            st.success("Successfully Added Data: {0}".format(task))

    elif choice == 'Read':
        st.subheader("View Items")
        result = view_all_data()
        st.write(type(result))
        st.write(str(result))
        # st.write(result.__str__())
        # st.write(result.__repr__())
        st.write(result)
        df = pd.DataFrame(result, columns=["Task", "Status", "Due Date"])
        # st.write(df)

        with st.beta_expander("View All Data"):
            st.dataframe(df)

        with st.beta_expander("Task Status"):
            task_df = df['Status'].value_counts().to_frame()
            task_df = task_df.reset_index()
            st.dataframe(task_df)

            p1 = px.pie(task_df, names="index", values="Status")
            st.plotly_chart(p1)

    elif choice == 'Update':
        st.subheader("Edit/Update Items")
        result = view_all_data()

        df = pd.DataFrame(result, columns=["Task", "Status", "Due Date"])

        with st.beta_expander("Current Data"):
            st.dataframe(df)

        # st.write(view_unique_column())
        list_of_task = [i[0] for i in view_unique_column()]
        # st.write(list_of_task)

        selected_task = st.selectbox("Task to Edit", list_of_task)

        selected_result = get_tasks(selected_task)
        st.write(selected_result)

        if selected_result:
            task = selected_result[0][0]
            task_status = selected_result[0][1]
            task_due_date = selected_result[0][2]

            # Layout
            col1, col2 = st.beta_columns(2)

            with col1:
                new_task = st.text_area("Task To Do", task)

            with col2:
                new_task_status = st.selectbox(task_status, ["ToDo", "Doing"])
                new_task_due_date = st.date_input(task_due_date)

            if st.button("Update Task"):
                edit_task_data(new_task, new_task_status, new_task_due_date,
                               task, task_status, task_due_date)

                st.success("Successfully Updated Data: {0} To {1}".format(task, new_task))

        result2 = view_all_data()

        df2 = pd.DataFrame(result2, columns=["Task", "Status", "Due Date"])

        with st.beta_expander("Updated Data"):
            st.dataframe(df2)

    elif choice == 'Delete':
        st.subheader("Delete Item")
        result = view_all_data()

        df = pd.DataFrame(result, columns=["Task", "Status", "Due Date"])

        with st.beta_expander("Current Data"):
            st.dataframe(df)

        list_of_task = [i[0] for i in view_unique_column()]
        selected_task = st.selectbox("Task to Edit", list_of_task)
        st.warning(f"Do you want to delete {selected_task}?")

        if st.button("Delete Task"):
            selected_result = delete_data(selected_task)
            st.success("Task has been Successfully Deleted")

        result3 = view_all_data()

        df3 = pd.DataFrame(result3, columns=["Task", "Status", "Due Date"])

        with st.beta_expander("Updated After Deleting Data"):
            st.dataframe(df3)

    else:
        st.subheader("About")


if __name__ == '__main__':
    main()
