import os
import subprocess

def verificar_exiftool():
    """Verifica se o exiftool está disponível no sistema."""
    try:
        resultado = subprocess.run(['exiftool', '-ver'], capture_output=True, text=True, check=True)
        print(f"ExifTool versão: {resultado.stdout.strip()}")
    except subprocess.CalledProcessError:
        print("ExifTool não está instalado ou não está no PATH. Por favor, instale o ExifTool.")
        exit(1)

def extrair_metadados(caminho_pasta):
    # Lista de extensões de arquivos suportados
    extensoes_suportadas = ['.docx', '.pdf', '.mp4', '.mov', '.avi', '.jpg', '.jpeg', '.png', '.gif', '.tiff']
    
    # Caminho do arquivo de saída
    arquivo_saida = os.path.join(caminho_pasta, 'metadados_extrados.txt')
    
    with open(arquivo_saida, 'w') as saida:
        # Itera sobre os arquivos na pasta fornecida
        for root, dirs, files in os.walk(caminho_pasta):
            for file in files:
                # Verifica se o arquivo tem uma extensão suportada
                if any(file.lower().endswith(ext) for ext in extensoes_suportadas):
                    caminho_arquivo = os.path.join(root, file)
                    try:
                        # Comando exiftool para extrair metadados
                        print(f"Extraindo metadados de {caminho_arquivo}...")
                        resultado = subprocess.run(['exiftool', caminho_arquivo], capture_output=True, text=True, check=True)
                        metadados = resultado.stdout
                        
                        if metadados.strip():
                            # Escreve os metadados no arquivo de saída
                            saida.write(f'Arquivo: {caminho_arquivo}\n')
                            saida.write(metadados)
                            saida.write('\n' + '-'*60 + '\n')
                            print(f'Metadados extraídos de: {caminho_arquivo}')
                        else:
                            print(f'Nenhum metadado encontrado para: {caminho_arquivo}')
                    except subprocess.CalledProcessError as e:
                        print(f'Erro ao extrair metadados de {caminho_arquivo}: {e}')
                    except Exception as e:
                        print(f'Erro inesperado ao processar {caminho_arquivo}: {e}')
    
    print(f'Todos os metadados foram salvos em {arquivo_saida}')

def main():
    caminho_pasta = input('Digite o caminho da pasta: ').strip()
    
    if os.path.isdir(caminho_pasta):
        verificar_exiftool()
        extrair_metadados(caminho_pasta)
    else:
        print('O caminho fornecido não é uma pasta válida.')

if __name__ == '__main__':
    main()
