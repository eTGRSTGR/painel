import streamlit as st
from PIL import Image
import io

def split_image(image, pages_width, pages_height, margin=0):
    width, height = image.size
    page_width = (width - (pages_width - 1) * margin) // pages_width
    page_height = (height - (pages_height - 1) * margin) // pages_height
    
    pages = []
    for y in range(pages_height):
        for x in range(pages_width):
            left = x * (page_width + margin)
            top = y * (page_height + margin)
            right = left + page_width
            bottom = top + page_height
            
            page = image.crop((left, top, right, bottom))
            pages.append(page)
    
    return pages

# Função para gerar uma miniatura (prévia) da imagem
def generate_thumbnail(image, size=(150, 150)):
    return image.resize(size, Image.Resampling.LANCZOS)

# Função para simular a visualização estilo "Publisher"
def show_preview(pages, pages_width, pages_height):
    # Organizar as páginas em uma grade
    cols = st.columns(pages_width)
    for i, page in enumerate(pages):
        col = i % pages_width
        # Exibir a imagem de cada página em sua coluna
        cols[col].image(page, caption=f'Página {i+1}')

# Função para salvar a imagem em formato PDF
def save_image_as_pdf(pages, filename):
    pdf_pages = [page.convert("RGB") for page in pages]
    pdf_pages[0].save(filename, save_all=True, append_images=pdf_pages[1:], resolution=100.0)

# Função para salvar as imagens em formato PNG
def save_image_as_png(pages, filename):
    pages[0].save(filename, format='PNG')

st.title('Criador de Painel')

uploaded_file = st.file_uploader("Escolha uma imagem", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Mostrar a imagem original
    st.image(image, caption='Imagem Original', use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col2:
        pages_width = st.number_input('Número de páginas (largura)', 1, 10, 2)
        pages_height = st.number_input('Número de páginas (altura)', 1, 10, 2)
        margin = st.slider('Selecione a largura da margem entre páginas (em pixels)', 0, 100, 10)
    
    if st.button('Processar'):
        # Dividir a imagem original em partes
        pages = split_image(image, pages_width, pages_height, margin)
        
        # Mostrar a prévia das páginas em formato estilo Publisher
        st.write('### Visualização do Layout (Estilo Publisher)')
        show_preview(pages, pages_width, pages_height)
        
        # Converter página para bytes para download
        st.write('### Páginas individuais para download:')
        for i, page in enumerate(pages):
            buf = io.BytesIO()
            page.save(buf, format='PNG')
            byte_im = buf.getvalue()
            
            st.download_button(
                label=f"Download página {i+1} (PNG)",
                data=byte_im,
                file_name=f'original_page_{i+1}.png',
                mime='image/png'
            )
        
        # Opções de download do arquivo inteiro como PDF ou PNG
        st.write('### Baixar o arquivo inteiro:')
        save_as_pdf = st.button('Baixar como PDF')
        save_as_png = st.button('Baixar como PNG')

        if save_as_pdf:
            pdf_filename = 'imagem_dividida.pdf'
            save_image_as_pdf(pages, pdf_filename)
            with open(pdf_filename, "rb") as pdf_file:
                st.download_button(
                    label="Baixar PDF",
                    data=pdf_file,
                    file_name=pdf_filename,
                    mime="application/pdf"
                )
        
        if save_as_png:
            png_filename = 'imagem_dividida.png'
            save_image_as_png(pages, png_filename)
            with open(png_filename, "rb") as png_file:
                st.download_button(
                    label="Baixar PNG",
                    data=png_file,
                    file_name=png_filename,
                    mime="image/png"
                )
