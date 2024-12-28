import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI rendering

from blog.models import Article, Category, ApiEndpoint
import pandas as pd
import matplotlib.pyplot as plt
from django.http import HttpResponse, JsonResponse
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from django.shortcuts import render, get_object_or_404
import requests
from django.conf import settings
import json
import random
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def index(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    if category_id:
        category = Category.objects.get(id=category_id)
        articles = Article.objects.filter(category=category)
    else:
        articles = Article.objects.all()
    return render(request, 'blog/index.html', {'articles': articles, 'categories': categories, 'category_id': category_id})

def check_row_and_years(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        start_year = int(request.POST.get('start_year'))
        end_year = int(request.POST.get('end_year'))
        article_id = request.POST.get('article_id')

        if not text or not start_year or not end_year or not article_id:
            return JsonResponse({'error': 'Missing required parameters'}, status=400)

        article = get_object_or_404(Article, id=article_id)
        if not article.excel_file:
            return JsonResponse({'error': 'No Excel file associated with this article'}, status=400)

        file_path = article.excel_file.file.path

        df = read_and_process_excel(file_path)
        if text in df.index:
            years = df.columns.astype(int)
            if any(year in range(start_year, end_year + 1) for year in years):
                return JsonResponse({'error': 'Year range includes years from the data'}, status=400)
            else:
                # Create JSON request for Azure endpoint
                input_data = {
                    "Inputs": {
                        "input1": [
                            {"Typ": text, "rok": year} for year in range(start_year, end_year + 1)
                        ]
                    },
                    "GlobalParameters": {}
                }

                # Retrieve the API URL and hashed API key from the database
                api_endpoint = get_object_or_404(ApiEndpoint, article=article)
                azure_endpoint_url = api_endpoint.url
                api_key = api_endpoint.api_key  # Retrieve the hashed API key from the database

                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}'
                }

                response = requests.post(azure_endpoint_url, json=input_data, headers=headers)

                if response.status_code == 200:
                    response_data = response.json()
                    results = response_data['Results']['WebServiceOutput0']

                    # Extract values for the plot and randomize the Scored Labels
                    x_values = [result['rok'] for result in results]
                    y_values = [result['Scored Labels'] * random.uniform(0.85, 1.05) for result in results]
                    plot_title = results[0]['Typ']

                    # Generate the plot
                    fig, ax = plt.subplots()
                    ax.plot(x_values, y_values)
                    ax.set_title(plot_title)
                    ax.set_xlabel('Year')
                    ax.set_ylabel('Scored Labels')

                    # Set x-axis ticks to the exact years
                    ax.set_xticks(x_values)
                    ax.set_xticklabels([str(year) for year in x_values])

                    # Tilt x-axis labels
                    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

                    # Format y-axis labels to remove decimal values
                    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

                    # Adjust layout to include all text
                    plt.tight_layout()

                    # Save the plot to a BytesIO object
                    buf = BytesIO()
                    canvas = FigureCanvas(fig)
                    canvas.print_png(buf)
                    buf.seek(0)

                    # Save the plot as an image in the media folder

                    # Define the file path and name
                    file_name = f'plot_{article_id}_{text}_{start_year}_{end_year}.png'
                    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

                    # Save the image to the media folder
                    with default_storage.open(file_path, 'wb') as f:
                        f.write(buf.getvalue())

                    # Store the file path in the session
                    if 'generated_files' not in request.session:
                        request.session['generated_files'] = []
                    request.session['generated_files'].append(file_path)
                    request.session.modified = True

                   # Return the file URL as JSON
                    file_url = default_storage.url(file_name)
                    return JsonResponse({'file_url': file_url})
                else:
                    return JsonResponse({'error': 'Request failed', 'status_code': response.status_code, 'response': response.text}, status=response.status_code)
        else:
            return JsonResponse({'error': 'Text not found in the data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def read_and_process_excel(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No such file or directory: '{file_path}'")
    
    df = pd.read_excel(file_path, engine='openpyxl')
    df = df.replace('.', "")  # Replace '.' with 0
    df.set_index(df.columns[0], inplace=True)  # Set the first column as the index
    return df

def article(request, id):
    article = get_object_or_404(Article, id=id)
    categories = Category.objects.all()
    selected_row = request.GET.get('row')

    if article.excel_file:
        excel_file = article.excel_file
        file_path = excel_file.file.path
        if file_path.endswith(('.xlsx', '.xls')):
            df = read_and_process_excel(file_path)
            rows = df.index.tolist()
            if selected_row and selected_row in rows:
                data = df.loc[selected_row]
            elif rows:
                selected_row = rows[0]
                data = df.loc[selected_row]
            else:
                data = []
        else:
            rows = []
            data = []
    else:
        rows = []
        data = []

    context = {
        'article': article,
        'categories': categories,
        'rows': rows,
        'selected_row': selected_row,
        'data': data,
    }
    return render(request, 'blog/article.html', context)

def plot_graph(request, id):
    article = get_object_or_404(Article, id=id)
    selected_row = request.GET.get('row')

    if article.excel_file and selected_row:
        excel_file = article.excel_file
        file_path = excel_file.file.path
        if file_path.endswith(('.xlsx', '.xls')):
            df = read_and_process_excel(file_path)
            if selected_row in df.index:
                data = df.loc[selected_row]
                print(f"Plotting data for row: {selected_row}")
                print(data.head())

                fig, ax = plt.subplots()
                # Check if the first row contains numeric values
                if pd.to_numeric(data.index, errors='coerce').notnull().all():
                    data.plot(ax=ax)  # Use line plot if all values are numeric                 
                else:
                    data.plot(kind='bar', ax=ax)  # Use bar chart if any value is non-numeric

                #TODO: Put variables instead of hard-coded values depending on the table
                ax.set_title(f'Row {selected_row} Data')
                ax.set_xlabel('Column')
                ax.set_ylabel('Value')

                # Add labels from the DataFrame
                ax.set_xticks(range(len(data)))
                ax.set_xticklabels(data.index, rotation=45, ha='right')

                 # Adjust layout to include all text
                plt.tight_layout()

                canvas = FigureCanvas(fig)
                response = HttpResponse(content_type='image/png')
                canvas.print_png(response)
                return response
            else:
                print(f"Row {selected_row} not found in the DataFrame")
    return HttpResponse(status=400)

def category(request, id):
    category = Category.objects.get(id=id)
    articles = Article.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'blog/article_list.html', context = {'category': category, 'articles': articles, 'categories': categories})

