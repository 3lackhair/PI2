import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Orcamento
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Função auxiliar para verificar a extensão do arquivo
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orcamentos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'  # Importante para mensagens flash

# Inicializa o banco de dados
db.init_app(app)

# Cria as tabelas do banco de dados
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/enviar_orcamento', methods=['POST'])
def enviar_orcamento():
    if request.method == 'POST':
        try:
            novo_orcamento = Orcamento(
                nome=request.form['nome'],
                email=request.form['email'],
                telefone=request.form['telefone'],
                rua=request.form['rua'],
                numero=request.form['numero'],
                complemento=request.form['complemento'],
                bairro=request.form['bairro'],
                cidade=request.form['cidade'],
                uf=request.form['uf'],
                cep=request.form['cep'],
                produto=request.form['produto'],
                tipo_produto=request.form.get('tipo_caneca') or request.form.get('tipo_caderno'),
                cor=request.form.get('cor_caneca'),
                quantidade_paginas=request.form.get('quantidade_de_paginas'),
                quantidade=request.form['quantidade'],
                estampa=request.form['estampa'],
                observacoes=request.form['obs']
            )

            db.session.add(novo_orcamento)
            db.session.commit()
            flash('Orçamento enviado com sucesso!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            flash('Erro ao enviar orçamento. Por favor, tente novamente.', 'error')
            return redirect(url_for('index'))


@app.route('/autenticar-adm', methods=['POST'])
def autenticar_admin():
    # 1. Recebe os dados dos campos 'username' e 'password' do formulário
    usuario_digitado = request.form.get('username')
    senha_digitada = request.form.get('password')

    # 2. Defina o usuário e senha fixos (Apenas para teste!)
    USUARIO_CORRETO = "admin_micheli"
    SENHA_CORRETA = "senha123"

    # 3. Lógica de Verificação
    if usuario_digitado == USUARIO_CORRETO and senha_digitada == SENHA_CORRETA:
        # Sucesso: Se for válido, redireciona para um painel
        flash('Login de Administrador bem-sucedido!', 'success')
        return redirect(url_for('painel_admin'))  # Você precisa criar essa rota!
    else:
        # Falha: Informa o erro e redireciona de volta para o login
        flash('Usuário ou senha inválidos.', 'error')
        return redirect(url_for('login_admin'))  # Rota que mostra o formulário


# A rota 'painel_admin' é o que o usuário vê após o login. Você deve criá-la:
@app.route('/painel-admin')
def painel_admin():
    # *************************************************************
    # FUTURO: Em um projeto real, você PRECISA verificar aqui se o
    # usuário está logado antes de renderizar esta página.
    # Por enquanto, renderizamos diretamente para testar o redirecionamento.
    # *************************************************************

    return render_template('painel_admin.html')


# Rota simples para fazer o logout (você pode aprimorar isso depois)
@app.route('/logout')
def logout_admin():
    # *************************************************************
    # FUTURO: Aqui você limpará a sessão do usuário logado.
    # Por enquanto, apenas redireciona para a home.
    # *************************************************************
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('index'))


# ... (suas rotas home, login_admin, painel_admin, etc.)

@app.route('/upload-imagem', methods=['POST'])
def upload_imagem():
    # 1. Verificar se o formulário tem a parte do arquivo
    if 'new_file' not in request.files:
        flash('Nenhum arquivo selecionado.', 'error')
        return redirect(url_for('painel_admin'))

    file = request.files['new_file']
    target_filename = request.form.get('target_file')  # Pega o nome do arquivo que será substituído

    # 2. Verificar se um nome alvo foi selecionado
    if not target_filename:
        flash('Nenhum arquivo alvo selecionado.', 'error')
        return redirect(url_for('painel_admin'))

    # 3. Processar o upload
    if file and allowed_file(file.filename):

        # Usamos o nome do arquivo ALVO como o nome seguro para salvar
        filename = secure_filename(target_filename)

        # Salva o NOVO arquivo com o NOME DO ARQUIVO ANTIGO, substituindo-o
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        flash(f'A imagem "{target_filename}" foi substituída com sucesso!', 'success')

    else:
        flash('Tipo de arquivo não permitido.', 'error')

    return redirect(url_for('painel_admin'))


if __name__ == '__main__':
    app.run(debug=True)