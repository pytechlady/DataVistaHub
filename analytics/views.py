# views.py
from django.shortcuts import render
from plotly.offline import plot
from .forms import DataForm, FormSubmit
import plotly.express as px
from .utils import Util
import pandas as pd
from django.http import JsonResponse

# import pdb; 

# pdb.set_trace()

def index(request):
    return render(request, 'analytics/index.html')
    
def plot_scatter_plot(request, form, df):
    try:
        if form.is_valid():
            x = form.cleaned_data['set_x']
            y = form.cleaned_data['set_y']
            title = form.cleaned_data['title']

            fig = px.scatter(df, x=x, y=y, title=title)
            scatter_plot = plot(fig, output_type="div")

            context = {"plot_div": scatter_plot}
            # print(context.title.text)
            return render(request, "analytics/graphs.html", context)
        else:
            print("Form is not valid")

        return render(request, "analytics/upload.html", {"form": form})
    except Exception as e:
        return render(request, "analytics/upload.html", {"error": e})

def plot_interactive_graphs(request, form ,df):
    try:
        if form.is_valid():
            x = form.cleaned_data['x_axis']
            title = form.cleaned_data['title']
            fig = px.line(title=title)
            norm_plot = Util.normalize(df, x)
            interactive_graph = Util.interactive_plot(norm_plot, x, fig)
            output_graph = plot(interactive_graph, output_type="div")
            context = {"plot_div": output_graph}
            return render(request, "analytics/graphs.html", context)
        else:
            print("Form is not valid")
            
        return render(request, "analytics/submit-form.html", {"form": form})
    except Exception as e:
        return render(request, "analytics/submit-form.html", {"error": e})

def plot_daily_returns(request, form ,df):
    try:
        if form.is_valid():
            x = form.cleaned_data['x_axis']
            title = form.cleaned_data['title']
            fig = px.line(title=title)
            resp = Util.daily_return(df, x)
            interactive_graph = Util.interactive_plot(resp, x, fig)
            output_graph = plot(interactive_graph, output_type="div")
            context = {"plot_div": output_graph}
            return render(request, "analytics/graphs.html", context)
        else:
            print("Form is not valid")
            
        return render(request, "analytics/daily-returns.html", {"form": form})
    except Exception as e:
        return render(request, "analytics/daily-returns.html", {"error": e})
        
def upload(request):
    form = DataForm()

    if request.method == 'POST':
        form = DataForm(request.POST, request.FILES)
        df = None

        if form.is_valid():
            df = Util.read_dataset(form.cleaned_data['data_set'])
            column_choices = [(col, col) for col in df.columns]
            form.fields['set_x'].widget.choices = column_choices
            form.fields['set_y'].widget.choices = column_choices

            # Print selected values for debugging
            print(f"Selected set_x value: {form.cleaned_data['set_x']}")
            print(f"Selected set_y value: {form.cleaned_data['set_y']}")

            # Validate form again after setting choices
            if form.is_valid():
                print("Form is valid. Proceeding to plot_scatter_plot.")
                return plot_scatter_plot(request, form, df)
            else:
                print("Form is not valid after updating choices.")
                print(form.errors)
        else:
            print("Form errors after initial validation:")
            print(form.errors)

    return render(request, "analytics/upload.html", {"form": form})

def upload_form(request):
    form = FormSubmit()

    if request.method == 'POST':
        form = FormSubmit(request.POST, request.FILES)
        df = None

        if form.is_valid():
            df = Util.read_dataset(form.cleaned_data['data_set'])
            column_choices = [(col, col) for col in df.columns]
            form.fields['x_axis'].widget.choices = column_choices

            # Print selected values for debugging
            print(f"Selected x_axis value: {form.cleaned_data['x_axis']}")

            # Validate form again after setting choices
            if form.is_valid():
                print("Form is valid. Proceeding to plot_interactive_plot.")
                return plot_interactive_graphs(request, form, df)
            else:
                print("Form is not valid after updating choices.")
                print(form.errors)
        else:
            print("Form errors after initial validation:")
            print(form.errors)

    return render(request, "analytics/submit-form.html", {"form": form})

def daily_return(request):
    form = FormSubmit()

    if request.method == 'POST':
        form = FormSubmit(request.POST, request.FILES)
        df = None

        if form.is_valid():
            df = Util.read_dataset(form.cleaned_data['data_set'])
            column_choices = [(col, col) for col in df.columns]
            form.fields['x_axis'].widget.choices = column_choices

            # Print selected values for debugging
            print(f"Selected x_axis value: {form.cleaned_data['x_axis']}")

            # Validate form again after setting choices
            if form.is_valid():
                print("Form is valid. Proceeding to plot_interactive_plot.")
                return plot_daily_returns(request, form, df)
            else:
                print("Form is not valid after updating choices.")
                print(form.errors)
        else:
            print("Form errors after initial validation:")
            print(form.errors)

    return render(request, "analytics/daily-returns.html", {"form": form})

def get_column_names(request):
    if request.method == 'POST' and request.FILES.get('data_set'):
        data_set = request.FILES['data_set']
        print("Received file:", data_set)
        
        try:
            df = Util.read_dataset(data_set)
            column_names = list(df.columns)
            print("Column names:", column_names)
            return JsonResponse(column_names, safe=False)
        except Exception as e:
            print("Error reading CSV:", str(e))
            return JsonResponse([], safe=False)

    return JsonResponse([], safe=False)

