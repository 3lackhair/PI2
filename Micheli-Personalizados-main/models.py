from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Orcamento(db.Model):
    __tablename__ = 'orcamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    
    # Endereço
    rua = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    
    # Detalhes do Produto
    produto = db.Column(db.String(50), nullable=False)
    tipo_produto = db.Column(db.String(50))
    cor = db.Column(db.String(50))
    quantidade_paginas = db.Column(db.Integer)
    quantidade = db.Column(db.Integer, nullable=False)
    estampa = db.Column(db.String(200))
    observacoes = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Orcamento, self).__init__(**kwargs)