# Detección de Números de Dados en Videos de Tiradas de Dados

## Modo de Uso

1. Clonar el repositorio:

```bash
git clone https://github.com/tu_usuario/tu-repositorio.git
```

2. Instalar las librerías necesarias mediante:

```bash
pip install -r requirements.txt
```

3. Para obtener resultados para todos los videos, ejecutar el archivo `video_generator.py`.

4. Para obtener resultados para un video específico, sigue estos pasos:

   - Abre el archivo `laboratory.py`.
   - Modifica la asignación de la variable `video_path`, colocando el nombre del archivo que deseas procesar entre comillas:

     ```python
     video_path = 'tirada_1.mp4'
     ```

   - Asigna el nombre deseado para el video resultado también entre comillas en la variable `output_path`:

     ```python
     output_path = 'resultado_tirada_1.mp4'
     ```

   - Finalmente, ejecuta `laboratory.py`.
