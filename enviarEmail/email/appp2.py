import smtplib
from email.message import EmailMessage
import pyperclip
import base64
from io import BytesIO
from PIL import Image
import win32clipboard
import time
import os

# seu email
remetente = "aladin@gmail.com"
#email dos destinatários
destinatarios = ["princesa@gmail.com", "sultao@gmail.com", "jasmine@gmail.com"]
# Assunto que será abordado
assunto = "IMAGENS"
# link para gerar a senha https://myaccount.google.com/apppasswords
# Gere uma senha do google e insira a senha gerada no google app abaixo 16 dígitos
senha = 'frfr kiki jiji dedk'


def aguardar_conteudo_clipboard():
    """Aguarda até que algo seja copiado para a área de transferência"""
    print("🖱️  AGUARDANDO CONTEÚDO...")
    print("1. Vá até seu documento/página")
    print("2. Selecione TUDO (Ctrl+A)")
    print("3. Copie (Ctrl+C)")
    print("⏳ Aguardando você copiar...")

    conteudo_anterior = pyperclip.paste()

    # Aguardar até que o conteúdo mude (usuário copiou algo)
    while True:
        time.sleep(1)  # Verificar a cada segundo
        conteudo_atual = pyperclip.paste()

        if conteudo_atual != conteudo_anterior and conteudo_atual.strip():
            print("✅ Conteúdo copiado com sucesso!")
            return conteudo_atual

        conteudo_anterior = conteudo_atual


def obter_imagem_clipboard():
    """Tenta obter imagem da área de transferência"""
    try:
        win32clipboard.OpenClipboard()
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
            data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
            win32clipboard.CloseClipboard()

            # Converter para imagem
            image = Image.open(BytesIO(data))
            return image
        win32clipboard.CloseClipboard()
    except:
        pass
    return None


def criar_email_com_conteudo_copiado():
    """Cria email com conteúdo da área de transferência"""

    # Obter texto
    texto_copiado = aguardar_conteudo_clipboard()

    # Obter imagem (se houver)
    imagem_copiada = obter_imagem_clipboard()

    if not texto_copiado and not imagem_copiada:
        print("❌ Nada foi copiado!")
        return None

    # Criar mensagem HTML
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            .conteudo-copiado {
                white-space: pre-wrap;
                background: #f9f9f9;
                padding: 20px;
                border-radius: 10px;
                border: 1px solid #ddd;
            }
            img {
                max-width: 100%;
                height: auto;
                border-radius: 8px;
                margin: 10px 0;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        <div class="conteudo-copiado">
    """

    # Adicionar texto
    if texto_copiado:
        # Manter formatação original
        texto_html = texto_copiado.replace('\n', '<br>')
        html_content += texto_html

    # Adicionar imagem se existir
    if imagem_copiada:
        try:
            # Converter imagem para base64
            buffered = BytesIO()
            imagem_copiada.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            html_content += f'<br><br><img src="data:image/png;base64,{img_str}" alt="Imagem copiada">'
            print("📸 Imagem incorporada no email!")
        except Exception as e:
            print(f"⚠️ Erro ao processar imagem: {e}")

    html_content += """
        </div>
    </body>
    </html>
    """

    return html_content, texto_copiado


def enviar_emails():
    """Função principal para enviar emails"""

    print("📧 ENVIADOR DE CONTEÚDO COPIADO")
    print("=" * 50)

    # Criar conteúdo do email
    html_content, texto_simples = criar_email_com_conteudo_copiado()

    if not html_content:
        return

    # Enviar para cada destinatário
    for destinatario in destinatarios:
        try:
            msg = EmailMessage()
            msg['From'] = remetente
            msg['To'] = destinatario
            msg['Subject'] = assunto

            # Versão texto simples e HTML
            msg.set_content(texto_simples if texto_simples else "Email com conteúdo copiado")
            msg.add_alternative(html_content, subtype='html')

            # Enviar email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(remetente, senha)
                server.send_message(msg)

            print(f"✅ Email enviado para: {destinatario}")

        except Exception as e:
            print(f"❌ Erro ao enviar para {destinatario}: {e}")


# Verificar e instalar dependências
def instalar_dependencias():
    try:
        import pyperclip
    except ImportError:
        print("Instalando pyperclip...")
        os.system("pip install pyperclip")

    try:
        import win32clipboard
    except ImportError:
        print("Instalando pywin32...")
        os.system("pip install pywin32")

    try:
        from PIL import Image
    except ImportError:
        print("Instalando Pillow...")
        os.system("pip install Pillow")


# Executar
if __name__ == "__main__":
    instalar_dependencias()
    enviar_emails()
    print("\n🎉 Processo concluído!")