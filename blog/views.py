from django.shortcuts import render, get_object_or_404
from blog.models import Article, Category, ExcelFile
import pandas as pd
import matplotlib.pyplot as plt
from django.http import HttpResponse
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


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
    article = get_object_or_404(Article, id=id)
    categories = Category.objects.all()
    selected_column = request.GET.get('column')

    if article.excel_file:
        excel_file = article.excel_file
        file_path = excel_file.file.path
        if file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
            columns = df.columns
            if selected_column:
                data = df[selected_column]
            else:
                data = df[columns[0]]
        else:
            columns = []
            data = []
    else:
        columns = []
        data = []

    context = {
        'article': article,
        'categories': categories,
        'columns': columns,
        'selected_column': selected_column,
        'data': data,
    }
    return render(request, 'blog/article.html', context)

def plot_graph(request, id):
    article = get_object_or_404(Article, id=id)
    selected_column = request.GET.get('column')

    if article.excel_file and selected_column:
        excel_file = article.excel_file
        file_path = excel_file.file.path
        if file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
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
    return HttpResponse(status=400)

def category(request, id):
    category = Category.objects.get(id=id)
    articles = Article.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'blog/article_list.html', context = {'category': category, 'articles': articles, 'categories': categories})

