Note: this read me created using chatGT 


# File Upload and Processing Web Application

This Flask-based web application allows users to upload and process various types of files, including audio, image, and text files. The application provides functionalities like face detection in images, silence splitting in audio files, and named entity recognition (NER) in text files.

## Features

- **Audio Upload & Processing**:  
  Upload `.wav` files, which are then split into chunks based on silence. The chunks are merged back together and available for download.

- **Image Upload & Face Detection**:  
  Upload image files (`.png`, `.jpg`, `.jpeg`, `.gif`), which are processed to detect faces using a pre-trained deep learning model. The processed image with face bounding boxes is displayed.

- **Text Upload & NER**:  
  Upload `.txt` files. The application tokenizes the text and processes it for Named Entity Recognition (NER) using `nltk`.

## Prerequisites

Before running the application, ensure you have the following dependencies installed:

- Python 3.x
- Flask
- OpenCV
- pydub
- nltk
- werkzeug

You can install these dependencies using `pip`:

```bash
pip install flask opencv-python pydub nltk werkzeug
```

## Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Ibn-mohey/machine-learning-flask-app.git 
   cd machine-learning-flask-app
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Download necessary NLTK data**:

   The app requires certain NLTK datasets. Run the following Python commands:

   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('averaged_perceptron_tagger')
   nltk.download('maxent_ne_chunker')
   nltk.download('words')
   ```

## Running the Application

To run the Flask application, execute the following:

```bash
python app.py
```

The application will start on `http://localhost:5000` by default. You can access the features via the browser.

## Directory Structure

```
/static
    /input           - Folder for uploaded images and audio files
    /music_input     - Folder for uploaded audio files
    /music_out       - Folder for processed audio chunks
    /output          - Folder for processed images
    /text_in         - Folder for uploaded text files
/text_model_data
    deploy.prototxt  - Caffe model prototxt file
    weights.caffemodel - Caffe model weights file
```

## Endpoints

- **`/`**: Main page, provides links to upload and process audio, image, and text files.
- **`/audio`**: Upload `.wav` audio files and split them based on silence.
- **`/audio_download`**: Download the processed audio.
- **`/image`**: Upload images and detect faces using OpenCV.
- **`/predict_image`**: Display the image with detected faces.
- **`/text`**: Upload `.txt` files for Named Entity Recognition (NER).
- **`/predict_text`**: Display the NER results of the uploaded text file.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to your branch (`git push origin feature/your-feature`).
6. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [OpenCV](https://opencv.org/)
- [pydub](https://pydub.com/)
- [nltk](https://www.nltk.org/)
- [werkzeug](https://werkzeug.palletsprojects.com/)
```

