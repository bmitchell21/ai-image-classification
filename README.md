# ai-image-classification
This repo contains the code to build an image classification app powered by AI. The application runs on Docker and uses Python, PyTorch, Flask, and ResNet.

### prerequisites
- Python
- Pip
- Docker

To use this application, follow the steps below:

1. Clone this repo
2. Open the terminal and navigate to the root of the repo
3. Run
   ```docker build -t ai-image-classification -f docker/Dockerfile .```
   ```docker run -p 4000:5000 ai-image-classification```
4. Open your browser and go to http://localhost:4000
5. Upload a png or jpeg image
