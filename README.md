# EmailSend
É um script em python

📧 Envio de E-mails com Anexos em Python

Este projeto é um script em Python desenvolvido para enviar e-mails automaticamente, anexando arquivos de uma pasta específica.
Além disso, ele permite o envio para múltiplos destinatários simultaneamente, tornando o processo rápido e eficiente.

🚀 Funcionalidades

Envio automático de e-mails via SMTP.

Anexa todos os arquivos de uma pasta específica.

Permite definir múltiplos destinatários.

Personalização do assunto e corpo do e-mail.

Log de envio (opcional).

Compatível com provedores como Gmail, Outlook, Yahoo, etc.

🧩 Pré-requisitos

Antes de rodar o script, é necessário ter:

Python 3.8+ instalado.

As seguintes bibliotecas:

pip install smtplib email os ssl


(As bibliotecas smtplib, email, os e ssl já vêm com o Python padrão.)

Se quiser ler variáveis de ambiente (recomendado para segurança):

pip install python-dotenv

⚙️ Configuração

Crie um arquivo .env (opcional, mas recomendado) e adicione suas credenciais:

EMAIL_USER=seuemail@gmail.com
EMAIL_PASS=sua_senha_ou_app_password


Configure o script Python com:

Caminho da pasta de anexos

Lista de destinatários

Assunto e corpo do e-mail

🧠 Exemplo de Uso
import smtplib
import ssl
from email.message import EmailMessage
import os

# Configurações básicas
EMAIL_REMETENTE = "seuemail@gmail.com"
SENHA = "sua_senha_ou_app_password"
DESTINATARIOS = ["email1@exemplo.com", "email2@exemplo.com"]
ASSUNTO = "Relatórios Automáticos"
CORPO = "Olá! Segue em anexo os relatórios do dia."

PASTA_ANEXOS = "anexos/"  # Caminho da pasta com os arquivos

# Cria o e-mail
msg = EmailMessage()
msg["From"] = EMAIL_REMETENTE
msg["To"] = ", ".join(DESTINATARIOS)
msg["Subject"] = ASSUNTO
msg.set_content(CORPO)

# Adiciona os anexos
for arquivo in os.listdir(PASTA_ANEXOS):
    caminho = os.path.join(PASTA_ANEXOS, arquivo)
    if os.path.isfile(caminho):
        with open(caminho, "rb") as f:
            dados = f.read()
            msg.add_attachment(
                dados,
                maintype="application",
                subtype="octet-stream",
                filename=arquivo
            )

# Envia o e-mail
contexto = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as smtp:
    smtp.login(EMAIL_REMETENTE, SENHA)
    smtp.send_message(msg)

print("✅ E-mail enviado com sucesso!")

📂 Estrutura do Projeto
enviarEmail/
│
├── anexos/                # Pasta com os arquivos a serem enviados
├── .idea                   # (Opcional) Armazena credenciais de e-mail
├── email --> app.py # Script principal
├── pasta.pdf               # arquivo para usar de exemplo para envio
├── ImagensF


├── scriptExemplo.pdf       # mais um arquivo, compactado, com tamanho necessário para o envio
├── + 2 arquivos em bloco de notas como exemplo
└── README.md              # Documentação

🔐 Segurança

Nunca exponha sua senha diretamente no código.

Utilize senhas de aplicativo (disponíveis no Gmail, Outlook, etc.).

Caso use .env, adicione-o ao .gitignore para não subir ao repositório.

🧾 Licença

Este projeto é de uso livre sob a licença MIT.
Sinta-se à vontade para modificar e distribuir conforme suas necessidades.

🤝 Contribuições

Contribuições são bem-vindas!
Sinta-se à vontade para abrir issues e enviar pull requests.
