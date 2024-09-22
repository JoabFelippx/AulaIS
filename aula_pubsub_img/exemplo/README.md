# Aula de Quarta: Transferência de Imagem Usando PUB/SUB

 - Aplicar os conceitos de PUB e SUB para criar um código de transferência de arquivos, especificamente imagens.

 - Compreender a biblioteca is-msgs e seu uso com mensagens protobuf.
 
 - Aprender o comando scp para transferir arquivos entre máquinas.

 - Desafio: Construir uma Docker image para rodar o código PUB em um container

## Estrutura da Aula

1. ### Introdução Breve revisão do conceito PUB/SUB:  

    PUB: Publicar uma mensagem (ex: imagem). 

    SUB: Consumir o tópico e receber a mensagem. 

2. ### Biblioteca is-msgs Apresentação da biblioteca is-msgs:

    Link da documentação: [is-msgs](https://github.com/labvisio/is-msgs).

    Descrição da estrutura da mensagem para [imagem](https://github.com/labvisio/is-msgs/tree/master/docs#is.vision.Image) usando Protobuf.

3. ### Transformação de Imagem no PUB e SUB

     - Função to_image: Transforma uma imagem em um array de bytes no lado do PUB.

        ```python
        def to_image(input_image, encode_format='.jpeg', compression_level=0.8):
            if isinstance(input_image, np.ndarray):
                if encode_format == '.jpeg':
                    params = [cv2.IMWRITE_JPEG_QUALITY, int(compression_level * (100 - 0) + 0)]
                elif encode_format == '.png':
                    params = [cv2.IMWRITE_PNG_COMPRESSION, int(compression_level * (9 - 0) + 0)]
                else:
                    return Image()
                cimage = cv2.imencode(ext=encode_format, img=input_image, params=params)
                return Image(data=cimage[1].tobytes())
            elif isinstance(input_image, Image):
                return input_image
            else:
                return Image()
        ```

    - Função to_np: Converte o array de bytes em um numpy_array para processamento no lado do SUB.

        ```python
        def to_np(input_image):
            if isinstance(input_image, np.ndarray):
                output_image = input_image
            elif isinstance(input_image, Image):
                buffer = np.frombuffer(input_image.data, dtype=np.uint8)
                output_image = cv2.imdecode(buffer, flags=cv2.IMREAD_COLOR)
            else:
                output_image = np.array([], dtype=np.uint8)
            return output_image
        ```

4. ### Transferência de Arquivo Usando SCP

    #### Exemplos:
    - Transferir arquivo da máquina local para um servidor:

        ```bash
        scp /path/source/filename user-destination@ip-destination:/path/destination
        ```

    - Transferir arquivo do servidor para a máquina local:

        ```
        scp user-source@ip-source:/path/source/filename /path/destination
        ```

    #### Dica: Use pwd no terminal para encontrar o caminho atual.

### Exercício:

- Baixar uma imagem .jpg da internet.
- Transferir a imagem para outra máquina usando scp.

### Instalação das Bibliotecas Necessárias

#### Numpy:
```bash
pip3 install numpy
```

#### OpenCV-Python (headless):

#### A versão headless do OpenCV é útil em ambientes sem interface gráfica (servidores por exemplo).
```bash
pip3 install opencv-python-headless
```

### Construção de Docker Image (Desafio - obrigatório)
Criar um Dockerfile para rodar o código PUB em um container.
Incluir as dependências instaladas (ex.: numpy, opencv-python-headless).
