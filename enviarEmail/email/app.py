import smtplib
from email.message import EmailMessage
import mimetypes
import os
import zipfile
from pathlib import Path

# seu email
remetente = "aladin@gmail.com"
#email dos destinatários
destinatario = "princesa@gmail.com"
# Assunto que será abordado
assunto = "IMAGENS"
# link para gerar a senha https://myaccount.google.com/apppasswords
# Gere uma senha do google e insira a senha gerada no google app abaixo 16 dígitos
senha = 'uklw tqqq vbzy tuho'


# Diretório onde estão as fotos
diretorio_fotos = r"C:\Aula1\enviarEmail\ImagensF"


# Função para comprimir múltiplos arquivos em ZIP
def comprimir_arquivos(lista_arquivos, nome_zip="fotos.zip"):
    with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for arquivo in lista_arquivos:
            zipf.write(arquivo, os.path.basename(arquivo))
    return nome_zip


# Função para obter lista de arquivos de imagem do diretório
def obter_arquivos_imagem(diretorio):
    extensoes = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    arquivos = []

    if not os.path.exists(diretorio):
        print(f"Erro: Diretório {diretorio} não encontrado!")
        return []

    if not os.path.isdir(diretorio):
        print(f"Erro: {diretorio} não é um diretório!")
        return []

    # Listar todos os arquivos do diretório
    for arquivo in os.listdir(diretorio):
        caminho_completo = os.path.join(diretorio, arquivo)
        if os.path.isfile(caminho_completo):
            extensao = os.path.splitext(arquivo)[1].lower()
            if extensao in extensoes:
                arquivos.append(caminho_completo)

    return arquivos


# Obter lista de fotos
fotos = obter_arquivos_imagem(diretorio_fotos)

if not fotos:
    print("Nenhuma foto encontrada no diretório!")
    exit()

print(f"Encontradas {len(fotos)} fotos para anexar:")

# Calcular tamanho total
tamanho_total = sum(os.path.getsize(foto) for foto in fotos)
comprimir = tamanho_total > 20 * 1024 * 1024  # 20MB

msg = EmailMessage()
msg['From'] = remetente
msg['To'] = destinatario
msg['Subject'] = assunto

# Preparar mensagem
if comprimir:
    print("Tamanho total muito grande, comprimindo arquivos...")
    arquivo_zip = comprimir_arquivos(fotos)
    mensagem = f"""
    Olá, aqui estão as fotos solicitadas

    Total de fotos: {len(fotos)}
    Tamanho original: {tamanho_total / 1024 / 1024:.2f} MB
    Tamanho comprimido: {os.path.getsize(arquivo_zip) / 1024 / 1024:.2f} MB

    Att,Lc
    """
    anexos = [arquivo_zip]
else:
    mensagem = f"""
    Olá, aqui estão as {len(fotos)} fotos solicitadas

    Att,Lc
    """
    anexos = fotos

msg.set_content(mensagem)

# Anexar arquivos
for anexo in anexos:
    try:
        mime_type, _ = mimetypes.guess_type(anexo)
        if mime_type is None:
            mime_type = 'application'
            mime_subtype = 'octet-stream'
        else:
            mime_type, mime_subtype = mime_type.split('/', 1)

        with open(anexo, 'rb') as arquivo:
            file_data = arquivo.read()
            nome_arquivo = os.path.basename(anexo)

            msg.add_attachment(file_data,
                               maintype=mime_type,
                               subtype=mime_subtype,
                               filename=nome_arquivo)

        print(f"Anexado: {nome_arquivo}")

    except Exception as e:
        print(f"Erro ao anexar {anexo}: {e}")

# Enviar email
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as email:
        email.login(remetente, senha)
        email.send_message(msg)

    print('E-mail foi enviado com sucesso!')

    # Limpar arquivo ZIP temporário se foi criado
    if comprimir and os.path.exists(arquivo_zip):
        os.remove(arquivo_zip)
        print("Arquivo ZIP temporário removido")

except Exception as e:
    print(f'Erro ao enviar e-mail: {e}')