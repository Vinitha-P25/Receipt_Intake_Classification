import streamlit as st
import pandas as pd

from processor import process_pdf


st.set_page_config(
    page_title="Receipt Intake & Classification",
    page_icon="📄",
    layout="wide"
)


st.title("📄 Receipt Intake & Classification")
st.write("Upload PDF receipts and expense documents for automatic processing.")


# 1. Upload multiple PDF documents

uploaded_files = st.file_uploader(
    "Upload PDF documents",
    type=["pdf"],
    accept_multiple_files=True
)


if uploaded_files:

    st.subheader("Processing Documents")

    results = []

    progress_bar = st.progress(0)
    status_message = st.empty()

    total_files = len(uploaded_files)

    # 2. Process each uploaded PDF independently

    for index, uploaded_file in enumerate(uploaded_files):

        status_message.write(
            f"Processing {uploaded_file.name}..."
        )

        if not uploaded_file.name.lower().endswith(".pdf"):

            result = {
                "file": uploaded_file.name,
                "text": "",
                "source": "",
                "document_type": "",
                "category": "",
                "vendor": "",
                "date": "",
                "amount": "",
                "currency": "",
                "reference_number": "",
                "confidence": 0,
                "reason": "",
                "status": "Failed",
                "error": "Only PDF files are supported."
            }

        else:

            result = process_pdf(uploaded_file.getvalue())
            result["file"] = uploaded_file.name

        results.append(result)

        progress_bar.progress(
            (index + 1) / total_files
        )

    status_message.success("All documents processed!")

    # 3. Convert results into DataFrame

    df = pd.DataFrame(results)

    st.divider()

    # 4. Processing Summary

    st.subheader("Processing Summary")

    status_counts = df["status"].value_counts()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Documents", len(df))
    col2.metric("Done", status_counts.get("Done", 0))
    col3.metric("Needs Review", status_counts.get("Needs review", 0))

    col4.metric(
        "Unsupported / Failed",
        status_counts.get("Unsupported", 0)
        + status_counts.get("Failed", 0)
    )

    st.divider()

    # 5. Filter Results

    st.subheader("Document Results")

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        selected_status = st.multiselect(
            "Filter by Status",
            options=sorted(df["status"].dropna().unique()),
            default=sorted(df["status"].dropna().unique())
        )

    with filter_col2:

        selected_category = st.multiselect(
            "Filter by Category",
            options=sorted(df["category"].dropna().unique()),
            default=sorted(df["category"].dropna().unique())
        )

    filtered_df = df[
        df["status"].isin(selected_status)
        & df["category"].isin(selected_category)
    ].copy()

    # Sort Results

    st.subheader("Sort Documents")

    sort_col1, sort_col2 = st.columns(2)

    with sort_col1:

        sort_column = st.selectbox(
            "Sort By",
            [
                "file",
                "vendor",
                "date",
                "amount",
                "category",
                "document_type",
                "status",
                "confidence"
            ]
        )

    with sort_col2:

        sort_order = st.selectbox(
            "Sort Order",
            ["Ascending", "Descending"]
        )

    # Numeric sorting for amount

    if sort_column == "amount":

        filtered_df["__sort_amount"] = pd.to_numeric(
            filtered_df["amount"],
            errors="coerce"
        )

        filtered_df = filtered_df.sort_values(
            by="__sort_amount",
            ascending=(sort_order == "Ascending"),
            na_position="last",
            kind="stable"
        )

        filtered_df = filtered_df.drop(
            columns=["__sort_amount"]
        )

    else:

        filtered_df = filtered_df.sort_values(
            by=sort_column,
            ascending=(sort_order == "Ascending"),
            na_position="last",
            kind="stable"
        )

    filtered_df = filtered_df.reset_index(drop=True)

    display_columns = [
        "file",
        "source",
        "document_type",
        "category",
        "vendor",
        "date",
        "amount",
        "currency",
        "reference_number",
        "confidence",
        "status"
    ]

    # Highlight status with readable text colours

    def highlight_status(row):

        if row["status"] == "Done":
            background = "#d4edda"

        elif row["status"] == "Needs review":
            background = "#fff3cd"

        elif row["status"] == "Unsupported":
            background = "#e2e3e5"

        else:
            background = "#f8d7da"

        return [
            f"background-color: {background}; color: #212529;"
        ] * len(row)

    styled_df = filtered_df[display_columns].style.apply(
        highlight_status,
        axis=1
    )

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        height=350
    )

    st.divider()

    # 6. Expense Totals by Category and Currency

    st.subheader("Expense Category Totals")

    completed_df = df[
        df["status"] == "Done"
    ].copy()

    if not completed_df.empty:

        completed_df["amount"] = pd.to_numeric(
            completed_df["amount"],
            errors="coerce"
        )

        totals = (
            completed_df
            .groupby(
                ["category", "currency"],
                as_index=False
            )["amount"]
            .sum()
        )

        totals["amount"] = totals["amount"].round(2)

        st.dataframe(
            totals,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No completed expense documents available.")

    st.divider()

    # 7. Individual Document Details

    st.subheader("Document Details")

    selected_file = st.selectbox(
        "Select a document",
        df["file"].tolist()
    )

    selected_result = df[
        df["file"] == selected_file
    ].iloc[0]

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Document Type:**", selected_result["document_type"])
        st.write("**Category:**", selected_result["category"])
        st.write("**Vendor:**", selected_result["vendor"])
        st.write("**Date:**", selected_result["date"])
        st.write("**Amount:**", selected_result["amount"])
        st.write("**Currency:**", selected_result["currency"])

    with col2:

        st.write("**Reference Number:**", selected_result["reference_number"])
        st.write("**Source:**", selected_result["source"])
        st.write("**Confidence:**", selected_result["confidence"])
        st.write("**Status:**", selected_result["status"])
        st.write("**Reason:**", selected_result["reason"])
        st.write("**Error:**", selected_result["error"])

    # Display extracted digital text or OCR output

    with st.expander("View Extracted Text / OCR Output"):

        extracted_text = selected_result.get("text", "")

        if pd.isna(extracted_text) or not extracted_text:
            st.info("No extracted text is available for this document.")

        else:
            st.text_area(
                "Extracted Document Text",
                value=extracted_text,
                height=250,
                disabled=True
            )

    # 8. Export Results to CSV

    st.divider()

    st.subheader("Download Results")

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV Results",
        data=csv_data,
        file_name="receipt_classification_results.csv",
        mime="text/csv"
    )

else:

    st.info("Please upload one or more PDF documents to begin.")