#This is the code where the multi-threaded socket client will be

class TorrentClient():



# import socket, cv2, pickle, struct
# import pyshine as ps #optional: pip install pyshine
# import imutils
#
#
#
# camera = True
# if camera:
#     vid = cv2.VideoCapture(0)
# else:
#     vid = cv2.VideoCapture("videos/top.mp4")  #Example
#
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host_ip = #ENTER THE IP ADDRESS OF THE server
#
# port = #HERE GOES THE PORT
#
# client_socket.connect((host_ip, port))
#
# if client_socket:
#     while(vid.isOpened()):
#         try:
#             img, frame = vid.read()
#             frame = imutils.resize(frame, width=380)
#             a=pickle.dumps(frame) #BYTES TYPE RECEIVED!
#             message = struct.pack("Q",len(a))+a
#             client_socket.sendall(message)
#
#
