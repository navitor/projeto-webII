# Importa os módulos necessários do Django.
"""from django.db import models  # Ferramentas para criar os modelos (tabelas do banco de dados).
from django.contrib.auth.models import User  # Importa o modelo de Usuário padrão do Django.

# Modelo para Categoria de Produtos
class Categoria(models.Model):  # Define a classe Categoria, que herda de models.Model para se tornar uma tabela no banco.
    # Define os campos (colunas) da tabela Categoria.
    nome = models.CharField("Nome da Categoria", max_length=100, unique=True)  # Campo de texto curto, com no máximo 100 caracteres. 'unique=True' garante que não haja categorias com nomes repetidos.
    descricao = models.TextField("Descrição", blank=True, null=True)  # Campo de texto longo. 'blank=True' e 'null=True' tornam este campo opcional.

    class Meta:  # Classe interna para configurar metadados do modelo.
        verbose_name = "Categoria"  # Nome singular que aparecerá no painel de administração do Django.
        verbose_name_plural = "Categorias"  # Nome plural que aparecerá no painel de administração.
        ordering = ["nome"]  # Define a ordem padrão dos registros como alfabética pelo campo 'nome'.

    def __str__(self):  # Método especial que define como um objeto Categoria será exibido 
        return self.nome  # Retorna o nome da categoria como sua representação em string.

# Modelo para Produto
class Produto(models.Model):  # Define a classe Produto, que será uma tabela no banco de dados.
    nome = models.CharField("Nome do Produto", max_length=150)  # Campo de texto para o nome do produto.
    descricao = models.TextField("Descrição")  # Campo de texto longo para a descrição detalhada do produto.
    preco = models.DecimalField("Preço", max_digits=8, decimal_places=2)  # Campo para números decimais,para preços. 'max_digits' é o total de dígitos e 'decimal_places' são as casas decimais.
    estoque = models.PositiveIntegerField("Estoque", default=0)  # Campo para números inteiros não negativos (a partir de zero), com valor padrão 0.
    imagem = models.ImageField("Imagem", upload_to="produtos/")  # Campo para upload de imagens. As imagens serão salvas na pasta 'media'.
    categoria = models.ForeignKey(  # Define um relacionamento de "chave estrangeira" 
        Categoria,  # O modelo com o qual se relaciona (um Produto pertence a uma Categoria).
        on_delete=models.CASCADE,  # Se uma Categoria for deletada, todos os Produtos nela também serão (efeito cascata).
        related_name="produtos",  # Permite acessar todos os produtos de uma categoria
        verbose_name="Categoria"  # Nome do campo no painel de administração.
    )

    class Meta:  # Metadados do modelo Produto.
        verbose_name = "Produto"  # Nome singular no admin.
        verbose_name_plural = "Produtos"  # Nome plural no admin.
        ordering = ["nome"]  # Ordena os produtos alfabeticamente por nome.

    def __str__(self):  # Define a representação em string de um objeto Produto.
        return f"{self.nome} (R$ {self.preco:.2f})"  # Retorna uma string formatada com nome e preço.

#Modelo para Pedido
class Pedido(models.Model):  # Define a classe Pedido, representando um pedido de um cliente.
    # Define as opções de escolha para o campo 'status'.
    STATUS_CHOICES = [
        ("aguardando", "Aguardando Pagamento"),
        ("pago", "Pago"),
        ("enviado", "Enviado"),
        ("entregue", "Entregue"),
        ("cancelado", "Cancelado"),
    ]

    usuario = models.ForeignKey(  # Relacionamento com o modelo de Usuário do Django.
        User,  # O modelo de usuário.
        on_delete=models.CASCADE,  # Se o usuário for deletado, seus pedidos também serão.
        related_name="pedidos",  # Permite acessar os pedidos de um usuário 
        null=True, blank=True,  # Permite que um pedido exista sem um usuário logado
        verbose_name="Usuário"  # Nome do campo no admin.
    )   

    data_pedido = models.DateTimeField("Data do Pedido", auto_now_add=True)  # Campo de data e hora que é preenchido automaticamente na criação do pedido.
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default="aguardando")  # Campo de texto com opções pré-definidas. O valor padrão é 'aguardando'.
    valor_total = models.DecimalField("Valor Total", max_digits=10, decimal_places=2, default=0)  # Valor total do pedido.

    class Meta:  # Metadados do modelo Pedido.
        verbose_name = "Pedido"  # Nome singular no admin.
        verbose_name_plural = "Pedidos"  # Nome plural no admin.
        ordering = ["-data_pedido"]  # Ordena os pedidos pela data, do mais recente para o mais antigo 

    def __str__(self):  # Define a representação em string de um objeto Pedido.
        usuario_nome = self.usuario.username if self.usuario else "Usuário Anônimo"  # Verifica se há um usuário associado.
        return f"Pedido {self.id} - {usuario_nome} - {self.get_status_display()}"  # Retorna uma string formatada. `get_status_display()` mostra o valor legível das 'choices'.

# Modelo para Item do Pedido 
class ItemPedido(models.Model):  # Tabela que liga Pedidos e Produtos 
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens")  # Chave estrangeira para o Pedido ao qual este item pertence.
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)  # Chave estrangeira para o Produto que foi comprado.
    quantidade = models.PositiveIntegerField("Quantidade", default=1)  # A quantidade de um produto específico neste pedido.
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # Armazena o preço do produto no momento da compra, para evitar problemas se o preço mudar no futuro.

    class Meta:  # Metadados do modelo ItemPedido.
        verbose_name = "Item do Pedido"  # Nome singular no admin.
        verbose_name_plural = "Itens do Pedido"  # Nome plural no admin.

    def __str__(self):  # Define a representação em string de um objeto ItemPedido.
        return f"{self.quantidade}x {self.produto.nome} (Pedido {self.pedido.id})"  
    
#Modelo para Pagamento
class Pagamento(models.Model):  # Define a classe Pagamento, que armazena informações sobre o pagamento de um pedido.
    # Opções para o método de pagamento.
    METODOS = [
        ("cartao", "Cartão de Crédito"),
        ("pix", "PIX"),
        ("boleto", "Boleto"),
    ]
    # Opções para o status do pagamento.
    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("pago", "Pago"),
        ("recusado", "Recusado"),
    ]

    pedido = models.OneToOneField(  # Relacionamento um-para-um cada Pedido tem exatamente um Pagamento
        Pedido, on_delete=models.CASCADE, related_name="pagamento", verbose_name="Pedido"
    )
    metodo = models.CharField("Método de Pagamento", max_length=20, choices=METODOS)  # O método escolhido para pagar.
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default="pendente")  # O status atual do pagamento.
    valor_pago = models.DecimalField("Valor Pago", max_digits=10, decimal_places=2, default=0)  # O valor que foi efetivamente pago.
    data_pagamento = models.DateTimeField("Data do Pagamento", blank=True, null=True)  # A data em que o pagamento foi confirmado. 

    class Meta:  # Metadados do modelo Pagamento.
        verbose_name = "Pagamento"  # Nome singular no admin.
        verbose_name_plural = "Pagamentos"  # Nome plural no admin.
        ordering = ["-data_pagamento"]  # Ordena pela data de pagamento, do mais recente para o mais antigo.

    def __str__(self):  # Define a representação em string de um objeto Pagamento.
        return f"Pagamento {self.id} - {self.get_metodo_display()} - {self.get_status_display()}" # Retorna informações do pagamento de forma legível.
    
# Modelo para Perfil do Usuário
class UserProfile(models.Model):  # Estende o modelo de usuário padrão com informações adicionais.
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")  # Relacionamento um-para-um com o modelo User.
    telefone = models.CharField(max_length=20, blank=True, null=True)  # Campo para o telefone do usuário.
    endereco = models.CharField(max_length=255, blank=True, null=True)  # Campo para o endereço.
    cidade = models.CharField(max_length=100, blank=True, null=True)  # Campo para a cidade.
    estado = models.CharField(max_length=50, blank=True, null=True)  # Campo para o estado.

    def __str__(self):  # Define a representação em string de um objeto UserProfile.
        return f"Perfil de {self.usuario.username}"  # Retorna uma string identificando o perfil pelo nome do usuário."""