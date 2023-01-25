from django.shortcuts import render, redirect
from accounts.models import Post, Categoria, Usuario, Comentario
from accounts.views import login
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.utils import timezone
from django.http import FileResponse
import io


# Create your views here.
def post(request):
    usuario_id = request.session['usuario_id']
    usuario_name = request.session['usuario_name']
    usuario_tipo = request.session['usuario_tipo']
    
    post = Post.objects.order_by('-date_create')
    
    paginator = Paginator(post,10)

    page_number = request.GET.get('page')
    post = paginator.get_page(page_number)
    
    return render(request, 'post/post.html',{
        'posts': post,
        'usuario_id':usuario_id,
        'usuario_name':usuario_name,
        'usuario_tipo':usuario_tipo,
    })

def view_post(request,post_id):
    post = Post.objects.get(id=post_id)
    comentarios = Comentario.objects.all()
    
    usuario_id = request.session['usuario_id']
    usuario_tipo = request.session['usuario_tipo']

    if request.method == 'POST':
        usuario = Usuario.objects.get(id=usuario_id)
        comentario = request.POST.get('comentario')
        
        if not comentario:
            messages.add_message(request, messages.ERROR, 'Você precisa ter um comentário para conseguir comentar.')
            return render(request, 'post/view_post.html',{
                'post': post,
                'comentarios':comentarios,
                'usuario_id':usuario_id,
                'usuario_tipo':usuario_tipo,
            })

        comentario_save = Comentario(comentario=comentario,usuario=usuario,post=post)
        comentario_save.save()

    return render(request, 'post/view_post.html',{
        'post': post,
        'comentarios':comentarios,
        'usuario_id':usuario_id,
        'usuario_tipo':usuario_tipo,
    })


def post_create(request):
    categorias = Categoria.objects.all()

    usuario_id = request.session['usuario_id']
    usuario_name = request.session['usuario_name']
    usuario_tipo = request.session['usuario_tipo']

    categoria_name = request.POST.get('categoria')
    titulo = request.POST.get('titulo')
    publicacao = request.POST.get('publicacao')
    
    if usuario_tipo != 'AU':
        return redirect('post')
    
    try:
        if request.method == 'POST':
            if not categoria_name or not titulo or not publicacao:
                messages.add_message(request, messages.ERROR, 'Todos os campos precisam ser preenchidos.')
                return redirect('post_create')

            categoria = Categoria.objects.filter(nome_categoria=categoria_name).first()
            autor = Usuario.objects.filter(id=usuario_id).first()
            post = Post(categoria=categoria,autor=autor,titulo=titulo,publicacao=publicacao)
            post.save()
            messages.add_message(request, messages.SUCCESS, 'Publicação criada com sucesso!')
            return redirect('post')
    except:
        return redirect('post')
    
    return render(request, 'post/post_create.html',{
        'categorias': categorias,
        'usuario_name': usuario_name,
        'usuario_id': usuario_id,
    })

def post_update(request,post_id):
    id_post = Post.objects.filter(id=post_id).first()
    categorias = Categoria.objects.all()

    usuario_tipo = request.session['usuario_tipo']
    usuario_id = request.session['usuario_id']

    if usuario_tipo != 'AU':
        return redirect('post')
    
    if request.method == 'POST':
        try:
            categoria_name = request.POST.get('categoria')
            categoria = Categoria.objects.filter(nome_categoria=categoria_name).first()

            id_post.categoria = categoria
            id_post.titulo = request.POST.get('titulo')
            id_post.publicacao = request.POST.get('publicacao')
            id_post.save(update_fields=['categoria','titulo','publicacao'])
            messages.add_message(request, messages.SUCCESS, 'Publicação atualizada com sucesso!')
            return redirect('post')
        except:
            messages.add_message(request, messages.ERROR, 'Ops, algo deu errado.')
            return redirect('post')

    return render(request, 'post/post_update.html',{
        'id_post':id_post,
        'categorias':categorias,
        'usuario_id':usuario_id,
    })

def post_delete(request,post_id):
    usuario_tipo = request.session['usuario_tipo']

    if usuario_tipo != 'AU':
        return redirect('post')

    try:
        id_post = Post.objects.get(id=post_id)
        id_post.delete()
        messages.add_message(request, messages.SUCCESS, 'Publicação deletada com sucesso!')
        return redirect('post')
    except:
        messages.add_message(request, messages.ERROR, 'Não foi possível excluir essa publicação.')
        return redirect('post')


def post_verified(request, post_id):
    post = Post.objects.all()
    id_post = Post.objects.get(id=post_id)

    usuario_tipo = request.session['usuario_tipo']
    usuario_id = request.session['usuario_id']
    
    return render(request, 'post/post_verified.html',{
        'id_post':id_post,
        'posts':post,
        'usuario_tipo':usuario_tipo,
        'usuario_id':usuario_id,
    })

def search(request):
    usuario_id = request.session['usuario_id']
    usuario_tipo = request.session['usuario_tipo']
    termo = request.GET.get('termo')

    if not termo:
        messages.add_message(request, messages.ERROR, 'O campo de pesquisa não pode ser vazio.')
        return redirect('post')
        
    posts = Post.objects.order_by('-date_create').filter(Q(titulo__icontains=termo))
    
    if not posts:
        messages.add_message(request, messages.ERROR, 'Não contém nenhuma publicação com este titulo.')
        return redirect('post')

    return render(request, 'post/search.html',{
        'posts':posts,
        'usuario_id':usuario_id,
        'usuario_tipo':usuario_tipo,
    })


def drawTitulo(pdf,x=210, y=800):
    pdf.drawString( x, y, 'Relatório de publicações')
    data_gerado(pdf)
    return x,y


def data_gerado(pdf):
    data_gerado = timezone.now()
    
    pdf.setFontSize(8)
    pdf.drawString( 455, 800, f'Gerado em: {data_gerado.astimezone().strftime("%d / %m / %y ás %H:%M:%S")}')


def reserva_linha(pdf,linha):
    linha -= 20
    if linha <= 10:
        linha = 745
        pdf.showPage()
        drawTitulo(pdf)
        
    return linha

def relatorio(request):
    usuario_tipo = request.session['usuario_tipo']

    if usuario_tipo != 'AD':
        return redirect('post')

    posts = Post.objects.all()
    gera_pdf = io.BytesIO()

    pdf = canvas.Canvas(gera_pdf, pagesize=A4)
    drawTitulo(pdf)
    
    linha = 770
    for post in posts:
        linha = reserva_linha(pdf,linha)
        pdf.drawString(20, linha, 'Autor:')
        pdf.drawString(80, linha, f'{post.autor}')
        linha = reserva_linha(pdf,linha)

        pdf.drawString(20, linha, 'Titulo:')
        pdf.drawString(80, linha, f'{post.titulo}')
        linha = reserva_linha(pdf,linha)
        
        pdf.drawString(20, linha, 'Categoria:')
        pdf.drawString(80, linha, f'{post.categoria}')
        linha = reserva_linha(pdf,linha)
        
        pdf.drawString(20, linha, 'Data:')
        pdf.drawString(80, linha, f'{post.date_create.astimezone().strftime("%d / %m / %y  %H:%M:%S")}')
        linha = reserva_linha(pdf,linha)
        
        pdf.drawString(20, linha, 'Publicação:')

        x = 80
        if len(post.publicacao) > 130:
            gen_linhas = generator_linhas(post.publicacao)
            linha_publicacao = next(gen_linhas)
            pdf.drawString(x, linha, linha_publicacao)

            for linha_publicacao in gen_linhas:
                linha = reserva_linha(pdf,linha)
                pdf.drawString(x, linha, linha_publicacao)
      
        else:
            pdf.drawString(80, linha, f'{post.publicacao}')
        
        linha = reserva_linha(pdf,linha)

    pdf.save()
    gera_pdf.seek(0)
    return FileResponse(gera_pdf, as_attachment=True, filename='relatorio.pdf')


def generator_linhas(string,comp_maximo=137):
    generator_de_palavras = (
        palavra_formatada
        for palavra in string.split(' ')
        for palavra_formatada in generator_palavras(palavra, comp_maximo)
            
    )
    comp_total = len(string)

    i = 0
    while comp_total >= 0 and i < 10:
        nova_lista = []
        comp_linha = 0
        # print(comp_total,comp_linha,i)
        for palavra in generator_de_palavras:
            
            if (len(palavra) + 1 + comp_linha) > comp_maximo:
                if comp_linha:
                    break

                if len(palavra) == comp_maximo:
                    nova_lista = [palavra]
                    comp_linha += len(palavra)
                    break
                
                break
            comp_linha += 1 + len(palavra)
            nova_lista.append(palavra)
        comp_total -= comp_linha
        yield ' '.join(nova_lista)
        # print(comp_total,comp_linha,i)
        i += 1
        
def generator_palavras(string,comp_maximo=137):
    for palavra in string.split(' '):
        if len(palavra) <= comp_maximo:
            yield palavra
            continue
        
    try:
        parte_palavra = ''
        generator_index_linha_da_palavra = (
            enumerate(range(comp_maximo -1, len(palavra), comp_maximo))
        )
        i,x = next(generator_index_linha_da_palavra)
        parte_palavra = palavra[i*comp_maximo:((i+1) * comp_maximo)]

        while True:
            i,x = next(generator_index_linha_da_palavra)
            yield parte_palavra
            parte_palavra = palavra[i*comp_maximo:((i+1) * comp_maximo)]
    except:
        yield parte_palavra
