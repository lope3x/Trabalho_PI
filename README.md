# Trabalho_PI
### Grupo
- Bruno Duarte de Paula Assis 
- Gabriel Lopes Ferreira
- Giovanni Carlos Guaceroni

### Instruções de como executar o projeto
- Para rodar o projeto é necessário ter o Python 3.8 instalado.
- Execute os comandos abaixo para instalar as dependências:
  ```
  pip install tkinter
  pip install pillow
  pip install scikit-learn
  pip install scikit-image
  pip install numpy
  pip install joblib
  ```
- Coloque o banco de imagens de treino em uma pasta chamada "imgs" de forma que o diretorio fique igual ao abaixo.

    ```
    ├── imgs/            
        ├── 1/ #Dentro de cada uma dessas pastas deverá ter as imagens 
        ├── 2/ utilizadas para o teste no formato png
        ├── 3/
        ├── 4/
    ```

- Em seguida execute `python main.py` para rodar o projeto.
- O arquivo `svm.joblib` contém um classificador previamente treinado.