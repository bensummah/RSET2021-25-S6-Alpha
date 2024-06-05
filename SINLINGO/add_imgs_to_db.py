import mysql.connector

def insert_images(label, asl_image_path, isl_image_path):
    # Establish the database connection
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="anushri"
    )
    cursor = connection.cursor()

    # Open the ASL image file in binary mode
    with open(asl_image_path, 'rb') as asl_file:
        asl_binary_data = asl_file.read()

    # Open the ISL image file in binary mode
    with open(isl_image_path, 'rb') as isl_file:
        isl_binary_data = isl_file.read()

    # Insert the image data into the table
    sql_query = "INSERT INTO translation_table (label, asl_img, isl_img) VALUES (%s, %s, %s)"
    cursor.execute(sql_query, (label, asl_binary_data, isl_binary_data))
    connection.commit()

    cursor.close()
    connection.close()

# Example usage
insert_images('E', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL E.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL E.jpg')
insert_images('F', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL F.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL F.jpg')
insert_images('G', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL G.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL G.jpg')
insert_images('H', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL H.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL H.jpg')
insert_images('I', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL I.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL I.jpg')
insert_images('K', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL K.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL K.jpg')
insert_images('L', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL L.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL L.jpg')
insert_images('M', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL M.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL M.jpg')
insert_images('N', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL N.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL N.jpg')
insert_images('O', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL O.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL O.jpg')
insert_images('P', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL P.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL P.jpg')
insert_images('Q', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL Q.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL Q.jpg')
insert_images('R', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL R.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL R.jpg')
insert_images('S', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL S.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL S.jpg')
insert_images('T', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL T.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL T.jpg')
insert_images('U', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL U.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL U.jpg')
insert_images('V', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL V.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL V.jpg')
insert_images('W', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL W.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL W.jpg')
insert_images('X', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL X.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL X.jpg')
insert_images('Y', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ASL Y.jpg', 'C:/Program Files/MySQL/MySQL Server 8.0/Uploads/ISL Y.jpg')




