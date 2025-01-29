from flask import Flask, request, send_file, jsonify
from base_functions import generate_image_1, generate_image_2, generate_image_3  # Replace with your actual import
from io import BytesIO
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

app = Flask(__name__)

@app.route('/generate_image_1', methods=['POST'])
def generate_image_1_endpoint():
    data = request.get_json()
    try:
        # Ensure the data is valid
        if not data:
            raise BadRequest("No data provided.")
        
        # Collecting data from the POST request
        required_fields = ['serial', 'owner', 'sales_name', 'nationality', 'idNo', 'phone', 'landline', 'central', 'quota', 'price', 'payment_frequency', 'date']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise BadRequest(f"Missing required fields: {', '.join(missing_fields)}")
        
        base_image_path = "base_image_1.jpg"  # Adjust the image path
        serial = data.get('serial')
        owner = data.get('owner')
        sales_name = data.get('sales_name')
        nationality = data.get('nationality')
        idNo = data.get('idNo')
        phone = data.get('phone')
        landline = data.get('landline')
        central = data.get('central')
        quota = data.get('quota')
        price = data.get('price')
        payment_frequency = data.get('payment_frequency')
        date = data.get('date')
        
        # Generate the image and return as a response
        img_buffer = generate_image_1(base_image_path, serial, owner, sales_name, nationality, idNo, phone, landline, central, quota, price, payment_frequency, date)
        
        return send_file(img_buffer, mimetype='image/jpeg', as_attachment=True, download_name="image_1.jpg")
    
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


@app.route('/generate_image_2', methods=['POST'])
def generate_image_2_endpoint():
    data = request.form
    try:
        # Ensure data is present
        if not data:
            raise BadRequest("No form data provided.")
        
        # Collecting text data from the POST request
        required_fields = ['owner', 'central', 'date', 'landline']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise BadRequest(f"Missing required fields: {', '.join(missing_fields)}")

        # Collecting file data from the POST request (as buffers)
        front_id_file = request.files.get('front_id')
        back_id_file = request.files.get('back_id')
        stamp_file = request.files.get('stamp')

        if not all([front_id_file, back_id_file, stamp_file]):  # Check that all images are provided
            raise BadRequest("front_id, back_id, and stamp images are required.")

        # Validate file formats (only images)
        for file in [front_id_file, back_id_file, stamp_file]:
            if not file.content_type.startswith('image/'):
                raise UnsupportedMediaType(f"File {file.filename} is not a valid image format.")
        
        # Create BytesIO buffers directly from file content
        front_id_buffer = BytesIO(front_id_file.read())
        back_id_buffer = BytesIO(back_id_file.read())
        stamp_buffer = BytesIO(stamp_file.read())

        # Collecting other paths and details for image generation
        base_image_path = "base_image_2.jpg"  # Adjust the image path

        # Generate the image and return as a response
        img_buffer = generate_image_2(base_image_path, stamp_buffer, front_id_buffer, back_id_buffer, data['owner'], data['central'], data['date'], data['landline'])
        
        return send_file(img_buffer, mimetype='image/jpeg', as_attachment=True, download_name="image_2.jpg")

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except UnsupportedMediaType as e:
        return jsonify({"error": str(e)}), 415
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


@app.route('/generate_image_3', methods=['POST'])
def generate_image_3_endpoint():
    data = request.get_json()
    try:
        # Ensure the data is valid
        if not data:
            raise BadRequest("No data provided.")
        
        # Collecting data from the POST request
        required_fields = ['owner', 'renter_name']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise BadRequest(f"Missing required fields: {', '.join(missing_fields)}")
        
        base_image_path = "base_image_3.jpg"  # Adjust the image path
        owner = data.get('owner')
        renter_name = data.get('renter_name')
        
        # Generate the image and return as a response
        img_buffer = generate_image_3(base_image_path, owner, renter_name)
        
        return send_file(img_buffer, mimetype='image/jpeg', as_attachment=True, download_name="image_3.jpg")
    
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=8000)
