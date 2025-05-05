# Importador SIGAA-DSpace

O sistema tem como função importar arquivos ZIP para a plataforma DSpace, exportados pelo módulo "Produções Acadêmicas" do SIGAA.

## Requisitos de sistema

 - Python 3.9 ou superior
 - pip
 - PostgreSQL ou MySQL
 - Servidor web (Apache, Nginx ou semelhante)

É fortemente recomendada a instalação em um ambiente virtual (venv).

## Instalação

Após o clone do projeto, deve-se instalar as dependências via pip:

    pip install -r requirements.txt

## Configuração

Baseado no arquivo **.env.TEMPLATE**, deve-se criar um arquivo **.env** na raiz do projeto, com as seguintes configurações:

 - SECRET_KEY: pode ser gerada [neste link](https://djecrety.ir/)
 - DEBUG: ajustado para **False**, a menos em ambiente de desenvolvimento
 - ALLOWED_HOSTS: domínio ou endereço IP onde será servido o sistema
 - DATABASE_URL: string de conexão seguindo a sintaxe do template. Mais informações na documentação oficial da biblioteca [DJ-Database-URL](https://github.com/jacobian/dj-database-url#dj-database-url).
 - SOLR_URL: URL do SOLR utilizado pelo repositório DSpace
 - DSPACE_PATH: diretório de instalação base do DSpace
 - DSPACE_IMPORT_USER_MAIL: usuário que fará a importação dos arquivos (deve ser administrador do DSpace).
 - SENTRY_DSN: DSN do [sentry.io](https://sentry.io), caso utilizado (opcional).

Realizam-se as migrações no database:

    python manage.py migrate

E por fim, deve-se criar o usuário administrador:

    python manage.py createsuperuser

## Execução

Recomenda-se a utilização de um daemon para execução do Gunicorn, exposto via socket unix ou porta TCP. Feito isso, deve ser realizada a exposição do serviço via servidor web por proxy reverso para o importador.

## Links de referência

 - https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04
 - https://docs.djangoproject.com/en/3.0/howto/deployment/
 - https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
