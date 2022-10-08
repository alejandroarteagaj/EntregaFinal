##Hecho y adaptado por juan camilo giraldo y alejandro arteaga
from concurrent import futures
import base64
from turtle import width
import numpy as np
import grpc
import cv2
import PIL 
import tensorflow as tf
import backend_pb2
import backend_pb2_grpc

 
class BackendService(backend_pb2_grpc.BackendServicer):
    def _test_func(self, path):
        global array
        image = cv2.imread(path)
        self.array = np.asarray(image)
        img2 = self.array.astype(float)
        img2show = PIL.Image.fromarray(self.array)
        img2 = (np.maximum(img2, 0) / img2.max()) * 255.0
        img2 = np.uint8(img2)
        h, w, _ = np.shape(image)
        print(f"image shape: w-{w} h-{h}")

        # OpenCV represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        
        return img2, w, h,img2show
    
    def load_image(self, request, context):##Funciona
        global path
        path = request.path
        print(path)
        img2,w,h,img2show= self._test_func(path=path)
        response_message = backend_pb2.image(img_content=img2show, width=w, height=h)
        return response_message
    
    def predict(self,request,context):
    #   1. call function to pre-process image: it returns image in batch format
      batch_array_img= self.preprocess()
    #   2. call function to load model and predict: it returns predicted class and probability
      modelo =  tf.keras.models.load_model("/home/src/interface/WilhemNet_86(1).h5")
    # model_cnn = tf.keras.models.load_model('conv_MLP_84.h5')
      prediction = np.argmax(modelo.predict(batch_array_img))
      
      label = ""
      if prediction == 0:
          label = "bacteriana"
      if prediction == 1:
          label = "normal"
      if prediction == 2:
          label = "viral"
    #   3. call function to generate Grad-CAM: it returns an image with a superimposed heatmap
      response_message = backend_pb2.label(label=label)
      return (response_message)
    
    
    

    def preprocess(self):
      global array21
      array21= cv2.resize(self.array, (512, 512))
      array2 = cv2.cvtColor(array21, cv2.COLOR_BGR2GRAY)
      clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
      global array23
      global array24
      array24 = clahe.apply(array2)
      array23 = array24 / 255
      array2 = np.expand_dims(array23, axis=-1)
      array2 = np.expand_dims(array2, axis=0)
      return array2 



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    backend_pb2_grpc.add_BackendServicer_to_server(BackendService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
