from django.shortcuts import render
from blog.models import Article, Category
import pandas as pd
import matplotlib.pyplot as plt
from django.conf import settings
from io import BytesIO
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from blog.models import CSVFile
# Create your views here.

def index(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    if category_id:
        category = Category.objects.get(id=category_id)
        articles = Article.objects.filter(category=category)
    else:
        articles = Article.objects.all()
    return render(request, 'blog/index.html', {'articles': articles, 'categories': categories, 'category_id': category_id})

def article(request, id):
    article = Article.objects.get(id=id)
    categories = Category.objects.all()
    csv_files = CSVFile.objects.all()
    selected_file = request.GET.get('file')
    selected_column = request.GET.get('column')

    if selected_file:
        csv_file = CSVFile.objects.get(id=selected_file)
        df = pd.read_csv(csv_file.file.path)
        columns = df.columns
        if selected_column:
            data = df[selected_column]
        else:
            data = df[columns[0]]
    else:
        columns = []
        data = []

    context = {
        'article': article,
        'categories': categories,
        'csv_files': csv_files,
        'columns': columns,
        'selected_file': selected_file,
        'selected_column': selected_column,
        'data': data,
    }
    return render(request, 'blog/article.html', context)

def plot_graph(request):
    selected_file = request.GET.get('file')
    selected_column = request.GET.get('column')

    if selected_file and selected_column:
        csv_file = CSVFile.objects.get(id=selected_file)
        df = pd.read_csv(csv_file.file.path)
        data = df[selected_column]

        fig, ax = plt.subplots()
        data.plot(ax=ax)
        ax.set_title(f'{selected_column} Data')
        ax.set_xlabel('Index')
        ax.set_ylabel(selected_column)

        canvas = FigureCanvas(fig)
        response = HttpResponse(content_type='image/png')
        canvas.print_png(response)
        return response
    else:
        return HttpResponse(status=400)

def category(request, id):
    category = Category.objects.get(id=id)
    articles = Article.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'blog/article_list.html', context = {'category': category, 'articles': articles, 'categories': categories})

