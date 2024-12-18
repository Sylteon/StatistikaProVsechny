import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI rendering

from django.shortcuts import render, get_object_or_404
from blog.models import Article, Category, ExcelFile
import pandas as pd
import matplotlib.pyplot as plt
from django.http import HttpResponse
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def index(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    if category_id:
        category = Category.objects.get(id=category_id)
        articles = Article.objects.filter(category=category)
    else:
        articles = Article.objects.all()
    return render(request, 'blog/index.html', {'articles': articles, 'categories': categories, 'category_id': category_id})

def read_and_process_excel(file_path):
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
                data.plot(ax=ax)  # Use line plot for better visualization

                #TODO: Put variables instead of hard-coded values depending on the table
                ax.set_title(f'Row {selected_row} Data')
                ax.set_xlabel('Column')
                ax.set_ylabel('Value')

                # Add labels from the DataFrame
                ax.set_xticks(range(len(data)))
                ax.set_xticklabels(data.index, rotation=45, ha='right')

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

