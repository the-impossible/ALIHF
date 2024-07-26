import cv2

list_name = [
    'Dr. Adesola Oyinide',
    'Richard Emmanuel Eghenayarhiore',
]

for index, name in enumerate(list_name):
    template = cv2.imread(rf'ALIHF_cert\certificate.jpg')

    cv2.putText(template, name, (270, 375), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0,0,0), 1, cv2.LINE_AA)

    cv2.imwrite(rf"ALIHF_cert\generated\{index+1}cert.jpg", template)

    print(f"Processing Certificate {index + 1}/{len(list_name)}")