from django.http import JsonResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.mail import send_mail
from django.template import RequestContext

def PagContato(request):
    if request.method == "POST":
        mensagem_nome = request.POST['mensagem-nome']
        mensagem_email = request.POST['mensagem-email']
        mensagem = request.POST['mensagem']

        # enviar email
        send_mail(
            mensagem_nome, #assunto
            mensagem, #mensagem
            mensagem_email, #Do email - remetente
            ['alfa_bar@hotmail.com'], #Para - destinatario
        )
        return render(request,'contato.html', {'mensagem_nome': mensagem_nome})

    else:
        return render(request, 'contato.html', {})
