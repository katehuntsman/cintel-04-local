import plotly.express as px
from palmerpenguins import load_penguins
from shiny.express import input, ui, render
from shiny import reactive
from shinywidgets import render_widget, render_plotly
import seaborn as sns

penguins = load_penguins()

ui.page_opts(title="Penguins Data - Kate Huntsman", fillable=True)

# ADD A SIDEBAR
with ui.sidebar(
    position="right", bg="#f8f8f8", open="open"
): 
    ui.h2("Sidebar") # sidebar header
    # Dropdown menu 
    ui.input_selectize(
        "selected_attribute",
        "Selected Attribute",
        choices=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )

    # Numeric input for Plotly histogram
    ui.input_numeric("plotly_bin_count", "Bin Count (Plotly)", 1, min=1, max=10)

    # Slider input for Seaborn
    ui.input_slider(
        "seaborn_bin_count", "Bin Count (Seaborn)", 5, 50, 25
    )

    # Checkbox to filter species
    ui.input_checkbox_group(
        "selected_species_list",
        "Select a Species",
        choices=["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo"],
        inline=False,
    )

    # Dividing line
    ui.hr()

    # Hyperlink to GitHub repo
    ui.h5("GitHub Repo")
    ui.a(
        "cintel-02-data",
        href="https://github.com/katehuntsman/cintel-02-data",
        target="_blank",
    )

# Main content layout
with ui.layout_columns():
    # Display the Plotly Histogram
    with ui.card():
        ui.card_header("Plotly Histogram")

        @render_plotly
        def plotly_histogram():
            return px.histogram(
                penguins,
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species",
            )

    # Display Data Table (showing all data)
    with ui.card():
        ui.card_header("Data Table")

        @render.data_frame
        def data_table():
            return render.DataTable(penguins)

    # Display Data Grid (showing all data)
    with ui.card():
        ui.card_header("Data Grid")

        @render.data_frame
        def data_grid():
            return render.DataGrid(penguins)

with ui.layout_columns():
    # Plotly Scatterplot (showing all species)
        with ui.card(full_screen=True):
            ui.card_header("Plotly Scatterplot: Species")
            @render_plotly
            def plotly_scatterplot():
                return px.scatter(
                data_frame=filtered_data(),
                x="body_mass_g",
                y="bill_depth_mm",
                color="species",
                labels={
                    "bill_depth_mm": "Bill Depth (mm)",
                    "body_mass_g": "Body Mass (g)",
                },
            )

    # Seaborn Histogram (showing all species)
        with ui.card():
            ui.card_header("Seaborn Histogram")
            @render.plot
            def plot2():
                ax = sns.histplot(
                    data=filtered_data(),
                    x=input.selected_attribute(),
                    bins=input.seaborn_bin_count(),
            )
                ax.set_title("Palmer Penguins")
                ax.set_xlabel(input.selected_attribute())
                ax.set_ylabel("Number")
                return ax

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

# Reactive function to filter data
@reactive.Calc
def filtered_data():
    selected_species = input.selected_species_list()
    if selected_species:
        return penguins[penguins['species'].isin(selected_species)]
    return penguins  # Return all data if no species are selected
