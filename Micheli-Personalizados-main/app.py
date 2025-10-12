from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Orcamento
import os

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)