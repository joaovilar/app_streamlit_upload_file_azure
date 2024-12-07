import streamlit as st
from azure.storage.filedatalake import DataLakeServiceClient

# Função para conectar ao Azure Data Lake
def connect_to_datalake(account_name, account_key):
    try:
        service_client = DataLakeServiceClient(
            account_url=f"https://{account_name}.dfs.core.windows.net",
            credential=account_key
        )
        return service_client
    except Exception as e:
        st.error(f"Erro ao conectar ao Azure Data Lake: {e}")
        return None

# Função para listar os containers (sistemas de arquivos)
def list_file_systems(service_client):
    try:
        file_systems = []
        # Usando a função list_file_systems para listar os containers
        file_systems_client = service_client.list_file_systems()
        for fs in file_systems_client:
            file_systems.append(fs.name)
        return file_systems
    except Exception as e:
        st.error(f"Erro ao listar containers: {e}")
        return []

# Função para fazer upload do arquivo
def upload_file(service_client, container_name, file):
    try:
        file_system_client = service_client.get_file_system_client(file_system=container_name)
        directory_client = file_system_client.get_directory_client("/")
        file_path = f"/{file.name}"
        file_client = directory_client.create_file(file_path)
        file_client.append_data(file.read(), 0)
        file_client.flush_data(len(file.read()))
        st.success(f"Arquivo '{file.name}' enviado para o container '{container_name}' com sucesso!")
    except Exception as e:
        st.error(f"Erro ao enviar o arquivo: {e}")

# Configuração da página
st.set_page_config(page_title="Upload de Arquivo para o Azure Data Lake", layout="wide")

# Título da aplicação (visível acima dos outros componentes)
st.title("Upload de Arquivo para o Azure Data Lake")

# Variáveis de conexão (movidas para variáveis de ambiente em produção)
account_name = "your_name_storage"
account_key = "your_secreat"

# Conectando ao Azure Data Lake
service_client = connect_to_datalake(account_name, account_key)

if service_client:
    # Listando os containers
    file_systems = list_file_systems(service_client)

    if file_systems:
        # Permitir que o usuário escolha o container
        container_name = st.selectbox("Escolha o container para fazer o upload", file_systems)
        
        # Permitir que o usuário faça o upload de um arquivo
        file = st.file_uploader("Escolha um arquivo para fazer o upload", type=["json", "csv", "txt", "xlsx"])
        
        if file:
            if st.button("Fazer upload"):
                upload_file(service_client, container_name, file)
    else:
        st.warning("Nenhum container encontrado.")
